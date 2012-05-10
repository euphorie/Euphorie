from Acquisition import aq_inner
from five import grok
from euphorie.client import model
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.client.navigation import getTreeData
from euphorie.client.session import SessionManager
from euphorie.client.utils import HasText
from euphorie.client.update import redirectOnSurveyUpdate
from sqlalchemy import sql


grok.templatedir("templates")

class IdentificationView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("module_identification")
    grok.name("index_html")

    phase = "identification"
    question_filter = model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        context=aq_inner(self.context)
        module=self.request.survey.restrictedTraverse(
                                        context.zodb_path.split("/"))

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            if module.optional:
                if "skip_children" in reply:
                    context.skip_children=reply.get("skip_children")
                    context.postponed=False
                else:
                    context.postponed=True

                SessionManager.session.touch()

            if reply["next"]=="previous":
                next = FindPreviousQuestion(context, filter=self.question_filter)
                if next is None:
                    # We ran out of questions, step back to intro page
                    url="%s/identification" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return
            else:
                next = FindNextQuestion(context, filter=self.question_filter)
                if next is None:
                    # We ran out of questions, proceed to the evaluation
                    url="%s/evaluation" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return

            url=QuestionURL(self.request.survey, next, phase="identification")
            self.request.response.redirect(url)
        else:
            self.tree=getTreeData(self.request, context)
            self.title=context.title
            self.module=module

            super(IdentificationView, self).update()


class EvaluationView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IEvaluationPhaseSkinLayer)
    grok.template("module_evaluation")
    grok.name("index_html")

    phase = "evaluation"
    question_filter = sql.and_(
            model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER,
            sql.or_(model.MODULE_WITH_RISK_NO_TOP5_NO_POLICY_FILTER,
                              model.RISK_PRESENT_NO_TOP5_NO_POLICY_FILTER))

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        survey=self.request.survey
        self.module=survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        self.title=self.context.title
        self.tree=getTreeData(self.request, self.context, filter=self.question_filter, phase=self.phase)

        previous=FindPreviousQuestion(self.context, filter=self.question_filter)
        if previous is None:
            self.previous_url="%s/%s" % (self.request.survey.absolute_url(), self.phase)
        else:
            self.previous_url=QuestionURL(survey, previous, phase=self.phase)

        next=FindNextQuestion(self.context, filter=self.question_filter)
        if next is None:
            self.next_url="%s/actionplan" % self.request.survey.absolute_url()
        else:
            self.next_url=QuestionURL(survey, next, phase=self.phase)
        super(EvaluationView, self).update()



class ActionPlanView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("module_actionplan")
    grok.name("index_html")

    phase = "actionplan"
    question_filter = sql.and_(
            model.RISK_OR_MODULE_WITH_DESCRIPTION_FILTER,
            sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                              model.RISK_PRESENT_OR_TOP5_FILTER))

    @property
    def use_solution_direction(self):
        module=self.request.survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        return HasText(getattr(module, "solution_direction", None))


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        survey=self.request.survey
        self.module=survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        self.title=self.context.title
        self.tree=getTreeData(self.request, self.context, filter=self.question_filter, phase=self.phase)

        previous=FindPreviousQuestion(self.context, filter=self.question_filter)
        if previous is None:
            self.previous_url="%s/%s" % (self.request.survey.absolute_url(), self.phase)
        else:
            self.previous_url=QuestionURL(survey, previous, phase=self.phase)

        next=FindNextQuestion(self.context, filter=self.question_filter)
        if next is None:
            self.next_url="%s/report" % self.request.survey.absolute_url()
        else:
            self.next_url=QuestionURL(survey, next, phase=self.phase)
        super(ActionPlanView, self).update()


