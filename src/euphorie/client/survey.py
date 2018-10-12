"""
Survey views
------------
"""
from .. import MessageFactory as _
from ..ghost import PathGhost
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.country import IClientCountry
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.interfaces import ICustomizationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IItalyActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IItalyCustomizationPhaseSkinLayer
from euphorie.client.interfaces import IItalyEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IItalyIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IItalyReportPhaseSkinLayer
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.navigation import QuestionURL
from euphorie.client.profile import extractProfile
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.content.survey import ISurvey
from five import grok
from plone import api
from plone.memoize.instance import memoize
from plone.memoize.view import memoize_contextless
from sqlalchemy import case
from sqlalchemy import func
from sqlalchemy import orm
from sqlalchemy import sql
from z3c.appconfig.interfaces import IAppConfig
from z3c.saconfig import Session
from zope.component import adapts
from zope.component import getUtility
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from ZPublisher.BaseRequest import DefaultPublishTraverse

import decimal
import logging


PloneLocalesFactory = MessageFactory("plonelocales")

log = logging.getLogger(__name__)

grok.templatedir("templates")


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
        """ We always open the tool on the "Start" page.
            Formerly, we would jump to the first question. Since the Start
            page is now much more important, it is also used when a session
            gets resumed.
        """
        survey = aq_inner(self.context)
        if redirectOnSurveyUpdate(self.request):
            return

        self.request.response.redirect(
            "%s/start?initial_view=1" % survey.absolute_url()
        )


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
        self.next_url = None
        if redirectOnSurveyUpdate(self.request):
            return
        self.survey = survey = aq_parent(aq_inner(self.context))
        question = FindFirstQuestion(filter=self.question_filter)
        if question is not None:
            self.next_url = QuestionURL(
                survey, question, phase="identification"
            )
            self.tree = getTreeData(self.request, question)

    @property
    def extra_text(self):
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        have_extra = settings.get('extra_text_identification', False)
        if not have_extra:
            return None
        lang = getattr(self.request, 'LANGUAGE', 'en')
        # Special handling for Flemish, for which LANGUAGE is "nl-be". For
        # translating the date under plone locales, we reduce to generic "nl".
        # For the specific oira translation, we rewrite to "nl_BE"
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        return translate(
            _(u"extra_text_identification", default=u""), target_language=lang
        )


class ActionPlan(grok.View):
    """Survey action plan start page.

    This view shows the introduction text for the action plan phase.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a
    :py:class:`PathGhost` object for the *actionplan* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("actionplan")
    grok.name("index_html")

    # The question filter will find modules AND risks
    question_filter = model.ACTION_PLAN_FILTER
    # The risk filter will only find risks
    risk_filter = model.RISK_PRESENT_OR_TOP5_FILTER

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return
        self.survey = survey = aq_parent(aq_inner(self.context))
        # We fetch the first actual risk, so that we can jump directly to it.
        question = FindFirstQuestion(filter=self.risk_filter)
        if question is not None:
            # We also fetch the first module, so that we can properly build the
            # tree: Open at the first module, but with no risk being selected
            module = FindFirstQuestion(filter=self.question_filter)
            self.next_url = QuestionURL(survey, question, phase="actionplan")
            self.tree = getTreeData(
                self.request,
                module,
                filter=self.question_filter,
                phase="actionplan"
            )
        else:
            self.next_url = None

    def __call__(self):
        ''' Render the page only if the user has edit rights,
        otherwise redirect to the start page of the session.
        '''
        if self.context.restrictedTraverse('webhelpers').can_edit_session():
            return super(ActionPlan, self).__call__()
        return self.request.response.redirect(
            self.context.aq_parent.absolute_url() + '/@@start'
        )


class _StatusHelper(object):

    COUNTRIES_WITHOUT_HIGH_RISKS = [
        'it',
    ]

    @property
    @memoize
    def sql_session(self):
        return Session()

    @property
    @memoize_contextless
    def preferred_language(self):
        return api.portal.get_tool('portal_languages').getPreferredLanguage()

    def module_query(self, sessionid, optional_modules):
        if optional_modules:
            case_clause = case([
                (
                    sql.and_(
                        model.SurveyTreeItem.profile_index != -1,
                        model.SurveyTreeItem.zodb_path.in_(optional_modules)
                    ), func.substr(model.SurveyTreeItem.path, 1, 6)
                ),
                (
                    sql.and_(
                        model.SurveyTreeItem.profile_index == -1,
                        model.SurveyTreeItem.zodb_path.in_(optional_modules)
                    ), func.substr(model.SurveyTreeItem.path, 1, 3) +
                    '000-profile'
                ),
                (
                    sql.and_(
                        model.SurveyTreeItem.profile_index != -1,
                        model.SurveyTreeItem.depth < 2
                    ), func.substr(model.SurveyTreeItem.path, 1, 3)
                ),
            ])
        else:
            case_clause = case([
                (
                    sql.and_(
                        model.SurveyTreeItem.profile_index != -1,
                        model.SurveyTreeItem.depth < 2
                    ), func.substr(model.SurveyTreeItem.path, 1, 3)
                ),
            ])

        query = self.sql_session.query(case_clause.label('module')).filter(
            sql.and_(
                model.SurveyTreeItem.session_id == sessionid,
                model.SurveyTreeItem.type == 'module'
            )
        ).group_by('module').order_by('module')
        return query

    def slicePath(self, path):
        while path:
            yield path[:3].lstrip("0")
            path = path[3:]

    def getModulePaths(self):
        """ Return a list of all the top-level modules belonging to this survey.
        """
        session_id = self.session.id
        if not session_id:
            return []
        profile = extractProfile(self.request.survey, SessionManager.session)
        module_query = self.module_query(
            sessionid=session_id, optional_modules=profile.keys()
        )
        module_res = module_query.all()
        modules_and_profiles = {}
        for row in module_res:
            if row.module is not None:
                if row.module.find('profile') > 0:
                    path = row.module[:3]
                    modules_and_profiles[path] = 'profile'
                else:
                    modules_and_profiles[row[0]] = ''
        module_paths = [m.module for m in module_res if m.module is not None]
        module_paths = modules_and_profiles.keys()
        module_paths = sorted(module_paths)
        self.modules_and_profiles = modules_and_profiles
        return module_paths

    def getModules(self):
        """ Return a list of dicts of all the top-level modules and locations
            belonging to this survey.
        """
        sql_session = self.sql_session
        session_id = self.session.id
        module_paths = self.getModulePaths()
        base_url = "%s/identification" % self.request.survey.absolute_url()
        parent_node = orm.aliased(model.Module)
        titles = dict(
            sql_session.query(
                model.Module.path, model.Module.title
            ).filter(model.Module.session_id == session_id).filter(
                model.Module.path.in_(module_paths)
            )
        )

        location_titles = dict(
            sql_session.query(
                model.Module.path, parent_node.title
            ).filter(model.Module.session_id == session_id).filter(
                model.Module.path.in_(module_paths)
            ).filter(
                sql.and_(
                    parent_node.session_id == session_id,
                    parent_node.depth < model.Module.depth,
                    model.Module.path.like(parent_node.path + "%")
                )
            )
        )
        modules = {}
        toc = {}
        title_custom_risks = utils.get_translated_custom_risks_title(
            self.request
        )

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
                if self.modules_and_profiles[path] == 'profile':
                    continue
            # sub-module (location) or location container
            else:
                if path in location_titles:
                    title = u"{0} - {1}".format(
                        location_titles[path], titles[path]
                    )
                    toc[path[:3]]['locations'].append({
                        'path': path,
                        'title': titles[path],
                        'number': number,
                    })
                else:
                    log.warning(
                        "Status: found a path for a submodule {0} for which "
                        "there's no location title.".format(path)
                    )
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
        global request
        request = self.request
        if not len(module_paths):
            return []
        sql_session = self.sql_session
        session_id = self.session.id
        # First, we need to compute the actual module paths, making sure that
        # skipped optional modules are excluded
        # This means top-level module paths like 001 or 001002 can be replaced
        # by several sub-modules paths like 001002, 001003 and 001002001
        path_clause = [
            model.SurveyTreeItem.path.like('{}%'.format(mp))
            for mp in module_paths
        ]

        module_query = sql_session.query(model.SurveyTreeItem).filter(
            sql.and_(
                model.SurveyTreeItem.session_id == session_id,
                model.SurveyTreeItem.type == 'module', sql.or_(*path_clause)
            )
        ).order_by(model.SurveyTreeItem.path)

        module_res = module_query.all()
        modules_by_path = {m.path: m for m in module_res}

        def nodes(modules):
            global use_nodes, s_paths
            use_nodes = []
            s_paths = sorted(modules, key=lambda x: x.path)
            # In case of repeatable profile questions, the top-level module
            # path will be 6 digits long.
            top_nodes = [
                elem for elem in s_paths if (
                    len(elem.path) == 3 or
                    (len(elem.path) == 6 and elem.path[:3] not in s_paths)
                ) and not elem.skip_children
            ]

            def use_node(elem):
                # Recursively find the nodes that are not disabled
                global use_nodes
                # Skip this elem?
                # If this is an optional module, check the "postponed" flag.
                # As long as the optional question has not been answered, skip
                # showing its children.
                # Only a "Yes" answer on the module will be considered as "do
                # not skip children"
                zodb_elem = request.survey.restrictedTraverse(
                    elem.zodb_path.split('/')
                )
                if getattr(zodb_elem, 'optional', False):
                    if elem.postponed in (True, None) or elem.skip_children:
                        return
                children = [
                    x for x in s_paths if x.path.startswith(elem.path)
                    and len(x.path) == len(elem.path) + 3
                ]
                if children:
                    for child in children:
                        use_node(child)
                else:
                    use_nodes.append(elem.path)

            for elem in top_nodes:
                use_node(elem)
            ret = []
            # Here we make sure that only the longest paths of sub-modules
            # are used, but not the parents. Example
            # (001, 002, 001001, 001003) will be turned into
            # (001001, 001003, 002), since the parent 001 contains sub-modules,
            # and some of those might have been de-selected, like 001002
            for elem in sorted(use_nodes, reverse=True):
                if not [x for x in ret if x.startswith(elem)]:
                    ret.append(elem)
            return ret

        filtered_module_paths = nodes(tuple(module_res))

        child_node = orm.aliased(model.Risk)
        risks = sql_session.query(model.Module, model.Risk).filter(
            sql.and_(
                model.Module.session_id == session_id,
                model.Module.path.in_(filtered_module_paths),
                sql.and_(
                    child_node.session_id == model.Module.session_id,
                    child_node.depth > model.Module.depth,
                    child_node.path.like(model.Module.path + "%")
                )
            )
        ).join((
            model.Risk,
            sql.and_(
                model.Risk.path.startswith(model.Module.path),
                model.Risk.session_id == session_id
            )
        )).order_by(model.Risk.path)

        def _module_path(path):
            # Due to the extended query above that replaces top-module paths
            # with sub-module paths (if present), we need to cut back the path
            # under which we store each risk back to the original top-level
            # module path
            for mp in module_paths:
                if path.startswith(mp):
                    return mp

        filtered_risks = []
        for (module, risk) in risks.all():
            if risk.identification != 'n/a':
                module_path = _module_path(module.path)
                # And, since we might have truncated the path to represent
                # the top-level module, we also need to get the corresponding
                # module object.
                module = modules_by_path[module_path]
                filtered_risks.append((module, risk))
        return filtered_risks

    def as_decimal(self, num):
        return decimal.Decimal(num)

    @property
    @memoize
    def show_high_risks(self):
        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                if obj.id in self.COUNTRIES_WITHOUT_HIGH_RISKS:
                    return False
        return True


class Status(grok.View, _StatusHelper):
    """Show survey status information.
    """
    grok.context(ISurvey)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("status")

    def __init__(self, context, request):
        super(Status, self).__init__(context, request)

        def default_risks_by_status():
            return {
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
                target_language=date_lang,
            ), now.strftime('%Y')
        )
        self.label_page = translate(
            _(u"label_page", default=u"Page"), target_language=lang
        )
        self.label_page_of = translate(
            _(u"label_page_of", default=u"of"), target_language=lang
        )
        self.session = SessionManager.session
        if (
            self.session is not None and self.session.title != (
                callable(getattr(self.context, 'Title', None))
                and self.context.Title() or ''
            )
        ):
            self.session_title = self.session.title
        else:
            self.session_title = None

    def getStatus(self):
        """ Gather a list of the modules and locations in this survey as well
            as data around their state of completion.
        """
        session = Session()
        self.session = SessionManager.session
        total_ok = 0
        total_with_measures = 0
        modules = self.getModules()
        filtered_risks = self.getRisks([m['path'] for m in modules.values()])
        for (module, risk) in filtered_risks:
            module_path = module.path
            has_measures = False
            if risk.identification in ['yes', 'n/a']:
                total_ok += 1
                modules[module_path]['ok'] += 1
            elif risk.identification == 'no':
                measures = session.query(
                    model.ActionPlan.id
                ).filter(model.ActionPlan.risk_id == risk.id)
                if measures.count():
                    has_measures = True
                    modules[module_path]['risk_with_measures'] += 1
                    total_with_measures += 1
                else:
                    modules[module_path]['risk_without_measures'] += 1
            elif risk.postponed:
                modules[module_path]['postponed'] += 1
            else:
                modules[module_path]['todo'] += 1

            self.add_to_risk_list(risk, module_path, has_measures=has_measures)

        for key, m in modules.items():
            if m['ok'] + m['postponed'] + m['risk_with_measures'] + m[
                'risk_without_measures'
            ] + m['todo'] == 0:
                del modules[key]
                del self.tocdata[key]
        self.percentage_ok = (
            not len(filtered_risks) and 100
            or int((total_ok + total_with_measures) /
                   Decimal(len(filtered_risks)) * 100)
        )
        self.status = modules.values()
        self.status.sort(key=lambda m: m["path"])
        self.toc = self.tocdata.values()
        self.toc.sort(key=lambda m: m["path"])

    def add_to_risk_list(self, risk, module_path, has_measures=False):
        if self.is_skipped_from_risk_list(risk):
            return

        risk_title = self.get_risk_title(risk)

        base_url = "%s/actionplan" % self.request.survey.absolute_url()
        url = '%s/%s' % (base_url, '/'.join(self.slicePath(risk.path)))

        if risk.identification != 'no':
            status = risk.postponed and 'postponed' or 'todo'
            self.risks_by_status[module_path]['possible'][status].append({
                'title': risk_title,
                'path': url
            })
        else:
            self.risks_by_status[module_path
                                 ]['present'][risk.priority or 'low'].append({
                                     'title': risk_title,
                                     'path': url,
                                     'has_measures': has_measures
                                 })

    def get_risk_title(self, risk):
        if risk.is_custom_risk:
            risk_title = risk.title
        else:
            risk_obj = self.request.survey.restrictedTraverse(
                risk.zodb_path.split('/')
            )
            if not risk_obj:
                return
            if risk.identification == 'no':
                risk_title = risk_obj.problem_description
            else:
                risk_title = risk.title
        return risk_title

    def is_skipped_from_risk_list(self, risk):
        if risk.priority == "high":
            if risk.identification != 'no':
                if risk.risk_type not in ['top5']:
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
    query = (
        Session.query(
            model.SurveyTreeItem.id
        ).filter(model.SurveyTreeItem.session_id == session_id
                 ).filter(model.SurveyTreeItem.path == sql.bindparam('path'))
    )
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
        'report': IReportPhaseSkinLayer,
    }

    countries = {
        'it': {
            'identification': IItalyIdentificationPhaseSkinLayer,
            'customization': IItalyCustomizationPhaseSkinLayer,
            'evaluation': IItalyEvaluationPhaseSkinLayer,
            'actionplan': IItalyActionPlanPhaseSkinLayer,
            'report': IItalyReportPhaseSkinLayer,
        }
    }

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
                session = Session.query(SessionManager.model).get(sid)
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
                aq_parent(aq_parent(self.context)).absolute_url(), lock=True
            )
            return self.context

        if name not in self.phases:
            return super(SurveyPublishTraverser, self)\
                    .publishTraverse(request, name)

        # Decorate the request with the right skin layer and add to the aq path

        # Some countries need to be marked specially. Check if this needs to be
        # done, and decorate the reques accordingly if yes.
        special = False
        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                if obj.id in self.countries:
                    special = True
                    directlyProvides(
                        request, self.countries[obj.id][name],
                        *directlyProvidedBy(request)
                    )
                    break
        if not special:
            directlyProvides(
                request, self.phases[name], *directlyProvidedBy(request)
            )
        self.context = PathGhost(name).__of__(self.context)

        session = SessionManager.session
        tree_id = find_sql_context(
            session.id, request['TraversalRequestNameStack']
        )
        if tree_id is not None:
            return build_tree_aq_chain(self.context, tree_id)

        # No SQL based traversal possible, return the existing context with the
        # new skin layer applied
        return self.context
