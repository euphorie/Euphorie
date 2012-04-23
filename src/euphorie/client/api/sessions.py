from five import grok
from z3c.saconfig import Session
from euphorie.client.survey import PathGhost
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.client.api.session import View as SessionView
from euphorie.client.api.session import get_survey



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
            survey = get_survey(self.request, survey_session.zodb_path)
            if survey is not None:
                self.request.survey = survey
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

    def GET(self):
        return {'sessions': self.sessions()}

    def POST(self):
        try:
            path = self.input['path']
            title = self.input['title']
        except KeyError:
            return {'type': 'error',
                    'message': 'Required data missing'}
        
        survey = self.request.restrictedTraverse(path.split('/'))
        if survey is None:
            return {'type': 'error',
                    'message': 'Unknown survey id'}

        survey_session = SurveySession(
                account=self.context.account,
                title=title,
                zodb_path=path)
        session = Session()
        session.add(survey_session)
        session.flush()
        view = SessionView(survey_session, self.request)
        return view.GET()
