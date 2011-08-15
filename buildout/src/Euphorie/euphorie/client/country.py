import logging
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl import getSecurityManager
from zope.interface import implements
from five import grok
from z3c.saconfig import Session
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.sector import IClientSector
from euphorie.content.survey import ISurvey
from euphorie.client.session import SessionManager

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
        return result

    def surveys(self):
        """Return a list of all available surveys for this country and current
        language. For each survey a dictionary is returned with the following
        keys:

        * `id`: unique identifier for the survey (unique within the country
          only)
        * `title`: title of the survey, includes name of the sector
        """
        language = self.request.locale.id.language
        surveys = []
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

                surveys.append(dict(id="%s/%s" % (sector.id, survey.id),
                                    title=survey.title))

        return sorted(surveys, key=lambda s: s["title"])

    def _NewSurvey(self, info):
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

        SessionManager.start(title=title, survey=survey)
        self.request.response.redirect("%s/start" % survey.absolute_url())

    def _ContinueSurvey(self, info):
        """Utility method to continue an existing session."""
        session = Session.query(model.SurveySession).get(info["session"])
        SessionManager.resume(session)
        survey = self.request.client.restrictedTraverse(str(session.zodb_path))
        self.request.response.redirect("%s/resume" % survey.absolute_url())

    def update(self):
        utils.setLanguage(self.request, self.context)

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply["action"] == "new":
                self._NewSurvey(reply)
            elif reply["action"] == "continue":
                self._ContinueSurvey(reply)


class DeleteSession(grok.CodeView):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("delete-session")

    def render(self):
        session = Session()
        ss = session.query(model.SurveySession).get(self.request.form["id"])
        if ss is not None:
            session.delete(ss)
        self.request.response.redirect(self.context.absolute_url())


class JsonRenameSession(grok.CodeView):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("json-rename-session")

    @utils.jsonify
    def render(self):
        session = Session()
        ss = session.query(model.SurveySession).get(self.request.form["id"])
        if ss is not None:
            ss.title = self.request.form["title"]
        return dict(result="ok")


class JsonDeleteSession(grok.CodeView):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("json-delete-session")

    @utils.jsonify
    def render(self):
        """JSON entry point for session deletion."""
        session = Session()
        ss = session.query(model.SurveySession).get(self.request.form["id"])
        if ss is not None:
            session.delete(ss)
        return dict(result="ok")
