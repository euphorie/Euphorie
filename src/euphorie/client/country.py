# coding=utf-8
"""
Country
-------

The main view after login, to list existing sessions, start new sessions,
delete & rename sessions

URL: https://client-oiranew.syslab.com/eu
"""

from .. import MessageFactory as _
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from anytree import NodeMixin
from anytree.node.util import _repr
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import SurveySession
from euphorie.client.sector import IClientSector
from euphorie.client.session import SessionManager
from euphorie.content.survey import ISurvey
from five import grok
from plone import api
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.statusmessages.interfaces import IStatusMessage
from sqlalchemy.orm import object_session
from z3c.form import button
from z3c.saconfig import Session
from zope import schema
from zope.interface import directlyProvides
from zope.interface import implements
from zope.interface import Interface

import logging
import six


grok.templatedir("templates")

log = logging.getLogger(__name__)


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


class IClientCountry(form.Schema, IBasic):
    """Country grouping in the online client.
    """


class ClientCountry(dexterity.Container):
    implements(IClientCountry)

    country_type = None


class View(grok.View):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.template("sessions")

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
        if not self.account.group:
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
            title=group.short_name or group.group_id,
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
        return Node(
            session,
            parent=self.get_survey_node(survey, group),
            title=session.title,
            type='session',
        )

    @memoize
    def get_sessions_tree_root(self):
        ''' Given some sessions create a tree
        '''
        scope = self.request.get('scope')
        if scope == 'all':
            sessions = self.account.sessions + self.account.acquired_sessions
        else:
            sessions = self.account.sessions
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
            log.error('Tried to start invalid survey %r' % info.get('survey'))
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

    def update(self):
        utils.setLanguage(self.request, self.context)
        reply = self.request.form
        action = reply.get('action')
        if action == "new":
            self._NewSurvey(reply)
        elif action == "continue":
            self._ContinueSurvey(reply)
        self._updateSurveys()


class CreateSession(View):
    """View name: @@new-session.html
    """
    grok.context(Interface)
    grok.name("new-session.html")
    grok.template("new-session")


class ConfirmationDeleteSession(grok.View):
    """View name: @@confirmation-delete-session.html
    """
    grok.context(IClientCountry)
    grok.name("confirmation-delete-session.html")
    grok.layer(IClientSkinLayer)
    grok.template("confirmation-delete-session")

    def __call__(self, *args, **kwargs):
        try:
            self.session_id = int(self.request.get("id"))
        except (ValueError, TypeError):
            raise KeyError("Invalid session id")
        user = getSecurityManager().getUser()
        session = object_session(user).query(SurveySession)\
                .filter(SurveySession.account == user)\
                .filter(SurveySession.id == self.session_id).first()
        if session is None:
            raise KeyError("Unknown session id")
        self.session_title = session.title
        return super(ConfirmationDeleteSession, self).__call__(*args, **kwargs)


class DeleteSession(grok.View):
    """View name: @@delete-session
    """
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("delete-session")

    def render(self):
        session = Session()
        ss = session.query(SurveySession).get(self.request.form["id"])
        if ss is not None:
            flash = IStatusMessage(self.request).addStatusMessage
            flash(
                _(
                    u"Session `${name}` has been deleted.",
                    mapping={
                        "name": getattr(ss, 'title')
                    }
                ), "success"
            )
            session.delete(ss)
        self.request.response.redirect(self.context.absolute_url())


class RenameSessionSchema(form.Schema):
    title = schema.TextLine(required=False)


class RenameSession(form.SchemaForm):
    """View name: @@rename-session
    """
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("rename-session")
    grok.template("rename-session")
    form.wrap(False)

    schema = RenameSessionSchema

    def getContent(self):
        try:
            session_id = int(self.request.get("id"))
        except (ValueError, TypeError):
            raise KeyError("Invalid session id")
        user = getSecurityManager().getUser()
        session = (
            object_session(user).query(SurveySession)
            .filter(SurveySession.account == user)
            .filter(SurveySession.id == session_id).first()
        )
        if session is None:
            raise KeyError("Unknown session id")
        self.original_title = session.title
        directlyProvides(session, RenameSessionSchema)
        return session

    @button.buttonAndHandler(_(u"Save"))
    def handleSave(self, action):
        (data, errors) = self.extractData()
        if errors:
            return
        if data["title"]:
            flash = IStatusMessage(self.request).addStatusMessage
            self.getContent().title = data['title']
            flash(
                _(
                    u"Session title has been changed to ${name}",
                    mapping={
                        "name": data["title"]
                    }
                ), "success"
            )
        came_from = self.request.form.get("came_from")
        if isinstance(came_from, list):
            # If came_from is both in the querystring and the form data
            came_from = came_from[0]
        if came_from:
            self.request.response.redirect(came_from)
        else:
            self.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        self.response.redirect(self.context.absolute_url())
