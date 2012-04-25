from five import grok
from euphorie.content.survey import ISurvey
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.client.utils import HasText
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.survey import Evaluation as BaseEvaluation
from euphorie.client.survey import ActionPlan as BaseActionPlan


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
                'survey': self.context.zodb_path,
                'created': self.context.created.isoformat(),
                'modified': self.context.modified.isoformat(),
                'title': self.context.title,
               }
        survey = get_survey(self.request, self.context.zodb_path)
        if HasText(survey.introduction):
            info['introduction'] = survey.introduction
        return info


class Identification(JsonView):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('identification')

    phase = 'identification'
    question_filter = None

    def GET(self):
        info = View(self.context, self.request).GET()
        info['phase'] = self.phase
        risk = FindFirstQuestion(self.context, self.question_filter)
        if risk is not None:
            info['next-step'] = '%s/%s/%s' % \
                    (self.context.absolute_url(), 
                            '/'.join(risk.short_path), self.phase)
        return info


class Evaluation(Identification):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('evaluation')

    phase = 'evaluation'
    question_filter = BaseEvaluation.question_filter


class ActionPlan(Identification):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    question_filter = BaseActionPlan.question_filter
