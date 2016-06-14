from five import grok
from euphorie.json import export_image
from ..navigation import FindPreviousQuestion
from ..navigation import FindNextQuestion
# from ..module import EvaluationView as BaseEvaluation
from ..module import ActionPlanView as BaseActionPlan
from ..utils import HasText
from ..model import Module
from . import context_menu
from . import JsonView


class View(JsonView):
    grok.context(Module)
    grok.require('zope2.View')
    grok.name('index_html')

    check_update = True

    def do_GET(self):
        self.module = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split('/'))
        info = {'id': self.context.id,
                'type': 'module',
                'title': self.module.title,
                'optional': self.module.optional,
                }
        image = export_image(self.module, self.request,
                'image', 'caption', width=150, height=500,
                direction='thumbnail')
        if image:
            info['image'] = image
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
    next_phase = 'evaluation'
    question_filter = None

    def do_GET(self):
        info = View(self.context, self.request).do_GET()
        info['phase'] = self.phase
        self._step(info, 'previous-step', FindPreviousQuestion)
        self._step(info, 'next-step', FindNextQuestion, self.next_phase)
        if 'menu' in self.request.form:
            info['menu'] = context_menu(self.request, self.context, self.phase,
                    self.question_filter)
        return info

    def do_PUT(self):
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


# class Evaluation(Identification):
#     grok.context(Module)
#     grok.require('zope2.View')
#     grok.name('evaluation')

#     phase = 'evaluation'
#     next_phase = 'actionplan'
#     question_filter = BaseEvaluation.question_filter


class ActionPlan(Identification):
    grok.context(Module)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    next_phase = None
    question_filter = BaseActionPlan.question_filter
