from zope.component import adapts
from five import grok
from sqlalchemy.orm import object_session
from euphorie.content.survey import ISurvey
from euphorie.client.model import SurveySession
from euphorie.client.api import JsonView
from euphorie.client.api.interfaces import IClientAPISkinLayer
from euphorie.client.utils import HasText
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.survey import Evaluation as BaseEvaluation
from euphorie.client.survey import ActionPlan as BaseActionPlan
from euphorie.client.survey import find_sql_context
from euphorie.client.survey import build_tree_aq_chain
from ZPublisher.BaseRequest import DefaultPublishTraverse


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

    def do_DELETE(self):
        session = object_session(self.context)
        session.delete(self.context)
        return {}
        
    def do_GET(self):
        info = {'id': self.context.id,
                'type': 'session',
                'survey': self.context.zodb_path,
                'created': self.context.created.isoformat(),
                'modified': self.context.modified.isoformat(),
                'title': self.context.title,
                'next-step': '%s/identification' % self.context.absolute_url(),
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
    next_phase = 'evaluation'
    question_filter = None

    def do_GET(self):
        info = View(self.context, self.request).do_GET()
        info['phase'] = self.phase
        risk = FindFirstQuestion(self.context, self.question_filter)
        if risk is not None:
            info['next-step'] = '%s/%s/%s' % \
                    (self.context.absolute_url(), 
                            '/'.join(risk.short_path), self.phase)
        else:
            info['next-step'] = '%s/%s' % \
                    (self.context.absolute_url(), self.next_phase)
        return info


class Evaluation(Identification):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('evaluation')

    phase = 'evaluation'
    next_phase = 'actionplan'
    question_filter = BaseEvaluation.question_filter


class ActionPlan(Identification):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    next_phase = None
    question_filter = BaseActionPlan.question_filter


class SurveySessionPublishTraverse(DefaultPublishTraverse):
    """Publish traverser for survey sessions.

    This takes care of finding a survey session tree item efficiently
    and setting up the right acquisition path for it.
    """
    adapts(SurveySession, IClientAPISkinLayer)

    def publishTraverse(self, request, name):
        stack = request['TraversalRequestNameStack']
        stack.append(name)
        node_id = find_sql_context(self.context.id, stack)
        if node_id is not None:
            self.request.survey_session = self.context
            if stack and not stack[-1].startswith('@@'):
                stack.append('@@%s' % stack.pop())
                
            return build_tree_aq_chain(self.context, node_id)
        stack.pop()
        return super(SurveySessionPublishTraverse, self).publishTraverse(
                request, name)
