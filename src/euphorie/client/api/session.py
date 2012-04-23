from five import grok
from euphorie.content.survey import ISurvey
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.client.utils import HasText


def get_survey(request, path):
    client = request.client
    try:
        survey = client.restrictedTraverse(path.split('/'))
        if ISurvey.providedBy(survey):
            return survey
    except KeyError:
        pass
    return None


class View(JsonView):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('index_html')

    def GET(self):
        info = {'id': self.context.id,
                'type': 'session',
                'created': self.context.created.isoformat(),
                'modified': self.context.modified.isoformat(),
                'title': self.context.title,
               }
        survey = get_survey(self.request, self.context.zodb_path)
        if HasText(survey.introduction):
            info['introduction'] = survey.introduction
        return info
