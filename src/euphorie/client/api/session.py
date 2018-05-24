from Acquisition.interfaces import IAcquirer
from euphorie.client.api import JsonView
from euphorie.client.api.interfaces import IClientAPISkinLayer
from euphorie.client.model import Company
from euphorie.client.model import SurveySession
from euphorie.client.navigation import FindFirstQuestion
from euphorie.client.report import ActionPlanReportDownload
from euphorie.client.report import ActionPlanTimeline
from euphorie.client.report import IdentificationReportDownload
from euphorie.client.survey import ActionPlan as BaseActionPlan
from euphorie.client.survey import build_tree_aq_chain
from euphorie.client.survey import find_sql_context
from euphorie.client.utils import HasText
from euphorie.content.survey import ISurvey
from five import grok
from sqlalchemy.orm import object_session
from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.interface import Interface
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
        info = {
            'id': self.context.id,
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
    next_phase = 'actionplan'
    question_filter = None
    check_update = True

    def do_GET(self):
        info = View(self.context, self.request).do_GET()
        info['phase'] = self.phase
        risk = FindFirstQuestion(self.context, self.question_filter)
        if risk is not None:
            info['next-step'] = '%s/%s/%s' % (
                self.context.absolute_url(),
                '/'.join(risk.short_path),
                self.phase,
            )
        elif self.next_phase is not None:
            info['next-step'] = '%s/%s' % \
                    (self.context.absolute_url(), self.next_phase)
        return info


class ActionPlan(Identification):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.name('actionplan')

    phase = 'actionplan'
    next_phase = None
    question_filter = BaseActionPlan.question_filter
    check_update = True


class IdentificationReport(grok.View):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.layer(IClientAPISkinLayer)
    grok.name('report-identification')

    def render(self):
        view = IdentificationReportDownload(self.request.survey, self.request)
        view.session = self.context
        return view.render()


class ActionPlanReport(grok.View):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.layer(IClientAPISkinLayer)
    grok.name('report-actionplan')

    def render(self):
        view = ActionPlanReportDownload(self.request.survey, self.request)
        view.session = self.context
        if view.session.company is None:
            view.session.company = Company()
        return view.render()


class TimelineReport(grok.View):
    grok.context(SurveySession)
    grok.require('zope2.View')
    grok.layer(IClientAPISkinLayer)
    grok.name('report-timeline')

    def render(self):
        view = ActionPlanTimeline(self.request.survey, self.request)
        view.session = self.context
        return view.render()


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
            if stack and stack[-1] != 'actionplans' and not stack[
                -1
            ].startswith('@@'):
                stack.append('@@%s' % stack.pop())

            return build_tree_aq_chain(self.context, node_id)
        stack.pop()
        view = queryMultiAdapter((self.context, request), Interface, name)
        if view is not None:
            if IAcquirer.providedBy(view):
                view = view.__of__(self.context)
            return view
        else:
            raise KeyError(name)
