# coding=utf-8
"""
Risk
----

Views for the identification and action plan phases.
"""

from .. import MessageFactory as _
from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.client import model
from euphorie.client.interfaces import IActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IItalyIdentificationPhaseSkinLayer
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.navigation import QuestionURL
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client.utils import HasText
from euphorie.content.solution import ISolution
from euphorie.content.survey import ISurvey
from euphorie.content.utils import StripMarkup
from five import grok
from json import dumps
from json import loads
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from z3c.saconfig import Session
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
import datetime

grok.templatedir("templates")

IMAGE_CLASS = {
    0: '',
    1: 'twelve',
    2: 'six',
    3: 'four',
    4: 'three',
}


class IdentificationView(grok.View):
    """A view for displaying a question in the idenfication phase

    View name: @@index_html
    """
    grok.context(model.Risk)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("risk_identification")
    grok.name("index_html")

    question_filter = None
    DESCRIPTION_CROP_LENGTH = 200

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        self.risk = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))

        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.use_existing_measures = settings.get('use_existing_measures', False)

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            answer = reply.get("answer")
            self.context.comment = reply.get("comment")
            if self.use_existing_measures:
                measures = self.get_existing_measures()
                new_measures = []
                for i, entry in enumerate(measures):
                    on = int(bool(reply.get('measure-{}'.format(i))))
                    entry[0] = on
                    measures[i] = entry
                    if on:
                        new_measures.append([1, entry[1]])
                for k, val in reply.items():
                    if k.startswith('new-measure') and val.strip() != '':
                        new_measures.append([1, val])
                self.context.existing_measures = dumps(new_measures)
            self.context.postponed = (answer == "postponed")
            if self.context.postponed:
                self.context.identification = None
            else:
                self.context.identification = answer
                if self.risk.type in ('top5', 'policy'):
                    self.context.priority = 'high'
                elif self.risk.evaluation_method == 'calculated':
                    self.calculatePriority(self.risk, reply)
                elif self.risk.evaluation_method == "direct":
                    self.context.priority = reply.get("priority")

            SessionManager.session.touch()

            if reply["next"] == "previous":
                next = FindPreviousQuestion(
                    self.context,
                    filter=self.question_filter)
                if next is None:
                    # We ran out of questions, step back to intro page
                    url = "%s/identification" % \
                        self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return
            else:
                next = FindNextQuestion(
                    self.context,
                    filter=self.question_filter)
                if next is None:
                    # We ran out of questions, proceed to the action plan
                    url = "%s/actionplan" % self.request.survey.absolute_url()
                    self.request.response.redirect(url)
                    return

            url = QuestionURL(self.request.survey, next, phase="identification")
            self.request.response.redirect(url)

        else:
            self.tree = getTreeData(self.request, self.context)
            self.title = self.context.parent.title
            self.show_info = self.risk.image or \
                HasText(self.risk.description) or \
                HasText(self.risk.legal_reference)
            number_images = getattr(self.risk, 'image', None) and 1 or 0
            if number_images:
                for i in range(2, 5):
                    number_images += getattr(
                        self.risk, 'image{0}'.format(i), None) and 1 or 0
            self.has_images = number_images > 0
            self.number_images = number_images
            self.image_class = IMAGE_CLASS[number_images]
            number_files = 0
            for i in range(1, 5):
                number_files += getattr(
                    self.risk, 'file{0}'.format(i), None) and 1 or 0
            self.has_files = number_files > 0
            self.risk_number = self.context.number

            ploneview = getMultiAdapter(
                (self.context, self.request), name="plone")
            stripped_description = StripMarkup(self.risk.description)
            if len(stripped_description) > self.DESCRIPTION_CROP_LENGTH:
                self.description_intro = ploneview.cropText(
                    stripped_description, self.DESCRIPTION_CROP_LENGTH)
            else:
                self.description_intro = ""
            self.description_probability = _(
                u"help_default_probability", default=u"Indicate how "
                "likely occurence of this risk is in a normal situation.")
            self.description_frequency = _(
                u"help_default_frequency", default=u"Indicate how often this "
                u"risk occurs in a normal situation.")
            self.description_severity = _(
                u"help_default_severity", default=u"Indicate the "
                "severity if this risk occurs.")

            self.title_extra = ''
            self.show_existing_measures = False
            if self.use_existing_measures:
                measures = self.risk.existing_measures or ""
                # Only show the form to select and add existing measures if
                # at least one measure was defined in the CMS
                if len(measures):
                    self.show_existing_measures = True
                    self.title_extra = _(
                        "Are the measures that are selected above sufficient?")
                if not self.context.existing_measures:
                    self.context.existing_measures = dumps(
                        [(1, text) for text in measures.splitlines()])

            if getattr(self.request.survey, 'enable_custom_evaluation_descriptions', False):
                if self.request.survey.evaluation_algorithm != 'french':
                    custom_dp = getattr(
                        self.request.survey, 'description_probability', '') or ''
                    self.description_probability = custom_dp.strip() or self.description_probability
                custom_df = getattr(self.request.survey, 'description_frequency', '') or ''
                self.description_frequency = custom_df.strip() or self.description_frequency
                custom_ds = getattr(self.request.survey, 'description_severity', '') or ''
                self.description_severity = custom_ds.strip() or self.description_severity

            # Italian special
            if IItalyIdentificationPhaseSkinLayer.providedBy(self.request):
                self.skip_evaluation = True
            else:
                self.skip_evaluation = False
            super(IdentificationView, self).update()

    def get_existing_measures(self):
        try:
            existing_measures = loads(self.context.existing_measures)
        except ValueError:
            measures = self.risk.existing_measures or ""
            existing_measures = [(1, text) for text in measures.splitlines()]
            self.context.existing_measures = dumps(existing_measures)
        return existing_measures

    @property
    def use_problem_description(self):
        risk = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))
        text = risk.problem_description
        return bool(text and text.strip())

    def evaluation_algorithm(self, risk):
        return evaluation_algorithm(risk)

    def calculatePriority(self, risk, reply):
        self.context.frequency = reply.get("frequency")
        try:
            if evaluation_algorithm(risk) == "french":
                self.context.effect = reply.get("severity")
            else:  # Kinney method
                self.context.effect = reply.get("effect")
                self.context.probability = reply.get("probability")
            calculate_priority(self.context, risk)
        except TypeError:
            pass
        return self.context.priority


class ActionPlanView(grok.View):
    """Logic for creating new action plans.

    View name: @@index_html
    """
    grok.context(model.Risk)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IActionPlanPhaseSkinLayer)
    grok.template("risk_actionplan")
    grok.name("index_html")

    phase = "actionplan"
    question_filter = model.ACTION_PLAN_FILTER
    DESCRIPTION_CROP_LENGTH = 200

    def get_existing_measures(self):
        try:
            existing_measures = (
                self.context.existing_measures and
                loads(self.context.existing_measures) or [])
        except ValueError:
            measures = self.risk.existing_measures or ""
            existing_measures = [(1, text) for text in measures.splitlines()]
            self.context.existing_measures = dumps(existing_measures)
        return existing_measures

    @property
    def risk_present(self):
        return self.context.identification == "no"

    @property
    def is_custom_risk(self):
        return getattr(self.context, 'is_custom_risk', False)

    @property
    def use_problem_description(self):
        if self.is_custom_risk:
            return False
        risk = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))
        text = risk.problem_description
        return bool(text and text.strip())

    def _extractViewData(self):
        """Extract the data from the current context and build a data structure
        that is usable by the view.
        """

    def _fieldsToDate(self, year, month, day):
        if not day or not year:
            return None
        return datetime.date(year, month, day)

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return
        context = aq_inner(self.context)

        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.use_existing_measures = settings.get('use_existing_measures', False)

        self.next_is_report = False
        # already compute "next" here, so that we can know in the template
        # if the next step might be the report phase, in which case we
        # need to switch off the sidebar
        next = FindNextQuestion(
            context, filter=self.question_filter)
        if next is None:
            # We ran out of questions, proceed to the report
            url = "%s/report" % self.request.survey.absolute_url()
            self.next_is_report = True
        else:
            url = QuestionURL(
                self.request.survey, next, phase="actionplan")

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            session = Session()
            context.comment = reply.get("comment")
            context.priority = reply.get("priority")

            new_plans = self.extract_plans_from_request()
            for plan in context.action_plans:
                session.delete(plan)
            context.action_plans.extend(new_plans)
            SessionManager.session.touch()

            if reply["next"] == "previous":
                next = FindPreviousQuestion(
                    context, filter=self.question_filter)
                if next is None:
                    # We ran out of questions, step back to intro page
                    url = "%s/evaluation" % self.request.survey.absolute_url()
                else:
                    url = QuestionURL(
                        self.request.survey, next, phase="actionplan")
            return self.request.response.redirect(url)

        else:
            self.data = context
            if len(context.action_plans) == 0:
                self.data.empty_action_plan = [model.ActionPlan()]

        self.title = context.parent.title
        self.tree = getTreeData(
            self.request, context,
            filter=self.question_filter, phase="actionplan")
        if self.context.is_custom_risk:
            self.risk = self.context
            self.description_intro = u""
            self.risk.description = u""
            number_images = 0
        else:
            self.risk = self.request.survey.restrictedTraverse(
                context.zodb_path.split("/"))
            number_images = getattr(self.risk, 'image', None) and 1 or 0
            if number_images:
                for i in range(2, 5):
                    number_images += getattr(
                        self.risk, 'image{0}'.format(i), None) and 1 or 0
            ploneview = getMultiAdapter(
                (self.context, self.request), name="plone")
            stripped_description = StripMarkup(self.risk.description)
            if len(stripped_description) > self.DESCRIPTION_CROP_LENGTH:
                self.description_intro = ploneview.cropText(
                    stripped_description, self.DESCRIPTION_CROP_LENGTH)
            else:
                self.description_intro = ""
            self.solutions = [
                solution for solution in self.risk.values()
                if ISolution.providedBy(solution)]

        self.number_images = number_images
        self.has_images = number_images > 0
        self.image_class = IMAGE_CLASS[number_images]
        self.risk_number = self.context.number
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.delete_confirmation = translate(_(
            u"Are you sure you want to delete this measure? This action can "
            u"not be reverted."),
            target_language=lang)
        self.override_confirmation = translate(_(
            u"The current text in the fields 'Action plan', 'Prevention plan' and "
            u"'Requirements' of this measure will be overwritten. This action cannot be "
            u"reverted. Are you sure you want to continue?"),
            target_language=lang)
        self.message_date_before = translate(_(
            u"error_validation_before_end_date",
            default=u"This date must be on or before the end date."),
            target_language=lang)
        self.message_date_after = translate(_(
            u"error_validation_after_start_date",
            default=u"This date must be on or after the start date."),
            target_language=lang)
        self.message_positive_number = translate(_(
            u"error_validation_positive_whole_number",
            default=u"This value must be a positive whole number."),
            target_language=lang)
        super(ActionPlanView, self).update()

    def extract_plans_from_request(self):
        """ Create new ActionPlan objects by parsing the Request.
        """
        new_plans = []
        added = 0
        updated = 0
        existing_plans = {}
        for plan in self.context.action_plans:
            existing_plans[str(plan.id)] = plan
        form = self.request.form
        form["action_plans"] = []
        for i in range(0, len(form['measure'])):
            measure = dict([p for p in form['measure'][i].items()
                            if p[1].strip()])
            form['action_plans'].append(measure)
            if len(measure):
                budget = measure.get("budget")
                budget = budget and budget.split(',')[0].split('.')[0]
                if measure.get('id', '-1') in existing_plans:
                    plan = existing_plans[measure.get('id')]
                    if (
                        measure.get("action_plan") != plan.action_plan or
                        measure.get("prevention_plan") != plan.prevention_plan or
                        measure.get("requirements") != plan.requirements or
                        measure.get("responsible") != plan .responsible or (
                            plan.budget and (budget != str(plan.budget)) or
                            plan.budget is None and budget
                        ) or (
                            (plan.planning_start and
                                measure.get('planning_start') != plan.planning_start.strftime('%Y-%m-%d')) or
                            (plan.planning_start is None and measure.get('planning_start'))
                        ) or (
                            (plan.planning_end and
                                measure.get('planning_end') != plan.planning_end.strftime('%Y-%m-%d')) or
                            (plan.planning_end is None and measure.get('planning_end'))
                        )
                    ):
                        updated += 1
                    del existing_plans[measure.get('id')]
                else:
                    added += 1
                new_plans.append(
                    model.ActionPlan(
                        action_plan=measure.get("action_plan"),
                        prevention_plan=measure.get("prevention_plan"),
                        requirements=measure.get("requirements"),
                        responsible=measure.get("responsible"),
                        budget=budget,
                        planning_start=measure.get('planning_start'),
                        planning_end=measure.get('planning_end')
                    )
                )
        removed = len(existing_plans)
        if added == 0 and updated == 0 and removed == 0:
            IStatusMessage(self.request).add(
                _(u"No changes were made to measures in your action plan."),
                type='info'
            )
        if added == 1:
            IStatusMessage(self.request).add(
                _(u"message_measure_saved", default=u"A measure has been added to your action plan."),
                type='success'
            )
        elif added == 2:
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_saved_2",
                    default=u"${no_of_measures} measures have been added to your action plan.",
                    mapping={'no_of_measures': str(added)}),
                type='success'
            )
        elif added in (3, 4):
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_saved_3_4",
                    default=u"${no_of_measures} measures have been added to your action plan.",
                    mapping={'no_of_measures': str(added)}),
                type='success'
            )
        elif added > 4:
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_saved",
                    default=u"${no_of_measures} measures have been added to your action plan.",
                    mapping={'no_of_measures': str(added)}),
                type='success'
            )

        if updated == 1:
            IStatusMessage(self.request).add(
                _(u"message_measure_updated", default=u"A measure has been updated in your action plan."),
                type='success'
            )
        elif updated == 2:
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_updated_2",
                    default=u"${no_of_measures} measures have been updated in your action plan.",
                    mapping={'no_of_measures': str(updated)}),
                type='success'
            )
        elif updated in (3, 4):
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_updated_3_4",
                    default=u"${no_of_measures} measures have been updated in your action plan.",
                    mapping={'no_of_measures': str(updated)}),
                type='success'
            )
        elif updated > 4:
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_updated",
                    default=u"${no_of_measures} measures have been updated in your action plan.",
                    mapping={'no_of_measures': str(updated)}),
                type='success'
            )

        if removed == 1:
            IStatusMessage(self.request).add(
                _(u"message_measure_removed", default=u"A measure has been removed from your action plan."),
                type='success'
            )
        elif removed == 2:
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_removed_3",
                    default=u"${no_of_measures} measures have been removed from your action plan.",
                    mapping={'no_of_measures': str(removed)}),
                type='success'
            )
        elif removed in (3, 4):
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_removed_3_4",
                    default=u"${no_of_measures} measures have been removed from your action plan.",
                    mapping={'no_of_measures': str(removed)}),
                type='success'
            )
        elif removed > 4:
            IStatusMessage(self.request).add(
                _(
                    u"message_measures_removed",
                    default=u"${no_of_measures} measures have been removed from your action plan.",
                    mapping={'no_of_measures': str(removed)}),
                type='success'
            )
        return new_plans


def calculate_priority(db_risk, risk):
    """Update the risk priority.

    This method can be used for risks using a calculated evaluation method
    to determine the priority absed on the subquestions.
    """
    assert risk.evaluation_method == 'calculated'
    if risk.type in ['top5', 'policy']:
        db_risk.priority = 'high'
    elif evaluation_algorithm(risk) == 'french':
        priority = db_risk.frequency * db_risk.effect
        if priority < 10:
            db_risk.priority = 'low'
        elif priority <= 45:
            db_risk.priority = 'medium'
        else:
            db_risk.priority = 'high'
    else:
        priority = db_risk.frequency * db_risk.effect * db_risk.probability
        if priority <= 15:
            db_risk.priority = 'low'
        elif priority <= 50:
            db_risk.priority = 'medium'
        else:
            db_risk.priority = 'high'
    return db_risk.priority


def evaluation_algorithm(risk):
    for parent in aq_chain(aq_inner(risk)):
        if ISurvey.providedBy(parent):
            return getattr(parent, 'evaluation_algorithm', u'kinney')
    else:
        return u'kinney'
