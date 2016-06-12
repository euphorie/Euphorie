from Acquisition import aq_parent
from zope.component import adapts
from ZPublisher.BaseRequest import DefaultPublishTraverse
from five import grok
from euphorie.content.risk import evaluation_algorithm
from euphorie.content.risk import IFrenchEvaluation
from euphorie.content.risk import IKinneyEvaluation
from euphorie.content.risk import IRisk
from euphorie.content.solution import ISolution
from euphorie.json import get_json_token
from euphorie.json import vocabulary_token
from euphorie.json import vocabulary_options
from euphorie.json import export_image
from ..utils import HasText
from ..model import Risk
from ..navigation import FindPreviousQuestion
from ..navigation import FindNextQuestion
# from ..risk import EvaluationView as BaseEvaluation
from ..risk import ActionPlanView as BaseActionPlan
# from ..risk import calculate_priority
from . import JsonView
from . import context_menu
from .actionplans import RiskActionPlans
from .actionplan import plan_info
from .interfaces import IClientAPISkinLayer


class View(JsonView):
    grok.context(Risk)
    grok.require('zope2.View')
    grok.name('index_html')

    check_update = True

    def do_GET(self):
        self.risk = risk = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split('/'))
        info = {'id': self.context.id,
                'type': 'risk',
                'title': risk.title,
                'module-title': aq_parent(risk).title,
                'problem-description': risk.problem_description,
                'show-not-applicable': risk.show_notapplicable,
                'evaluation-method': risk.evaluation_method,
                'present': self.context.identification,
                'priority': self.context.priority,
                'comment': self.context.comment,
                }
        images = filter(None,
                [export_image(risk, self.request,
                    'image%s' % postfix, 'caption%s' % postfix,
                    width=150, height=500, direction='thumbnail')
                    for postfix in ['', '2', '3', '4']])
        if images:
            info['images'] = images
        if HasText(risk.description):
            info['description'] = risk.description
        if HasText(risk.legal_reference):
            info['legal-reference'] = risk.legal_reference
        if risk.evaluation_method == 'calculated':
            algorithm = evaluation_algorithm(risk)
            info['evaluation-algorithm'] = algorithm
            if algorithm == 'french':
                field = IFrenchEvaluation['default_severity']
                info['severity'] = vocabulary_token(
                        field, self.context.severity) \
                                if self.context.severity else None
                info['severity-options'] = vocabulary_options(
                        field, self.request)
                field = IFrenchEvaluation['default_frequency']
                info['frequency'] = vocabulary_token(
                        field, self.context.frequency) \
                                if self.context.frequency else None
                info['frequency-options'] = vocabulary_options(
                        field, self.request)
            else:  # Kinney
                field = IKinneyEvaluation['default_frequency']
                info['frequency'] = vocabulary_token(
                        field, self.context.frequency) \
                                if self.context.frequency else None
                info['frequency-options'] = vocabulary_options(
                        field, self.request)
                field = IKinneyEvaluation['default_effect']
                info['effect'] = vocabulary_token(field, self.context.effect) \
                                if self.context.effect else None
                info['effect-options'] = vocabulary_options(
                        field, self.request)
                field = IKinneyEvaluation['default_probability']
                info['probability'] = vocabulary_token(
                        field, self.context.probability) \
                                if self.context.probability else None
                info['probability-options'] = vocabulary_options(
                        field, self.request)
        solutions = [solution for solution in risk.values()
                     if ISolution.providedBy(solution)]
        if solutions:
            info['standard-solutions'] = [
                    {'description': solution.description,
                     'action-plan': solution.action_plan,
                     'prevention-plan': solution.prevention_plan,
                     'requirements': solution.requirements}
                    for solution in risk.values()]
        return info


class Identification(JsonView):
    grok.context(Risk)
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
        return self.do_GET()


# class Evaluation(Identification):
#     grok.context(Risk)
#     grok.require('zope2.View')
#     grok.name('evaluation')

#     phase = 'evaluation'
#     next_phase = 'actionplan'
#     question_filter = BaseEvaluation.question_filter

#     def do_PUT(self):
#         self.risk = self.request.survey.restrictedTraverse(
#                 self.context.zodb_path.split('/'))
#         if self.risk.type in ['top5', 'policy']:
#                 return {'type': 'error',
#                         'message': 'Can not evaluate a %s risk'
#                             % self.risk.type}
#         try:
#             if self.risk.evaluation_method == 'direct':
#                 self.context.priority = get_json_token(self.input, 'priority',
#                         IRisk['default_priority'],
#                         default=self.context.priority)
#             else:
#                 algorithm = evaluation_algorithm(self.risk)
#                 if algorithm == 'french':
#                     self.context.severity = get_json_token(self.input,
#                             'severity', IFrenchEvaluation['default_severity'],
#                             self.context.severity)
#                     self.context.frequency = get_json_token(self.input,
#                             'frequency',
#                             IFrenchEvaluation['default_frequency'],
#                             self.context.frequency)
#                 else:  # Kinney
#                     self.context.probability = get_json_token(self.input,
#                             'probability',
#                             IKinneyEvaluation['default_probability'],
#                             self.context.probability)
#                     self.context.frequency = get_json_token(self.input,
#                             'frequency',
#                             IKinneyEvaluation['default_frequency'],
#                             self.context.frequency)
#                     self.context.effect = get_json_token(self.input, 'effect',
#                             IKinneyEvaluation['default_effect'],
#                             self.context.effect)
#                 calculate_priority(self.context, self.risk)
#         except (KeyError, ValueError) as e:
#             return {'type': 'error',
#                     'message': str(e)}
#         return self.do_GET()


class ActionPlan(Identification):
    grok.context(Risk)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    next_phase = None
    question_filter = BaseActionPlan.question_filter

    def do_GET(self):
        info = super(ActionPlan, self).do_GET()
        info['action-plans'] = [plan_info(plan)
                                for plan in self.context.action_plans]
        return info

    def do_PUT(self):
        self.risk = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split('/'))
        if 'priority' in self.input:
            if self.risk.type in ['top5', 'policy']:
                return {'type': 'error',
                        'message': 'Can not set priority for top-5 or '
                                   'policy risks'}
            self.context.priority = get_json_token(self.input, 'priority',
                    IRisk['default_priority'],
                    default=self.context.priority)
        self.context.comment = self.input.get('comment', self.context.comment)
        return self.do_GET()


class RiskPublishTraverse(DefaultPublishTraverse):
    """Publish traverser for risks.

    This is traverser makes it possible to traverse to the action plan
    container.
    """
    adapts(Risk, IClientAPISkinLayer)

    def publishTraverse(self, request, name):
        if name == 'actionplans':
            return RiskActionPlans(name, request, self.context)\
                    .__of__(self.context)
        else:
            return super(RiskPublishTraverse, self).publishTraverse(
                    request, name)
