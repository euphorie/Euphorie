from five import grok
from euphorie.client.utils import HasText
from euphorie.client.model import Module
from euphorie.client.api import context_menu
from euphorie.client.api import JsonView
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.module import EvaluationView as BaseEvaluation
from euphorie.client.module import ActionPlanView as BaseActionPlan


class View(JsonView):
    grok.context(Module)
    grok.require('zope2.View')
    grok.name('index_html')

    def do_GET(self):
        self.module = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split('/'))
        info = {'id': self.context.id,
                'type': 'module',
                'title': self.module.title,
                'optional': self.module.optional,
                }
        if HasText(self.module.description):
            info['description'] = self.module.description
        if HasText(self.module.solution_direction):
            info['solution-direction'] = self.module.solution_direction
        if self.module.optional:
            info['question'] = self.module.question
            info['skip-children'] = self.context.skip_children
        return info


class Identification(JsonView):
    grok.context(Module)
    grok.require('zope2.View')
    grok.name('identification')

    phase = 'identification'
    question_filter = None

    def _step(self, info, key, finder):
        node = finder(self.context, self.request.survey_session,
                self.question_filter)
        if node is not None:
            info[key] = '%s/%s/%s' % \
                    (self.request.survey_session.absolute_url(), 
                    '/'.join(node.short_path), self.phase)

    def do_GET(self):
        info = View(self.context, self.request).do_GET()
        info['phase'] = self.phase
        self._step(info, 'previous-step', FindPreviousQuestion)
        self._step(info, 'next-step', FindNextQuestion)
        if 'menu' in self.request.form:
            info['menu'] = context_menu(self.request, self.context, self.phase,
                    self.question_filter)
        return info

    def do_POST(self):
        self.module = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split('/'))
        if not self.module.optional:
            return self.do_GET()

        value = self.input.get('skip-children')
        if not isinstance(value, bool):
            return {'type': 'error',
                    'message': 'skip-children field missing or invalid'}
        self.context.skip_children = value
        return self.do_GET()


class Evaluation(Identification):
    grok.context(Module)
    grok.require('zope2.View')
    grok.name('evaluation')

    phase = 'evaluation'
    question_filter = BaseEvaluation.question_filter


class ActionPlan(Identification):
    grok.context(Module)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    question_filter = BaseActionPlan.question_filter
