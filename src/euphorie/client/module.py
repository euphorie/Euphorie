from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from euphorie.client import model
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.interfaces import ICustomizationPhaseSkinLayer
from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.client.navigation import getTreeData
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client.utils import HasText
from euphorie.content import MessageFactory as _
from euphorie.content.interfaces import ICustomRisksModule
from five import grok
from sqlalchemy import sql
from z3c.saconfig import Session

grok.templatedir("templates")


class IdentificationView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("module_identification")
    grok.name("index_html")

    phase = "identification"
    question_filter = None

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        context = aq_inner(self.context)
        module = self.request.survey.restrictedTraverse(
                                        context.zodb_path.split("/"))

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if module.optional:
                if "skip_children" in reply:
                    context.skip_children = reply.get("skip_children")
                    context.postponed = False
                else:
                    context.postponed = True

                SessionManager.session.touch()

            if reply["next"] == "previous":
                next = FindPreviousQuestion(context,
                        filter=self.question_filter)
                if next is None:
                    # We ran out of questions, step back to intro page
                    url = "%s/identification" % \
                            self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return
            else:
                if ICustomRisksModule.providedBy(module):
                    # The user will now be allowed to create custom
                    # (user-defined) risks.
                    url = "%s/customization/%d" % (
                            self.request.survey.absolute_url(),
                            int(self.context.path))
                    return self.request.response.redirect(url)
                next = FindNextQuestion(context, filter=self.question_filter)
                if next is None:
                    # We ran out of questions, proceed to the evaluation
                    url = "%s/evaluation" % self.request.survey.absolute_url()
                    return self.request.response.redirect(url)

            url = QuestionURL(self.request.survey, next,
                    phase="identification")
            self.request.response.redirect(url)
        else:
            self.tree = getTreeData(self.request, context,
                    filter=model.NO_CUSTOM_RISKS_FILTER)
            self.title = context.title
            self.module = module
            super(IdentificationView, self).update()


class CustomizationView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(ICustomizationPhaseSkinLayer)
    grok.template("module_customization")
    grok.name("index_html")

    phase = "customization"
    question_filter = None

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        context = aq_inner(self.context)
        survey = self.request.survey
        session = SessionManager.session
        self.module = survey.restrictedTraverse(self.context.zodb_path.split("/"))
        self.title = self.context.title
        self.tree = getTreeData(
                self.request, self.context, phase="identification",
                filter=model.NO_CUSTOM_RISKS_FILTER)

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply.get("next") == "previous":
                url = "%s/identification/%d" % (
                        self.request.survey.absolute_url(),
                        int(self.context.path))
                return self.request.response.redirect(url)

            elif reply.get("next") == "next":
                # We ran out of questions, proceed to the evaluation
                url = "%s/evaluation" % self.request.survey.absolute_url()
                return self.request.response.redirect(url)

            if not reply.get("description") or not reply.get("priority"):
                IStatusMessage(self.request).add(
                        _(u"Please fill in the required fields"),
                        type="error")
                self.request.set('errors', {
                    'description': not reply.get("description"),
                    'priority': not reply.get("priority"),
                });
                return;

            risk = model.Risk(
                comment=reply.get('comment'),
                priority=reply['priority'],
                risk_id=None,
                risk_type='risk', # XXX Could it also be top5 or policy?
                skip_evaluation=True,
                title=reply['description'],
            )
            risk.is_custom_risk = True
            risk.skip_children = False
            risk.postponed = False
            risk.has_description = None
            risk.zodb_path = "/".join([session.zodb_path] + ['customization'] + ['1'])
            risk.profile_index = 0 # XXX: not sure what this is for
            self.context.addChild(risk)
            IStatusMessage(self.request).add(
                    _(u"Your custom risk has been succesfully created."),
                    type="success")
        return super(CustomizationView, self).update()

    def get_custom_risks(self):
        session = SessionManager.session
        query = Session.query(model.Risk).filter(
            sql.and_(
                model.Risk.is_custom_risk == True,
                model.Risk.path.startswith(model.Module.path),
                model.Risk.session_id == session.id
            )
        )
        return query.all()


class EvaluationView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IEvaluationPhaseSkinLayer)
    grok.template("module_evaluation")
    grok.name("index_html")
    phase = "evaluation"
    question_filter = model.EVALUATION_FILTER

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        survey = self.request.survey
        self.module = survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        self.title = self.context.title
        self.tree = getTreeData(self.request, self.context,
                filter=self.question_filter, phase=self.phase)

        previous = FindPreviousQuestion(self.context,
                filter=self.question_filter)
        if previous is None:
            self.previous_url = "%s/%s" % (self.request.survey.absolute_url(),
                                           self.phase)
        else:
            self.previous_url = QuestionURL(survey, previous, phase=self.phase)

        next = FindNextQuestion(self.context, filter=self.question_filter)
        if next is None:
            self.next_url = "%s/actionplan" % \
                    self.request.survey.absolute_url()
        else:
            self.next_url = QuestionURL(survey, next, phase=self.phase)
        super(EvaluationView, self).update()


class ActionPlanView(grok.View):
    grok.context(model.Module)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("module_actionplan")
    grok.name("index_html")

    phase = "actionplan"
    question_filter = model.ACTION_PLAN_FILTER

    @property
    def use_solution_direction(self):
        module = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        return HasText(getattr(module, "solution_direction", None))

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        survey = self.request.survey
        self.module = survey.restrictedTraverse(
                self.context.zodb_path.split("/"))
        self.title = self.context.title
        self.tree = getTreeData(self.request, self.context,
                filter=self.question_filter, phase=self.phase)
        previous = FindPreviousQuestion(self.context,
                filter=self.question_filter)
        if previous is None:
            self.previous_url = "%s/%s" % (self.request.survey.absolute_url(),
                    self.phase)
        else:
            self.previous_url = QuestionURL(survey, previous, phase=self.phase)

        next = FindNextQuestion(self.context, filter=self.question_filter)
        if next is None:
            self.next_url = "%s/report" % self.request.survey.absolute_url()
        else:
            self.next_url = QuestionURL(survey, next, phase=self.phase)
        super(ActionPlanView, self).update()
