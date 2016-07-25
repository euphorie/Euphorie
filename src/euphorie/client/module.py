"""
Module
------

Module views for the client.
"""

from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage
from euphorie.client import model
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
# from euphorie.client.interfaces import IEvaluationPhaseSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import ICustomizationPhaseSkinLayer
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import QuestionURL
from euphorie.client.navigation import getTreeData
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client.utils import HasText
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion
from five import grok
from sqlalchemy import sql
from z3c.saconfig import Session
from zope.i18n import translate
from .. import MessageFactory as _

grok.templatedir("templates")


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


class CustomizationView(grok.View, Mixin):
    """Module without a connection to a real module in the backend, container
    for custom risks.

    View name: @@index_html
    """
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
        self.module = survey.restrictedTraverse(self.context.zodb_path.split("/"))
        self.title = context.title
        self.tree = getTreeData(
            self.request, self.context, phase="identification",
            filter=model.NO_CUSTOM_RISKS_FILTER)

        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.message_required = translate(_(
            u"message_field_required", default=u"Please fill out this field."),
            target_language=lang)

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply.get("next") == "next":
                self.add_custom_risks(reply)
                url = "%s/actionplan" % self.request.survey.absolute_url()
                return self.request.response.redirect(url)

        return super(CustomizationView, self).update()

    def give_customization_feedback(self, added, updated, removed):
        if removed == 0 and added == 0 and updated == 0:
            IStatusMessage(self.request).add(
                _(u"No changes were made to your added risks."),
                type='warning'
            )
            return

        if added > 1:
            IStatusMessage(self.request).add(
                _(u"Your new added risks have been created."),
                type='success'
            )
        elif added == 1:
            IStatusMessage(self.request).add(
                _(u"A new added risk has been created."),
                type='success'
            )
        if updated > 1:
            IStatusMessage(self.request).add(
                _(u"Existing added risks have been updated."),
                type='success'
            )
        elif updated == 1:
            IStatusMessage(self.request).add(
                _(u"An existing added risk has been updated."),
                type='success'
            )
        if removed == 1:
            IStatusMessage(self.request).add(
                _(u"An added risk has been removed."), type='success')
        elif removed > 1:
            IStatusMessage(self.request).add(
                _(u"Added risks have been removed."), type='success')

    def add_custom_risks(self, form):
        session = SessionManager.session
        existing_risks = {}
        for risk_dict in form.get('risk', []):
            if risk_dict.get('id'):
                existing_risks[risk_dict['id']] = risk_dict
        # Remove risks not in the form any more.
        excluded = [int(k) for k in existing_risks.keys()]
        removed = len(self.context.removeChildren(excluded=excluded))

        sql_risks = self.context.children()
        added = 0
        updated = 0
        for risk_values in form.get('risk', []):
            if not risk_values.get("description") or not risk_values.get("priority"):
                continue
            if risk_values.get('id') in existing_risks:
                # Update an existing risk
                risk = sql_risks.filter_by(id=risk_values.get('id')).all()[0]
                if risk.title != risk_values['description'] or \
                        risk.priority != risk_values['priority'] or \
                        risk.comment != risk_values.get('comment'):

                    risk.comment = risk_values.get('comment')
                    risk.priority = risk_values['priority']
                    risk.title = risk_values['description']
                    updated += 1
            else:
                # Add a new risk
                risk = model.Risk(
                    comment=risk_values.get('comment'),
                    priority=risk_values['priority'],
                    risk_id=None,
                    risk_type='risk',  # XXX Could it also be top5 or policy?
                    skip_evaluation=True,
                    title=risk_values['description'],
                    identification="no"
                )
                risk.is_custom_risk = True
                risk.skip_children = False
                risk.postponed = False
                risk.has_description = None
                risk.zodb_path = "/".join([session.zodb_path] + [self.context.zodb_path] + ['1'])
                risk.profile_index = 0  # XXX: not sure what this is for
                self.context.addChild(risk)
                added += 1
        self.give_customization_feedback(added, updated, removed)


class IdentificationView(grok.View, Mixin):
    """The introduction page for a module.

    View name: @@index_html
    """
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
            self.save_and_continue(module)
        else:
            if IProfileQuestion.providedBy(module) and context.depth == 2:
                next = FindNextQuestion(context, filter=self.question_filter)
                if next is None:
                    url = "%s/actionplan" % self.request.survey.absolute_url()
                else:
                    url = QuestionURL(self.request.survey, next, phase=self.phase)
                return self.request.response.redirect(url)

            elif ICustomRisksModule.providedBy(module) \
                    and not self.context.skip_children \
                    and len(self.get_custom_risks()):
                url = "%s/customization/%d" % (
                    self.request.survey.absolute_url(),
                    int(self.context.path))
                return self.request.response.redirect(url)

            self.tree = getTreeData(
                self.request, context, filter=model.NO_CUSTOM_RISKS_FILTER)
            self.title = module.title
            self.module = module
            number_files = 0
            for i in range(1, 5):
                number_files += getattr(
                    self.module, 'file{0}'.format(i), None) and 1 or 0
            self.has_files = number_files > 0
            self.next_is_actionplan = not FindNextQuestion(
                context, filter=self.question_filter)
            super(IdentificationView, self).update()

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

        if reply["next"] == "previous":
            next = FindPreviousQuestion(context, filter=self.question_filter)
            if next is None:
                # We ran out of questions, step back to intro page
                url = "%s/identification" % self.request.survey.absolute_url()
                self.request.response.redirect(url)
                return
        else:
            if ICustomRisksModule.providedBy(module):
                if not context.skip_children:
                    # The user will now be allowed to create custom
                    # (user-defined) risks.
                    url = "%s/customization/%d" % (
                        self.request.survey.absolute_url(),
                        int(self.context.path))
                    return self.request.response.redirect(url)
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


# class EvaluationView(grok.View):
#     grok.context(model.Module)
#     grok.require("euphorie.client.ViewSurvey")
#     grok.layer(IEvaluationPhaseSkinLayer)
#     grok.template("module_evaluation")
#     grok.name("index_html")
#     phase = "evaluation"
#     question_filter = model.EVALUATION_FILTER

#     def update(self):
#         if redirectOnSurveyUpdate(self.request):
#             return

#         survey = self.request.survey
#         self.module = survey.restrictedTraverse(
#                 self.context.zodb_path.split("/"))
#         self.title = self.context.title
#         self.tree = getTreeData(self.request, self.context,
#                 filter=self.question_filter, phase=self.phase)

#         previous = FindPreviousQuestion(self.context,
#                 filter=self.question_filter)
#         if previous is None:
#             self.previous_url = "%s/%s" % (self.request.survey.absolute_url(),
#                                            self.phase)
#         else:
#             self.previous_url = QuestionURL(survey, previous, phase=self.phase)

#         next = FindNextQuestion(self.context, filter=self.question_filter)
#         if next is None:
#             self.next_url = "%s/actionplan" % \
#                     self.request.survey.absolute_url()
#         else:
#             self.next_url = QuestionURL(survey, next, phase=self.phase)
#         super(EvaluationView, self).update()


class ActionPlanView(grok.View):
    """The introduction page for an :obj:`euphorie.content.module` in an action
    plan.

    View name: @@index_html
    """
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
        if self.request.environ["REQUEST_METHOD"] == "POST":
            return self._update()

        context = aq_inner(self.context)
        module = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))
        self.module = module
        if (
            (IProfileQuestion.providedBy(module) and context.depth == 2) or
            (ICustomRisksModule.providedBy(module) and self.phase == 'actionplan')
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
        super(ActionPlanView, self).update()
