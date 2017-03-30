"""
Survey views
------------
"""

import logging
import urlparse
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import aq_base
from AccessControl import getSecurityManager
from zExceptions import Unauthorized
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from five import grok
from zope.interface import directlyProvides
from zope.interface import directlyProvidedBy
from zope.component import adapts
from zope.component import getUtility
from z3c.appconfig.interfaces import IAppConfig
from z3c.saconfig import Session
from sqlalchemy import orm
from sqlalchemy import sql
from plone.memoize.instance import memoize
from plonetheme.nuplone.tiles.analytics import trigger_extra_pageview
from ..ghost import PathGhost
from .. import MessageFactory as _
from euphorie.content.survey import ISurvey
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import ICustomizationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client.navigation import getTreeData
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.client.profile import extractProfile
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client import model
from euphorie.client import utils
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

PloneLocalesFactory = MessageFactory("plonelocales")


log = logging.getLogger(__name__)

grok.templatedir("templates")


class View(grok.View):
    """The default view which shows an overview of a user's sessions for the
    current survey.

    View name: @@index_html
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("survey_sessions")
    grok.name("index_html")

    def sessions(self):
        """Return a list of all sessions for the current user. For each
        session a dictionary is returned with the following keys:

        * `id`: unique identifier for the session
        * `title`: session title
        * `modified`: timestamp of last session modification
        """
        survey = aq_inner(self.context)
        my_path = utils.RelativePath(self.request.client, survey)
        account = getSecurityManager().getUser()
        result = [{'id': session.id,
                 'title': session.title,
                 'modified': session.modified}
                 for session in account.sessions
                 if session.zodb_path == my_path]
        result.sort(key=lambda s: s['modified'], reverse=True)
        return result

    def _NewSurvey(self, info):
        """Utility method to start a new survey session."""
        survey = aq_inner(self.context)
        title = info.get("title", u"").strip()
        if not title:
            title = survey.Title()
        SessionManager.start(title=title, survey=survey)
        v_url = urlparse.urlsplit(self.url()+'/resume').path
        trigger_extra_pageview(self.request, v_url)
        self.request.response.redirect("%s/start?initial_view=1" % survey.absolute_url())

    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session = Session.query(model.SurveySession).get(info["session"])
        current_user = aq_base(getSecurityManager().getUser())
        if session.account is not current_user:
            log.warn('User %s tried to hijack session from %s',
                    getattr(current_user, 'loginname', repr(current_user)),
                    session.account.loginname)
            raise Unauthorized()
        SessionManager.resume(session)
        survey = self.request.client.restrictedTraverse(str(session.zodb_path))
        v_url = urlparse.urlsplit(self.url()+'/resume').path
        trigger_extra_pageview(self.request, v_url)
        self.request.response.redirect("%s/resume?initial_view=1" % survey.absolute_url())

    def update(self):
        utils.setLanguage(self.request, self.context)
        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply["action"] == "new":
                self._NewSurvey(reply)
            elif reply["action"] == "continue":
                self._ContinueSurvey(reply)
        else:
            survey = aq_inner(self.context)
            dbsession = SessionManager.session
            if dbsession is not None and \
                    dbsession.zodb_path == utils.RelativePath(
                                        self.request.client, survey):
                self.request.response.redirect(
                        "%s/resume?initial_view=1" % survey.absolute_url())


class Start(grok.View):
    """Survey start screen.

    This view shows basic introduction text and any extra information provided
    the sector if present. After viewing this page the user is forwarded to the
    profile page.

    View name: @@start
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("start")
    grok.name("start")

    @memoize
    def has_introduction(self):
        survey = aq_inner(self.context)
        return utils.HasText(getattr(survey, "introduction", None))

    def update(self):
        survey = aq_inner(self.context)
        if self.request.environ["REQUEST_METHOD"] != "POST":
            return

        self.request.response.redirect("%s/@@profile" % survey.absolute_url())


class Resume(grok.View):
    """Survey resume screen.

    This view is used when a user resumes an existing session.

    View name: @@resume
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("resume")

    def render(self):
        survey = aq_inner(self.context)
        dbsession = SessionManager.session
        if redirectOnSurveyUpdate(self.request):
            return

        question = FindFirstQuestion(dbsession=dbsession)
        if question is None:
            # No tree generated, so start over
            self.request.response.redirect("%s/start?initial_view=1" % survey.absolute_url())
        else:
            # Redirect to the start page of the Identification phase.
            # We do this to ensure the screen with the tool name gets shown.
            # If we jump directly to the first question, the user does not
            # see the tool name.
            # This is especially relevant since the osc-header now displays the
            # user-given session name.
            self.request.response.redirect(
                "{0}/{1}?initial_view=1".format(survey.absolute_url(), "identification"))


class Identification(grok.View):
    """Survey identification start page.

    This view shows the introduction text for the identification phase. This
    includes an option to print a report with all questions.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object
    for the *identification* component of the URL.

    View name: @@index_html
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("identification")
    grok.name("index_html")

    question_filter = None

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return
        self.survey = survey = aq_parent(aq_inner(self.context))
        question = FindFirstQuestion(filter=self.question_filter)
        if question is not None:
            self.next_url = QuestionURL(
                survey, question, phase="identification")
            self.tree = getTreeData(self.request, question)
        else:
            self.next_url = None

    @property
    def extra_text(self):
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        have_extra = settings.get('extra_text_idendification', False)
        if not have_extra:
            return None
        lang = getattr(self.request, 'LANGUAGE', 'en')
        # Special handling for Flemish, for which LANGUAGE is "nl-be". For
        # translating the date under plone locales, we reduce to generic "nl".
        # For the specific oira translation, we rewrite to "nl_BE"
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        return translate(_(
            u"extra_text_identification", default=u""), target_language=lang)


class ActionPlan(grok.View):
    """Survey action plan start page.

    This view shows the introduction text for the action plan phase.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *actionplan* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("actionplan")
    grok.name("index_html")

    question_filter = model.ACTION_PLAN_FILTER

    def update(self):
        self.survey = survey = aq_parent(aq_inner(self.context))
        question = FindFirstQuestion(filter=self.question_filter)
        if question is not None:
            self.next_url = QuestionURL(survey, question, phase="actionplan")
            self.tree = getTreeData(
                self.request, question,
                filter=self.question_filter, phase="actionplan")
        else:
            self.next_url = None


class Status(grok.View):
    """Show survey status information.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("status")

    def __init__(self, context, request):
        super(Status, self).__init__(context, request)
        default_risks_by_status = lambda: {
            'present': {
                'high': [],
                'medium': [],
                'low': [],
            },
            'possible': {
                'postponed': [],
                'todo': [],
            },
        }
        self.risks_by_status = defaultdict(default_risks_by_status)
        now = datetime.now()
        lang = date_lang = getattr(self.request, 'LANGUAGE', 'en')
        # Special handling for Flemish, for which LANGUAGE is "nl-be". For
        # translating the date under plone locales, we reduce to generic "nl".
        # For the specific oira translation, we rewrite to "nl_BE"
        if "-" in lang:
            date_lang = lang.split("-")[0]
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.date = u"{0} {1} {2}".format(
            now.strftime('%d'),
            translate(
                PloneLocalesFactory(
                    "month_{0}".format(now.strftime('%b').lower()),
                    default=now.strftime('%B'),
                ),
                target_language=date_lang,),
            now.strftime('%Y')
        )
        self.label_page = translate(_(u"label_page", default=u"Page"), target_language=lang)
        self.label_page_of = translate(_(u"label_page_of", default=u"of"), target_language=lang)
        session = SessionManager.session
        if (
            session is not None and session.title != (
                callable(getattr(self.context, 'Title', None)) and
                self.context.Title() or ''
            )
        ):
            self.session_title = session.title
        else:
            self.session_title = None

    def module_query(self, sessionid, optional_modules):
        if optional_modules:
            omc = """WHEN profile_index != -1 AND zodb_path IN %(modules)s
                        THEN SUBSTRING(path FROM 1 FOR 6)
                    WHEN profile_index = -1 AND zodb_path IN %(modules)s
                        THEN SUBSTRING(path FROM 1 FOR 3) || '000-profile'
            """ % dict(modules=optional_modules)
        else:
            omc = ""
        query = """
            SELECT
                CASE %(OPTIONAL_MODULE_CLAUSE)s
                    WHEN profile_index != -1 AND depth < 2
                    THEN SUBSTRING(path FROM 1 FOR 3)
                END AS module
            FROM tree
            WHERE session_id=%(sessionid)d AND type='module'
            GROUP BY module
            ORDER BY module
        """ % dict(OPTIONAL_MODULE_CLAUSE=omc, sessionid=sessionid)
        return query

    def slicePath(self, path):
        while path:
            yield path[:3].lstrip("0")
            path = path[3:]

    def getModules(self):
        """ Return a list of dicts of all the top-level modules and locations
            belonging to this survey.
        """
        session = Session()
        session_id = SessionManager.id
        base_url = "%s/identification" % self.request.survey.absolute_url()
        profile = extractProfile(self.request.survey, SessionManager.session)
        module_query = self.module_query(
            sessionid=session_id,
            optional_modules=len(profile) and "(%s)" % (','.join(
                ["'%s'" % k for k in profile.keys()])) or None
        )
        module_res = session.execute(module_query).fetchall()
        modules_and_profiles = {}
        for row in module_res:
            if row[0] is not None:
                if row[0].find('profile') > 0:
                    path = row[0][:3]
                    modules_and_profiles[path] = 'profile'
                else:
                    modules_and_profiles[row[0]] = ''
        module_paths = [
            p[0] for p in session.execute(module_query).fetchall() if
            p[0] is not None]
        module_paths = modules_and_profiles.keys()
        module_paths = sorted(module_paths)
        parent_node = orm.aliased(model.Module)
        titles = dict(session.query(model.Module.path, model.Module.title)
                .filter(model.Module.session_id == session_id)
                .filter(model.Module.path.in_(module_paths)))

        location_titles = dict(session.query(
                    model.Module.path,
                    parent_node.title
                ).filter(
                        model.Module.session_id == session_id).filter(
                        model.Module.path.in_(module_paths)).filter(
                        sql.and_(
                            parent_node.session_id == session_id,
                            parent_node.depth < model.Module.depth,
                            model.Module.path.like(parent_node.path + "%")
                        )
                ))
        modules = {}
        toc = {}
        title_custom_risks = utils.get_translated_custom_risks_title(self.request)

        for path in module_paths:
            number = ".".join(self.slicePath(path))
            # top-level module, always include it in the toc
            if len(path) == 3:
                title = titles[path]
                if title == 'title_other_risks':
                    title = title_custom_risks
                toc[path] = {
                    'path': path,
                    'title': title,
                    'locations': [],
                    'number': number,
                }
                # If this is a profile (aka container for locations), skip
                # adding to the list of modules
                if modules_and_profiles[path] == 'profile':
                    continue
            # sub-module (location) or location container
            else:
                if path in location_titles:
                    title = u"{0} - {1}".format(location_titles[path], titles[path])
                    toc[path[:3]]['locations'].append({
                        'path': path,
                        'title': titles[path],
                        'number': number,
                    })
                else:
                    log.warning(
                        "Status: found a path for a submodule {0} for which "
                        "there's no location title.".format(path))
                    continue

            modules[path] = {
                'path': path,
                'title': title,
                'url': '%s/%s' % (base_url, '/'.join(self.slicePath(path))),
                'todo': 0,
                'ok': 0,
                'postponed': 0,
                'risk_with_measures': 0,
                'risk_without_measures': 0,
                'number': number,
            }
        self.tocdata = toc
        return modules

    def getRisks(self, module_paths):
        """ Return a list of risk dicts for risks that belong to the modules
            with paths as specified in module_paths.
        """
        session = Session()
        session_id = SessionManager.id
        # First, we need to compute the actual module paths, making sure that
        # skipped optional modules are excluded
        # This means top-level module paths like 001 or 001002 can be replaced
        # by several sub-modules paths like 001002, 001003 and 001002001
        module_query = """
        SELECT path
        FROM tree
        WHERE
            session_id={0}
            AND type='module'
            AND skip_children='f'
            and tree.path similar to '({1}%)'
            ORDER BY path
        """.format(session_id, "%|".join(module_paths))
        module_res = session.execute(module_query).fetchall()

        def nodes(paths):
            paths = sorted(paths, reverse=True)
            ret = []
            for elem in paths:
                if not [x for x in ret if x.startswith(elem)]:
                    ret.append(elem)
            return ret
        # Here we make sure that only the longest paths of sub-modules
        # are used, but not the parents. Example
        # (001, 002, 001001, 001003) will be turned into
        # (001001, 001003, 002), since the parent 001 contains sub-modules,
        # and some of those might have been de-selected, like 001002
        filtered_module_paths = nodes([x[0] for x in module_res])

        child_node = orm.aliased(model.Risk)
        risks = session.query(
                    model.Module.path,
                    child_node.id,
                    child_node.path,
                    child_node.title,
                    child_node.identification,
                    child_node.priority,
                    child_node.risk_type,
                    child_node.zodb_path,
                    child_node.is_custom_risk,
                    child_node.postponed
                ).filter(
                    sql.and_(
                        model.Module.session_id == session_id,
                        model.Module.path.in_(filtered_module_paths),
                        sql.and_(
                            child_node.session_id == model.Module.session_id,
                            child_node.depth > model.Module.depth,
                            child_node.path.like(model.Module.path + "%")
                        )
                    )
                )

        def _module_path(path):
            # Due to the extended query above that replaces top-module paths
            # with sub-module paths (if present), we need to cut back the path
            # under which we store each risk back to the original top-level
            # module path
            for mp in module_paths:
                if path.startswith(mp):
                    return mp
        return [{
                'module_path': _module_path(risk[0]),
                'id': risk[1],
                'path': risk[2],
                'title': risk[3],
                'identification': risk[4],
                'priority': risk[5],
                'risk_type': risk[6],
                'zodb_path': risk[7],
                'is_custom_risk': risk[8],
                'postponed': risk[9],
            } for risk in risks]

    def getStatus(self):
        """ Gather a list of the modules and locations in this survey as well
            as data around their state of completion.
        """
        session = Session()
        total_ok = 0
        total_with_measures = 0
        modules = self.getModules()
        risks = self.getRisks([m['path'] for m in modules.values()])
        for r in risks:
            has_measures = False
            if r['identification'] in ['yes', 'n/a']:
                total_ok += 1
                modules[r['module_path']]['ok'] += 1
            elif r['identification'] == 'no':
                measures = session.query(
                        model.ActionPlan.id
                    ).filter(model.ActionPlan.risk_id == r['id'])
                if measures.count():
                    has_measures = True
                    modules[r['module_path']]['risk_with_measures'] += 1
                    total_with_measures += 1
                else:
                    modules[r['module_path']]['risk_without_measures'] += 1
            elif r['postponed']:
                modules[r['module_path']]['postponed'] += 1
            else:
                modules[r['module_path']]['todo'] += 1

            self.add_to_risk_list(r, has_measures=has_measures)

        for key, m in modules.items():
            if m['ok'] + m['postponed'] + m['risk_with_measures'] + m['risk_without_measures'] + m['todo'] == 0:
                del modules[key]
                del self.tocdata[key]
        self.percentage_ok = not len(risks) and 100 or int((total_ok + total_with_measures) / Decimal(len(risks))*100)
        self.status = modules.values()
        self.status.sort(key=lambda m: m["path"])
        self.toc = self.tocdata.values()
        self.toc.sort(key=lambda m: m["path"])

    def add_to_risk_list(self, r, has_measures=False):
        if self.is_skipped_from_risk_list(r):
            return

        risk_title = self.get_risk_title(r)

        base_url = "%s/actionplan" % self.request.survey.absolute_url()
        url = '%s/%s' % (base_url, '/'.join(self.slicePath(r['path'])))

        if r['identification'] != 'no':
            status = r['postponed'] and 'postponed' or 'todo'
            self.risks_by_status[r['module_path']]['possible'][status].append({'title': risk_title, 'path': url})
        else:
            self.risks_by_status[r['module_path']]['present'][r['priority'] or 'low'].append({'title': risk_title, 'path': url, 'has_measures': has_measures})

    def get_risk_title(self, r):
        if r['is_custom_risk']:
            risk_title = r['title']
        else:
            risk_obj = self.request.survey.restrictedTraverse(r['zodb_path'].split('/'))
            if not risk_obj:
                return
            if r['identification'] == 'no':
                risk_title = risk_obj.problem_description
            else:
                risk_title = r['title']
        return risk_title

    def is_skipped_from_risk_list(self, r):
        if r['priority'] == "high":
            if r['identification'] != 'no':
                if r['risk_type'] not in ['top5']:
                    return True
        else:
            return True

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return
        self.getStatus()


def find_sql_context(session_id, zodb_path):
    """Find the closest SQL tree node for a candidate path.

    The path has to be given as a list of path entries. The session
    timestamp is only used as part of a cache key for this method.

    The return value is the id of the SQL tree node. All consumed
    entries will be removed from the zodb_path list.
    """
    # Pop all integer elements from the URL
    path = ""
    head = []
    while zodb_path:
        next = zodb_path.pop()
        if len(next) > 3:
            zodb_path.append(next)
            break

        try:
            path += '%03d' % int(next)
            head.append(next)
        except ValueError:
            zodb_path.append(next)
            break

    # Try and find a SQL tree node that matches our URL
    query = Session.query(model.SurveyTreeItem.id).\
            filter(model.SurveyTreeItem.session_id == session_id).\
            filter(model.SurveyTreeItem.path == sql.bindparam('path'))
    while path:
        node = query.params(path=path).first()
        if node is not None:
            return node[0]
        path = path[:-3]
        zodb_path.append(head.pop())


def build_tree_aq_chain(root, tree_id):
    """Build an acquisition context for a tree node.
    """
    tail = Session.query(model.SurveyTreeItem).get(tree_id)
    walker = root
    path = tail.path
    while len(path) > 3:
        id = str(int(path[:3]))
        path = path[3:]
        walker = PathGhost(id).__of__(walker)
    return tail.__of__(walker)


class SurveyPublishTraverser(DefaultPublishTraverse):
    """Publish traverser to setup the survey skin layers.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent sine in Zope 2 that is only fired for site objects.
    """
    adapts(ISurvey, IClientSkinLayer)

    phases = {
        'identification': IIdentificationPhaseSkinLayer,
        'customization': ICustomizationPhaseSkinLayer,
        'evaluation': IEvaluationPhaseSkinLayer,
        'actionplan': IActionPlanPhaseSkinLayer,
        'report': IReportPhaseSkinLayer}

    def hasValidSession(self, request):
        """Check if the user has an active session for the survey.
        """
        dbsession = SessionManager.session
        client_path = utils.RelativePath(request.client, self.context)

        if dbsession is None or \
                dbsession.zodb_path != client_path:

            # Allow for alternative session ids to be hardcoded in the
            # euphorie.ini file for automatic browser testing with Browsera
            conf = getUtility(IAppConfig).get("euphorie", {})
            debug_ids = conf.get('debug_sessions', '').strip().splitlines()
            for sid in debug_ids:
                session = Session.query(model.SurveySession).get(sid)
                if hasattr(session, 'zodb_path') and \
                        session.zodb_path == client_path:
                    SessionManager.resume(session)
                    return True

            return False
        return True

    def publishTraverse(self, request, name):
        request.survey = self.context
        utils.setLanguage(request, self.context, self.context.language)

        if name not in ["view", "index_html"] and \
                not self.hasValidSession(request):
            request.response.redirect(
                    aq_parent(aq_parent(self.context)).absolute_url(),
                    lock=True)
            return self.context

        if name not in self.phases:
            return super(SurveyPublishTraverser, self)\
                    .publishTraverse(request, name)

        # Decorate the request with the right skin layer and add to the aq path
        directlyProvides(request, self.phases[name],
                         *directlyProvidedBy(request))
        self.context = PathGhost(name).__of__(self.context)

        session = SessionManager.session
        tree_id = find_sql_context(session.id,
                request['TraversalRequestNameStack'])
        if tree_id is not None:
            return build_tree_aq_chain(self.context, tree_id)

        # No SQL based traversal possible, return the existing context with the
        # new skin layer applied
        return self.context
