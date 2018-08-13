# coding=utf-8
from Acquisition import aq_inner
from anytree import NodeMixin
from anytree.node.util import _repr
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.country import IClientCountry
from euphorie.client.sector import IClientSector
from euphorie.client.session import SessionManager
from euphorie.content.survey import ISurvey
from logging import getLogger
from plone import api
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.Five import BrowserView
from z3c.saconfig import Session
from zExceptions import Unauthorized

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

    def __repr__(self):
        args = [
            "%r" % self.separator.join(
                [""] + [repr(node.context) for node in self.path]
            )
        ]
        return _repr(self, args=args, nameblacklist=["context"])


class SessionsView(BrowserView):

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
        return sessions

    @memoize
    def get_sessions_tree_root(self):
        ''' Given some sessions create a tree
        '''
        sessions = self.get_sessions()
        map(self.get_session_node, sessions)
        return self.sessions_root

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
            "%s/start?initial_view=1" % survey.absolute_url()
        )

    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session = Session.query(model.SurveySession).get(info["session"])
        SessionManager.resume(session)
        survey = self.request.client.restrictedTraverse(
            six.binary_type(session.zodb_path)
        )
        self.request.response.redirect(
            "%s/resume?initial_view=1" % survey.absolute_url()
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
