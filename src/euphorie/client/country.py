# coding=utf-8
"""
Country
-------

The main view after login, to list existing sessions, start new sessions,
delete & rename sessions

URL: https://client-oiranew.syslab.com/eu
"""

import logging
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl import getSecurityManager
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.model import SurveySession
from euphorie.client.sector import IClientSector
from euphorie.content.survey import ISurvey
from euphorie.client.session import SessionManager
from five import grok
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from Products.statusmessages.interfaces import IStatusMessage
from sqlalchemy.orm import object_session
from z3c.form import button
from z3c.saconfig import Session
from zope import schema
from zope.interface import directlyProvides
from zope.interface import implements
from zope.interface import Interface


from .. import MessageFactory as _


grok.templatedir("templates")

log = logging.getLogger(__name__)


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

    def sessions(self):
        """Return a list of all sessions for the current user. For each
        session a dictionary is returned with the following keys:

        * `id`: unique identifier for the session
        * `title`: session title
        * `modified`: timestamp of last session modification
        """
        account = getSecurityManager().getUser()
        result = []
        client = aq_parent(aq_inner(self.context))
        for session in account.sessions:
            try:
                client.restrictedTraverse(session.zodb_path.split("/"))
                result.append({"id": session.id,
                               "title": session.title,
                               "modified": session.modified,
                               })
            except KeyError:
                pass
        result.sort(key=lambda s: s['modified'], reverse=True)
        return result

    def _updateSurveys(self):
        self.surveys = []
        self.obsolete_surveys = []

        language = self.request.locale.id.language
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
                info = {"id": "%s/%s" % (sector.id, survey.id),
                        "title": survey.title}
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
        self.request.response.redirect("%s/start?initial_view=1" % survey.absolute_url())

    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session = Session.query(model.SurveySession).get(info["session"])
        SessionManager.resume(session)
        survey = self.request.client.restrictedTraverse(str(session.zodb_path))
        self.request.response.redirect("%s/resume?initial_view=1" % survey.absolute_url())

    def update(self):
        utils.setLanguage(self.request, self.context)
        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply["action"] == "new":
                self._NewSurvey(reply)
            elif reply["action"] == "continue":
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
            flash(_(u"Session `${name}` has been deleted.",
                    mapping={"name": getattr(ss, 'title')}), "success")
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
        session = object_session(user).query(SurveySession)\
                .filter(SurveySession.account == user)\
                .filter(SurveySession.id == session_id).first()
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
            flash(_(u"Session title has been changed to ${name}",
                mapping={"name": data["title"]}), "success")
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
