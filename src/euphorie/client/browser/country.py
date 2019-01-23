# coding=utf-8
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from anytree import NodeMixin
from anytree.node.util import _repr
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.country import IClientCountry
from euphorie.client.model import get_current_account
from euphorie.client.model import Group
from euphorie.client.model import Module
from euphorie.client.model import Risk
from euphorie.client.model import SurveySession
from euphorie.client.model import SurveyTreeItem
from euphorie.client.sector import IClientSector
from euphorie.client.session import SessionManager
from euphorie.content.survey import ISurvey
from logging import getLogger
from plone import api
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from sqlalchemy.orm import object_session
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent

import six


logger = getLogger(__name__)


class Node(NodeMixin):

    def __init__(self, context, parent=None, **kwargs):
        self.__dict__.update(kwargs)
        self.context = context
        self.parent = parent

    @property
    def groups(self):
        ''' Assume childrens are groups and return them sorted by title
        '''
        return sorted(
            self.children,
            key=lambda x: x.title,
        )

    @property
    def sessions(self):
        ''' Assume childrens are sessions and return them sorted by
        reversed modification date
        '''
        return sorted(
            self.children,
            key=lambda x: x.context.modified,
            reverse=True,
        )

    @property
    def survey_templates(self):
        ''' Return all children that are survey_templates, sorted by title
        '''
        return sorted(
            [item for item in self.children if item.type == 'survey_template'],
            key=lambda x: x.title.lower(),
        )

    @property
    def categories(self):
        ''' Return all children that are categories, sorted by title
        '''
        return sorted(
            [item for item in self.children if item.type == 'category'],
            key=lambda x: x.title,
        )

    def __repr__(self):
        args = [
            "%r" % self.separator.join(
                [""] + [repr(node.context) for node in self.path]
            )
        ]
        return _repr(self, args=args, nameblacklist=["context"])


class SessionsView(BrowserView):

    # switch from radio buttons to dropdown above this number of tools
    tools_threshold = 12

    @property
    @memoize
    def my_context(self):
        if IClientCountry.providedBy(self.context):
            return "country"
        elif ISurvey.providedBy(self.context):
            return "survey"

    @property
    @memoize_contextless
    def portal(self):
        ''' The currenttly authenticated account
        '''
        return api.portal.get()

    @property
    @memoize_contextless
    def account(self):
        ''' The currenttly authenticated account
        '''
        return model.get_current_account()

    @property
    @memoize_contextless
    def scope_options(self):
        ''' We have the possibility to display only the sessions
        that were made by this user or all the accessible sessions through
        the group ownership
        '''
        account = self.account
        if not account or not account.group:
            return []
        options = [
            {
                'value': 'mine',
                'label': _('Show my risk assessments only'),
            },
            {
                'value': 'all',
                'label': _('Show all risk assessments'),
            },
        ]
        selected = self.request.get('scope')
        for option in options:
            if option['value'] == selected:
                option['selected'] = 'selected'
        return options

    @memoize
    def get_survey_by_path(self, zodb_path):
        return self.context.restrictedTraverse(
            six.binary_type(zodb_path), None
        )

    @property
    @memoize
    def sessions_root(self):
        return Node(None, title='', type='root')

    @memoize
    def get_group_node(self, group):
        ''' Get the Node for this group.
        '''
        if group is None:
            # Everything is grouped under the sessions_root node
            return self.sessions_root
        return Node(
            group,
            parent=self.get_group_node(group.parent),
            title=group.fullname,
            type='department',
        )

    @memoize
    def get_survey_node(self, survey, group):
        ''' Get a node for this survey, it might be in a group
        '''
        return Node(
            survey,
            parent=self.get_group_node(group),
            title=survey.title,
            type='tool',
        )

    @memoize
    def get_session_node(self, session):
        ''' Get a node for this session
        '''
        group = session.group
        survey = self.get_survey_by_path(session.zodb_path)
        if not survey:
            return
        return Node(
            session,
            parent=self.get_survey_node(survey, group),
            title=session.title,
            type='session',
        )

    def filter_valid_sessions(self, sessions):
        return [
            session for session in sessions
            if self.get_survey_by_path(session.zodb_path)
        ]

    @memoize
    def get_sessions(self):
        ''' Given some sessions create a tree
        '''
        scope = self.request.get('scope')
        account = self.account
        if not account:
            sessions = []
        elif scope == 'all':
            sessions = self.account.sessions + self.account.acquired_sessions
        else:
            sessions = self.account.sessions

        return self.filter_valid_sessions(sessions)

    @memoize
    def get_ordered_sessions(self):
        ''' Given some sessions create a tree
        '''
        return sorted(
            self.get_sessions(),
            key=lambda x: x.modified,
            reverse=True
        )

    @memoize
    def get_sessions_tree_root(self):
        ''' Given some sessions create a tree
        '''
        sessions = self.get_sessions()
        map(self.get_session_node, sessions)
        return self.sessions_root

    # Here, we assemble the list of available tools for starting a new session

    @property
    @memoize
    def survey_templates_root(self):
        return Node(None, title='', type='root')

    @memoize
    def get_survey_category_node(self, category):
        if category is None:
            # Everything is grouped under the survey_templates_root node
            return self.survey_templates_root
        return Node(
            category,
            parent=self.get_survey_category_node(None),
            title=category,
            type='category'
        )

    @memoize
    def get_survey_template_node(self, survey_item):
        category, survey, id = survey_item
        return Node(
            survey,
            parent=self.get_survey_category_node(category),
            title=survey.title,
            type='survey_template',
            id=id,
        )

    @memoize
    def get_survey_templates_tree_root(self):
        survey_items = self.get_survey_templates()
        map(self.get_survey_template_node, survey_items)
        return self.survey_templates_root

    @memoize
    def get_survey_templates(self):
        # This number might be higher than the actual amount of survey
        # templates, since some might appear under more than one category.
        self.template_count = 0
        # this is a list of tuples of the form
        # (category name, survey object, survey id)
        survey_items = []
        language = self.request.locale.id.language or ''
        for sector in aq_inner(self.context).values():
            if not IClientSector.providedBy(sector):
                continue

            for survey in sector.values():
                if not ISurvey.providedBy(survey):
                    continue
                if getattr(survey, "preview", False):
                    continue
                if survey.language and survey.language != language and not \
                        survey.language.strip().startswith(language):
                    continue
                if getattr(survey, 'obsolete', False):
                    continue
                categories = getattr(survey, 'tool_category', None)
                id = "%s/%s" % (sector.id, survey.id)
                if not isinstance(categories, list):
                    categories = [categories]
                if not categories:
                    categories = [None]
                for category in categories:
                    survey_items.append((category, survey, id))
                    self.template_count += 1
        return sorted(
            survey_items,
            key=lambda x: (x[0], x[1].title)
        )

    def _updateSurveys(self):
        self.surveys = []
        self.obsolete_surveys = []

        language = self.request.locale.id.language or ''
        for sector in aq_inner(self.context).values():
            if not IClientSector.providedBy(sector):
                continue

            for survey in sector.values():
                if not ISurvey.providedBy(survey):
                    continue
                if getattr(survey, "preview", False):
                    continue
                if survey.language and survey.language != language and not \
                        survey.language.strip().startswith(language):
                    continue
                info = {
                    "id": "%s/%s" % (sector.id, survey.id),
                    "title": survey.title
                }
                if getattr(survey, 'obsolete', False):
                    # getattr needed for surveys which were published before
                    # the obsolete flag added.
                    self.obsolete_surveys.append(info)
                else:
                    self.surveys.append(info)
        self.surveys.sort(key=lambda s: s["title"])
        self.obsolete_surveys.sort(key=lambda s: s["title"])

    def _NewSurvey(self, info, account=None):
        """Utility method to start a new survey session."""
        context = aq_inner(self.context)
        survey = info.get("survey")
        survey = context.restrictedTraverse(survey)
        if not ISurvey.providedBy(survey):
            logger.error(
                'Tried to start invalid survey %r',
                info.get('survey'),
            )
            # Things are sufficiently messed up at this point that rendering
            # breaks, so trigger a redirect to the same URL again.
            self.request.response.redirect(context.absolute_url())
            return
        title = info.get("title", u"").strip()
        if not title:
            title = survey.Title()

        SessionManager.start(title=title, survey=survey, account=account)
        self.request.response.redirect(
            "%s/start?initial_view=1&new_session=1" % survey.absolute_url()
        )

    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session = Session.query(model.SurveySession).get(info["session"])
        SessionManager.resume(session)
        survey = self.request.client.restrictedTraverse(
            six.binary_type(session.zodb_path)
        )
        extra = ""
        if info.get('new_clone', None):
            extra = "&new_clone=1"
        self.request.response.redirect(
            "%s/resume?initial_view=1%s" % (survey.absolute_url(), extra)
        )

    def __call__(self):
        if not self.account:
            raise Unauthorized()

        utils.setLanguage(self.request, self.context)
        reply = self.request.form
        action = reply.get('action')
        if action == "new":
            if self.my_context == 'survey':
                reply['survey'] = "/".join(self.context.getPhysicalPath())
            return self._NewSurvey(reply)
        elif action == "continue":
            return self._ContinueSurvey(reply)
        self._updateSurveys()
        return super(SessionsView, self).__call__()


class SessionBrowserNavigator(SessionsView):
    ''' Logic to build the navigator for the sessions
    '''

    group_model = Group
    no_splash = True

    @property
    @memoize
    def groupid(self):
        return self.request.get('groupid')

    @memoize
    def get_root_group(self):
        ''' Return the group that is the root of the navigation tree
        '''
        groupid = self.groupid
        if not groupid:
            return
        base_query = (
            Session
            .query(self.group_model)
            .order_by(self.group_model.short_name)
        )
        return (
            base_query
            .filter(self.group_model.group_id == groupid)
            .one()
        )

    @property
    @memoize
    def searchable_text(self):
        ''' Return the text we need to search in postgres
        already surrounded with '%'
        Allow a minimum size of 3 characters to reduce the load.
        '''
        searchable_text = self.request.get('SearchableText')
        if not isinstance(searchable_text, six.string_types):
            return ''
        if len(searchable_text) < 3:
            return ''
        return u'%{}%'.format(safe_unicode(searchable_text))

    def get_tools_tree(self, zodb_path=None):
        ''' Return a dict like structure to render the leaf sessions,
        something like:

        {
            'tool': [<SurveySession>, ...],
            ...
        }
        Optionally, we can pass in zodb_path, to filter for tools that match
        this path
        '''
        sessions = self.leaf_sessions()
        if not sessions.count():
            return {}
        tools = defaultdict(list)
        for session in sessions:
            # XXX
            # Filter by zodb_path for specific tools
            # if zodb_path and session.zodb_path != zodb_path:
            #     continue
            tool = self.get_survey_by_path(session.zodb_path)
            tools[tool].append(session)

        ordered_tools = OrderedDict()
        for tool in sorted(
            [x for x in tools.keys() if x], key=lambda s: s.title.lower()
        ):
            ordered_tools[tool] = sorted(
                tools[tool], key=lambda s: s.modified, reverse=True)

        return ordered_tools

    @memoize
    def leaf_groups(self, groupid=None):
        """ Nothing to do in main OiRA - to be filled in customer-specific
        packages.
        Here we just return a Query with 0 items.
        """
        base_query = Session.query(SurveySession)
        return base_query.filter(False)

    def leaf_sessions(self):
        ''' The sessions we want to display in the navigation
        '''
        base_query = (
            Session
            .query(SurveySession)
            .order_by(SurveySession.title)
        )
        if self.searchable_text:
            base_query = base_query.filter(
                SurveySession.title.ilike(self.searchable_text)
            )
        account = get_current_account()
        return base_query.filter(SurveySession.account_id == account.id)

    def has_content(self):
        ''' Checks if we have something meaningfull to display
        '''
        if self.leaf_groups().count():
            return True
        if len(self.get_tools_tree()):
            return True
        return False


class ConfirmationDeleteSession(BrowserView):
    """View name: @@confirmation-delete-session
    """

    @property
    @memoize_contextless
    def webhelpers(self):
        return api.content.get_view(
            'webhelpers',
            api.portal.get(),
            self.request,
        )

    @property
    @memoize_contextless
    def session_title(self):
        try:
            self.session_id = int(self.request.get("id"))
        except (ValueError, TypeError):
            raise KeyError("Invalid session id")
        user = getSecurityManager().getUser()
        session = (
            object_session(user)
            .query(SurveySession)
            .filter(SurveySession.id == self.session_id).first()
        )
        if session is None:
            raise KeyError("Unknown session id")
        if not self.webhelpers.can_delete_session(session):
            raise Unauthorized()
        return session.title

    def __call__(self, *args, **kwargs):
        ''' Before rendering check if we can find session title
        '''
        self.session_title
        self.no_splash = True
        return super(ConfirmationDeleteSession, self).__call__(*args, **kwargs)


def sql_clone(obj, skip={}, session=None):
    ''' Clone a sql object avoiding the properties in the skip parameter

    The skip parameter is optional but you probably want to always pass the
    primary key
    '''
    # Never copy the _sa_instance_state attribute
    skip.add('_sa_instance_state')
    params = {
        key: value
        for key, value in obj.__dict__.iteritems()
        if key not in skip
    }
    clone = obj.__class__(**params)
    if session:
        session.add(clone)
    return clone


class CloneSession(BrowserView):
    """View name: @@confirmation-clone-session
    """

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view(
            'webhelpers',
            self.context,
            self.request,
        )

    @property
    @memoize
    def session(self):
        ''' Get the requested session
        '''
        try:
            session_id = int(self.request.get("id"))
        except (ValueError, TypeError):
            raise KeyError("Invalid session id")
        return Session.query(SurveySession).filter(
            SurveySession.id == session_id
        ).one()

    def get_cloned_session(self):
        sql_session = Session
        old_session = self.session
        new_session = sql_clone(
            old_session,
            skip={
                'id',
                'created',
                'modified',
                'last_modifier_id',
                'company',
                'published',
                'group_id',
            },
            session=sql_session,
        )
        lang = getattr(self.request, 'LANGUAGE', 'en')
        new_session.title = u"{}: {}".format(
            translate(
                _('prefix_cloned_title', default=u'COPY'),
                target_language=lang
            ), new_session.title)
        account = self.webhelpers.get_current_account()
        new_session.group = account.group
        new_session.modified = new_session.created = datetime.now()
        new_session.account = account
        if old_session.company:
            new_session.company = sql_clone(
                old_session.company,
                skip={'id', 'session'},
                session=sql_session,
            )

        risk_module_skipped_attributes = {
            'id',
            'session',
            'sql_module_id',
            'parent_id',
            'session_id',
            'sql_risk_id',
            'risk_id',
        }
        module_mapping = {}

        old_modules = (
            sql_session
            .query(Module)
            .filter(SurveyTreeItem.session == old_session)
        )
        for old_module in old_modules:
            new_module = sql_clone(
                old_module,
                skip=risk_module_skipped_attributes,
                session=sql_session,
            )
            module_mapping[old_module.id] = new_module
            new_module.session = new_session

        old_risks = (
            sql_session
            .query(Risk)
            .filter(SurveyTreeItem.session == old_session)
        )
        for old_risk in old_risks:
            new_risk = sql_clone(
                old_risk,
                skip=risk_module_skipped_attributes,
                session=sql_session,
            )
            new_risk.parent_id = module_mapping[old_risk.parent_id].id
            new_risk.session = new_session

            for old_plan in old_risk.action_plans:
                new_plan = sql_clone(
                    old_plan,
                    skip={'id', 'risk_id'},
                    session=sql_session,
                )
                new_plan.risk = new_risk
        notify(ObjectModifiedEvent(new_session))
        return new_session

    def clone(self):
        ''' Clone this session and redirect to the start view
        '''
        new_session = self.get_cloned_session()
        api.portal.show_message(
            _('The risk assessment has been cloned'),
            self.request,
            'success',
        )
        target = '{contexturl}/@@view?action=continue&new_clone=1&session={sessionid}'.format(  # noqa: E501
            contexturl=self.context.absolute_url(),
            sessionid=new_session.id,
        )
        self.request.response.redirect(target)
