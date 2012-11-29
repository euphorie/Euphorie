from Acquisition import aq_inner
from five import grok
from z3c.saconfig import Session
from euphorie.content.survey import ISurvey
from euphorie.ghost import PathGhost
from ..model import SurveySession
from . import JsonView
from ..profile import set_session_profile
from ..session import create_survey_session
from .session import View as SessionView
from .session import get_survey


class Sessions(PathGhost):
    """Virtual container for all user data."""

    def __init__(self, id, request, account):
        super(Sessions, self).__init__(id, request)
        self.account = account

    def __getitem__(self, key):
        try:
            survey_session = Session.query(SurveySession)\
                    .filter(SurveySession.id == int(key))\
                    .filter(SurveySession.account == self.account)\
                    .first()
            self.request.survey_session = survey_session
            survey = get_survey(self.request, survey_session.zodb_path)
            if survey is not None:
                self.request.survey = survey
                if survey.language is not None:
                    self.request['LANGUAGE'] = survey.language
                    binding = self.request.get('LANGUAGE_TOOL', None)
                    if binding is not None:
                        binding.LANGUAGE = survey.language
                return survey_session.__of__(self)
        except (AttributeError, TypeError, ValueError):
            pass

        raise KeyError(key)


class View(JsonView):
    grok.context(Sessions)
    grok.require('zope2.View')
    grok.name('index_html')

    def sessions(self):
        return [{'id': session.id,
                 'title': session.title,
                 'created': session.modified.isoformat(),
                 'modified': session.modified.isoformat()}
                for session in self.context.account.sessions]

    def do_GET(self):
        return {'sessions': self.sessions()}

    def do_POST(self):
        try:
            survey = self.request.client.restrictedTraverse(
                    self.input['survey'].split('/'))
            if not ISurvey.providedBy(survey):
                raise TypeError('Not a survey')
        except (KeyError, TypeError):
            return {'type': 'error',
                    'message': 'Unknown survey'}

        title = self.input.get('title', survey.title)
        survey_session = create_survey_session(title, survey)
        survey_session = survey_session.__of__(aq_inner(self.context))
        view = SessionView(survey_session, self.request)
        response = view.do_GET()
        survey_session_url = survey_session.absolute_url()
        if survey.ProfileQuestions():
            response['next-step'] = '%s/profile' % survey_session_url
        else:
            survey_session = set_session_profile(survey, survey_session, {})
            response['next-step'] = '%s/identification' % survey_session_url
        return response
