# coding=utf-8
from Acquisition import aq_inner
from euphorie.client import model
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.navigation import QuestionURL
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client.utils import HasText
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion
from logging import getLogger
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sqlalchemy import sql
from z3c.saconfig import Session

logger = getLogger(__name__)


class Mixin(object):

    def get_custom_risks(self):
        session = SessionManager.session
        query = Session.query(model.Risk).filter(
            sql.and_(
                model.Risk.is_custom_risk == 't',
                model.Risk.path.startswith(model.Module.path),
                model.Risk.session_id == session.id
            )
        ).order_by(model.Risk.id)
        return query.all()


class IdentificationView(BrowserView, Mixin):
    """The introduction page for a module.
    """
    variation_class = "variation-risk-assessment"
    phase = "identification"
    question_filter = None
    template = ViewPageTemplateFile('templates/module_identification.pt')

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not (
            self.context.restrictedTraverse('webhelpers').can_edit_session()
        ):

            return self.request.response.redirect(
                self.context.aq_parent.aq_parent.absolute_url() + '/@@start'
            )
        if redirectOnSurveyUpdate(self.request):
            return
        context = aq_inner(self.context)
        module = self.request.survey.restrictedTraverse(
            context.zodb_path.split("/"))
        if self.request.environ["REQUEST_METHOD"] == "POST":
            self.save_and_continue(module)
        else:
            if IProfileQuestion.providedBy(module) and context.depth == 2:
                next = FindNextQuestion(context, filter=self.question_filter)
                if next is None:
                    url = "%s/actionplan" % self.request.survey.absolute_url()
                else:
                    url = QuestionURL(
                        self.request.survey, next, phase=self.phase)
                return self.request.response.redirect(url)

            # elif ICustomRisksModule.providedBy(module) \
            #         and not self.context.skip_children \
            #         and len(self.get_custom_risks()):
            #     url = "%s/customization/%d" % (
            #         self.request.survey.absolute_url(),
            #         int(self.context.path))
            #     return self.request.response.redirect(url)

            self.tree = getTreeData(
                self.request, context, filter=self.question_filter)
            self.title = module.title
            self.module = module
            number_files = 0
            for i in range(1, 5):
                number_files += getattr(
                    self.module, 'file{0}'.format(i), None) and 1 or 0
            self.has_files = number_files > 0
            self.next_is_actionplan = not FindNextQuestion(
                context, filter=self.question_filter)
            if ICustomRisksModule.providedBy(module):
                template = ViewPageTemplateFile(
                    'templates/module_identification_custom.pt'
                ).__get__(self, "")
            else:
                template = self.template
            return template()

    def save_and_continue(self, module):
        """ We received a POST request.
            Submit the form and figure out where to go next.
        """
        context = aq_inner(self.context)
        reply = self.request.form
        if module.optional:
            if "skip_children" in reply:
                context.skip_children = reply.get("skip_children")
                context.postponed = False
            else:
                context.postponed = True
            SessionManager.session.touch()

        if reply.get("next") == "previous":
            next = FindPreviousQuestion(context, filter=self.question_filter)
            if next is None:
                # We ran out of questions, step back to intro page
                url = "%s/identification" % self.request.survey.absolute_url()
                self.request.response.redirect(url)
                return
        else:
            if ICustomRisksModule.providedBy(module):
                if reply["next"] == "add_custom_risk":
                    risk_id = self.add_custom_risk()
                    url = "%s/%d" % (self.context.absolute_url(), risk_id)
                    self.request.response.redirect(url)
                    return
                else:
                    # We ran out of questions, proceed to the evaluation
                    url = "%s/actionplan" % self.request.survey.absolute_url()
                    return self.request.response.redirect(url)
            next = FindNextQuestion(context, filter=self.question_filter)
            if next is None:
                # We ran out of questions, proceed to the evaluation
                url = "%s/actionplan" % self.request.survey.absolute_url()
                return self.request.response.redirect(url)

        url = QuestionURL(self.request.survey, next, phase="identification")
        self.request.response.redirect(url)

    def add_custom_risk(self):

        session = SessionManager.session
        sql_risks = self.context.children()
        if sql_risks.count():
            counter_id = max(
                [int(risk.path[-3:]) for risk in sql_risks.all()]) + 1
        else:
            counter_id = 1

        # Add a new risk
        risk = model.Risk(
            comment="",
            priority=None,
            risk_id=None,
            risk_type='risk',
            skip_evaluation=True,
            title="",
            identification=None,
            training_notes="",
            custom_description="",
        )
        risk.is_custom_risk = True
        risk.skip_children = False
        risk.postponed = False
        risk.has_description = None
        risk.zodb_path = "/".join(
            [session.zodb_path] +
            [self.context.zodb_path] +
            # There's a constraint for unique zodb_path per session
            ['%d' % counter_id]
        )
        risk.profile_index = 0  # XXX: not sure what this is for
        self.context.addChild(risk)
        return counter_id


class ActionPlanView(BrowserView):
    """The introduction page for an :obj:`euphorie.content.module` in an action
    plan.

    """
    variation_class = "variation-risk-assessment"
    phase = "actionplan"
    question_filter = model.ACTION_PLAN_FILTER

    @property
    def use_solution_direction(self):
        module = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))
        return HasText(getattr(module, "solution_direction", None))

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not (
            self.context.restrictedTraverse('webhelpers').can_edit_session()
        ):

            return self.request.response.redirect(
                self.context.aq_parent.aq_parent.absolute_url() + '/@@start'
            )
        if redirectOnSurveyUpdate(self.request):
            return
        if self.request.environ["REQUEST_METHOD"] == "POST":
            return self._update()

        context = aq_inner(self.context)
        module = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))
        self.module = module
        if (
            (IProfileQuestion.providedBy(module) and context.depth == 2) or
            (
                ICustomRisksModule.providedBy(module) and
                self.phase == 'actionplan'
            )
        ):
            next = FindNextQuestion(context, filter=self.question_filter)
            if next is None:
                if self.phase == 'identification':
                    url = "%s/actionplan" % self.request.survey.absolute_url()
                elif self.phase == 'evaluation':
                    url = "%s/actionplan" % self.request.survey.absolute_url()
                elif self.phase == 'actionplan':
                    url = "%s/report" % self.request.survey.absolute_url()
            else:
                url = QuestionURL(self.request.survey, next, phase=self.phase)
            return self.request.response.redirect(url)
        else:
            return self._update()

    def _update(self):
        survey = self.request.survey
        self.title = self.context.title
        self.tree = getTreeData(
            self.request, self.context, filter=self.question_filter,
            phase=self.phase)
        previous = FindPreviousQuestion(
            self.context, filter=self.question_filter)
        if previous is None:
            self.previous_url = "%s/%s" % (
                self.request.survey.absolute_url(), self.phase)
        else:
            self.previous_url = QuestionURL(survey, previous, phase=self.phase)

        next = FindNextQuestion(self.context, filter=self.question_filter)
        if next is None:
            self.next_url = "%s/report" % self.request.survey.absolute_url()
        else:
            self.next_url = QuestionURL(survey, next, phase=self.phase)
        return self.index()
