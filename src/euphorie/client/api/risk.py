from five import grok
from euphorie.client.utils import HasText
from euphorie.client.model import Risk
from euphorie.client.api import JsonView
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.risk import EvaluationView as BaseEvaluation
from euphorie.client.risk import ActionPlanView as BaseActionPlan


class View(JsonView):
    grok.context(Risk)
    grok.require('zope2.View')
    grok.name('index_html')

    def GET(self):
        self.risk = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split('/'))
        info = {'id': self.context.id,
                'type': 'risk',
                'title': self.risk.title,
                'problem-description': self.risk.problem_description,
                'show-not-applicable': self.risk.show_notapplicable,
                'evaluation-method': self.risk.evaluation_method,
                'present': self.context.identification,
                'priority': self.context.priority,
                'comment': self.context.comment,
                }
        if HasText(self.risk.description):
            info['description'] = self.risk.description
        if HasText(self.risk.legal_reference):
            info['legal-reference'] = self.risk.legal_reference
        if self.risk.evaluation_method == 'calculated':
            info['frequency'] = self.context.frequency
            info['effect'] = self.context.effect
            info['probability'] = self.context.probability
        return info


class Identification(JsonView):
    grok.context(Risk)
    grok.require('zope2.View')
    grok.name('identification')

    phase = 'identification'
    question_filter = None

    def __init__(self, *a):
        super(Identification, self).__init__(*a)

    def _step(self, info, key, finder):
        node = finder(self.context, self.request.survey_session,
                self.question_filter)
        if node is not None:
            info[key] = '%s/%s/%s' % \
                    (self.request.survey_session.absolute_url(), 
                    '/'.join(node.short_path), self.phase)

    def GET(self):
        info = View(self.context, self.request).GET()
        info['phase'] = self.phase
        self._step(info, 'previous-step', FindPreviousQuestion)
        self._step(info, 'next-step', FindNextQuestion)
        return info

    def POST(self):
        allowed_values = Risk.__table__.c['identification'].type.values
        try:
            if self.input['present'] not in allowed_values:
                return {'type': 'error',
                        'message': '"present" field has invalid value'}
        except KeyError:
            return {'type': 'error',
                    'message': '"present" field missing'}
        self.context.identification = self.input['present']
        self.context.comment = self.input.get('comment', self.context.comment)
        return self.GET()


class Evaluation(Identification):
    grok.context(Risk)
    grok.require('zope2.View')
    grok.name('evaluation')

    phase = 'evaluation'
    question_filter = BaseEvaluation.question_filter


class ActionPlan(Identification):
    grok.context(Risk)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    question_filter = BaseActionPlan.question_filter

