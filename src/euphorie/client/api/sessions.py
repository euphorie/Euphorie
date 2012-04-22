from five import grok
from z3c.saconfig import Session
from euphorie.client.survey import PathGhost
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.content.survey import ISurvey


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
            if survey_session is not None:
                client = self.request.client
                survey = client.restrictedTraverse(
                        survey_session.zodb_path.split('/'))
                if ISurvey.providedBy(survey):
                    self.request.survey = survey
                    return survey_session.__of__(self)
        except (KeyError, TypeError, ValueError):
            pass

        raise KeyError(key)


class View(JsonView):
    grok.context(Sessions)
    grok.require('zope2.View')
    grok.name('index_html')

    def sessions(self):
        return [{'id': session.id,
                 'title': session.title,
                 'modified': session.modified.isoformat()}
                for session in self.context.account.sessions]

    def GET(self):
        return {'sessions': self.sessions()}
