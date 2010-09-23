import calendar
import datetime
from Acquisition import aq_inner
from five import grok
from z3c.saconfig import Session
from euphorie.content.solution import ISolution
from euphorie.client import model
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.client.navigation import getTreeData
from euphorie.client.utils import HasText
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client.session import SessionManager
from sqlalchemy import sql
from repoze import formapi


grok.templatedir("templates")


class IdentificationView(grok.View):
    grok.context(model.Risk)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("risk_identification")
    grok.name("index_html")

    phase = "identification"
    risk_present = False
    use_problem_description = False


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            answer=reply.get("answer")
            self.context.postponed=(answer=="postponed")
            if not self.context.postponed:
                self.context.identification=answer
            self.context.comment=reply.get("comment")
            SessionManager.session.touch()

            if reply["next"]=="previous":
                next=FindPreviousQuestion(self.context)
                if next is None:
                    # We ran out of questions, step back to intro page
                    url="%s/identification" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return
            else:
                next=FindNextQuestion(self.context)
                if next is None:
                    # We ran out of questions, proceed to the evaluation
                    url="%s/evaluation" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return

            url=QuestionURL(self.request.survey, next, phase="identification")
            self.request.response.redirect(url)
        else:
            self.risk=risk=self.request.survey.restrictedTraverse(
                                            self.context.zodb_path.split("/"))
            self.tree=getTreeData(self.request, self.context)
            self.title=self.context.parent.title
            self.show_info=risk.image or \
                    HasText(risk.description) or \
                    HasText(risk.legal_reference)

            super(IdentificationView, self).update()



class EvaluationView(grok.View):
    grok.context(model.Risk)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IEvaluationPhaseSkinLayer)
    grok.template("risk_evaluation")
    grok.name("index_html")

    phase = "evaluation"
    risk_present = True
    question_filter = sql.or_(model.MODULE_WITH_RISK_NO_TOP5_NO_POLICY_FILTER,
                              model.RISK_PRESENT_NO_TOP5_NO_POLICY_FILTER)


    @property
    def use_problem_description(self):
        risk=self.request.survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        text=risk.problem_description
        return bool(text and text.strip())


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        risk=self.request.survey.restrictedTraverse(
                self.context.zodb_path.split("/"))

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            self.context.comment=reply.get("comment")
            if risk.evaluation_method=="calculated":
                self.context.frequency=reply.get("frequency")
                self.context.effect=reply.get("effect")
                self.context.probability=reply.get("probability")

                # Apply the Kinney method to determine the priority for the risk.
                try:
                    priority=self.context.frequency*self.context.effect*self.context.probability
                    if priority<=15:
                        self.context.priority="low"
                    elif priority<=50:
                        self.context.priority="medium"
                    else:
                        self.context.priority="high"
                except TypeError:
                    self.context.priority=None
            else:
                self.context.priority=reply.get("priority")

            SessionManager.session.touch()

            if reply["next"]=="previous":
                next=FindPreviousQuestion(self.context, filter=self.question_filter)
                if next is None:
                    # We ran out of questions, step back to intro page
                    url="%s/evaluation" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return
            else:
                next=FindNextQuestion(self.context, filter=self.question_filter)
                if next is None:
                    # We ran out of questions, proceed to the action plan
                    url="%s/actionplan" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return

            url=QuestionURL(self.request.survey, next, phase="evaluation")
            self.request.response.redirect(url)
        else:
            self.risk=risk
            self.title=self.context.parent.title
            self.tree=getTreeData(self.request, self.context, filter=self.question_filter, phase="evaluation")

            super(EvaluationView, self).update()



class ActionPlanItemForm(formapi.Form):
    """A single action plan item."""

    fields = dict(action_plan=unicode,
                  prevention_plan=unicode,
                  requirements=unicode,
                  responsible=unicode,
                  budget=int,
                  planning_start_day=int,
                  planning_start_month=int,
                  planning_start_year=int,
                  planning_end_day=int,
                  planning_end_month=int,
                  planning_end_year=int)

    @formapi.validator("planning_start_day")
    def valid_start_day(self):
        day=self.data["planning_start_day"]
        if day is None:
            return
        if not 1<=day<=31:
            yield _(u"Invalid day of month")

        try:
            (__, maxday)=calendar.monthrange(self.data["planning_start_year"],
                                            self.data["planning_start_month"])
            if day>maxday:
                yield _(u"Invalid day of month")
        except TypeError:
            # Invalid year most likely
            pass


    @formapi.validator("planning_end_day")
    def valid_end_day(self):
        day=self.data["planning_end_day"]
        if day is None:
            return
        if not 1<=day<=31:
            yield _(u"Invalid day of month")

        try:
            (__, maxday)=calendar.monthrange(self.data["planning_end_year"],
                                            self.data["planning_end_month"])
            if day>maxday:
                yield _(u"Invalid day of month")
        except TypeError:
            # Invalid year most likely
            pass




class ActionPlanView(grok.View):
    grok.context(model.Risk)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("risk_actionplan")
    grok.name("index_html")

    phase = "actionplan"
    question_filter = sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                              model.RISK_PRESENT_OR_TOP5_FILTER)

    @property
    def risk_present(self):
        return self.context.identification=="no"


    @property
    def use_problem_description(self):
        risk=self.request.survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        text=risk.problem_description
        return bool(text and text.strip())


    def _extractViewData(self):
        """Extract the data from the current context and build a
        data structure that is usable by the view."""

    def _fieldsToDate(self, year, month, day):
        if not day or not year:
            return None
        return datetime.date(year, month, day)


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        context=aq_inner(self.context)
        self.errors={}
        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            session=Session()
            errors=False

            reply["action_plans"]=[]
            new_plans=[]

            for measure in reply["measure"]:
                # repoze.formapi treats an empty input for an int as a
                # validation error.
                measure=dict([p for p in measure.items() if p[1].strip()])
                form=ActionPlanItemForm(params=measure)
                if not form.validate():
                    errors=True
                    plan=dict(measure)
                    plan["errors"]=dict(form.errors._dict)
                    reply["action_plans"].append(plan)
                    continue

                if len(measure)>2:
                    new_plans.append(model.ActionPlan(
                                          action_plan=form.data["action_plan"],
                                          prevention_plan=form.data["prevention_plan"],
                                          requirements=form.data["requirements"],
                                          responsible=form.data["responsible"],
                                          budget=form.data["budget"],
                                          planning_start=self._fieldsToDate(form.data["planning_start_year"],
                                                                       form.data["planning_start_month"],
                                                                       form.data["planning_start_day"]),
                                          planning_end=self._fieldsToDate(form.data["planning_end_year"],
                                                                     form.data["planning_end_month"],
                                                                     form.data["planning_end_day"]),
                                          ))

            if errors:
                self.data=reply
            else:
                context.comment=reply.get("comment")
                context.priority=reply.get("priority")

                for plan in context.action_plans:
                    session.delete(plan)
                context.action_plans.extend(new_plans)

                SessionManager.session.touch()

                if reply["next"]=="previous":
                    next=FindPreviousQuestion(context, filter=self.question_filter)
                    if next is None:
                        # We ran out of questions, step back to intro page
                        url="%s/evaluation" % self.request.survey.absolute_url()
                        self.request.response.redirect(url)
                        return
                else:
                    next=FindNextQuestion(context, filter=self.question_filter)
                    if next is None:
                        # We ran out of questions, proceed to the report
                        url="%s/report" % self.request.survey.absolute_url()
                        self.request.response.redirect(url)
                        return

                url=QuestionURL(self.request.survey, next, phase="actionplan")
                self.request.response.redirect(url)
                return
        else:
            if len(context.action_plans)==0:
                context.action_plans.append(model.ActionPlan())
            self.data=context

        self.risk=risk=self.request.survey.restrictedTraverse(
                                        context.zodb_path.split("/"))
        self.title=context.parent.title
        self.tree=getTreeData(self.request, context, filter=self.question_filter, phase="actionplan")
        self.solutions=[solution for solution in risk.values()
                       if ISolution.providedBy(solution)]

        super(ActionPlanView, self).update()

