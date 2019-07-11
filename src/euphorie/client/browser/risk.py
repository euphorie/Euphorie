# coding=utf-8
"""
Risk
----

Views for the identification and action plan phases.
"""

from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from collections import OrderedDict
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client.interfaces import IItalyActionPlanPhaseSkinLayer
from euphorie.client.interfaces import IItalyIdentificationPhaseSkinLayer
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.navigation import QuestionURL
from euphorie.client.session import SessionManager
from euphorie.client.update import redirectOnSurveyUpdate
from euphorie.client.utils import HasText
from euphorie.content.risk import IRisk
from euphorie.content.solution import ISolution
from euphorie.content.survey import get_tool_type
from euphorie.content.survey import ISurvey
from euphorie.content.utils import IToolTypesInfo
from htmllaundry import StripMarkup
from json import dumps
from json import loads
from plone.memoize.instance import memoize
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from sqlalchemy import and_
from z3c.appconfig.interfaces import IAppConfig
from z3c.appconfig.utils import asBool
from z3c.saconfig import Session
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
import datetime

IMAGE_CLASS = {
    0: '',
    1: 'twelve',
    2: 'six',
    3: 'four',
    4: 'three',
}


class IdentificationView(BrowserView):
    """A view for displaying a question in the identification phase
    """
    template = ViewPageTemplateFile('templates/risk_identification.pt')
    variation_class = "variation-risk-assessment"

    question_filter = None

    # default value is False, can be overwritten by certain conditions
    skip_evaluation = False

    monitored_properties = {
        "identification": None,
        "postponed": None,
        "frequency": None,
        "severity": None,
        "priority": None,
        "comment": u"",
        "existing_measures": u"[]",
        "training_notes": None,
        "custom_description": None,
    }

    @property
    @memoize
    def webhelpers(self):
        return self.context.restrictedTraverse('webhelpers')

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not (
            self.webhelpers.can_edit_session()
        ):
            return self.request.response.redirect(
                self.webhelpers.survey_url() + '/@@start'
            )
        if redirectOnSurveyUpdate(self.request):
            return

        if self.is_custom_risk:
            # # Fetch the custom_risks module, so that we can at least
            # # traverse to the survey
            # path = "/".join(self.context.zodb_path.split('/')[:-1])
            self.risk = None
        else:
            self.risk = self.request.survey.restrictedTraverse(
                self.context.zodb_path.split("/"))

        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.tti = getUtility(IToolTypesInfo)
        self.my_tool_type = get_tool_type(self.context)
        self.use_existing_measures = (
            asBool(settings.get('use_existing_measures', False)) and
            self.my_tool_type in self.tti.types_existing_measures
        )
        self.use_training_module = asBool(
            settings.get('use_training_module', False))

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            # Don't persist anything if the user skipped the question
            if reply.get("next", None) == 'skip':
                return self.proceed_to_next(reply)
            old_values = {}
            for prop, default in self.monitored_properties.items():
                if prop == "existing_measures":
                    val = dumps([
                        entry for entry in loads(
                            getattr(self.context, prop, default)
                        ) if entry[1]
                    ])
                else:
                    val = getattr(self.context, prop, default)
                old_values[prop] = val
            answer = reply.get("answer", None)
            # If answer is not present in the request, do not attempt to set
            # any answer-related data, since the request might have come
            # from a sub-form.
            if answer:
                self.context.comment = reply.get("comment")
                self.context.postponed = (answer == "postponed")
                if self.context.postponed:
                    self.context.identification = None
                else:
                    self.context.identification = answer
                    if getattr(self.risk, "type", "") in ('top5', 'policy'):
                        self.context.priority = 'high'
                    elif getattr(
                        self.risk, "evaluation_method", ""
                    ) == 'calculated':
                        self.calculatePriority(self.risk, reply)
                    elif (
                        self.risk is None or
                        self.risk.evaluation_method == "direct"
                    ):
                        self.context.priority = reply.get("priority")

            if (
                self.use_existing_measures and
                reply.get('handle_measures_in_place')
            ):
                measures = self.get_existing_measures()
                new_measures = []
                seen = []
                for i, entry in enumerate(measures):
                    on = int(bool(reply.get('measure-{}'.format(i))))
                    new_measures.append((entry[0], on))
                    if on:
                        seen.append(i)
                for k, val in reply.items():
                    if (
                        k.startswith('new-measure') and
                        isinstance(val, str) and
                        val.strip() != ''
                    ):
                        new_measures.append((val, 1))
                    elif k.startswith('present-measure') and val.strip() != '':
                        idx = k.rsplit("-", 1)[-1]
                        try:
                            idx = int(idx)
                        except (TypeError, ValueError):
                            continue
                        if idx in seen:
                            new_measures[idx] = (val, 1)

                # Only save the measures that are active
                self.context.existing_measures = safe_unicode(
                    dumps([entry for entry in new_measures if entry[1]]))

            if self.use_training_module and reply.get('handle_training_notes'):
                self.context.training_notes = reply.get("training_notes")

            # This only happens on custom risks
            if reply.get("handle_custom_description"):
                self.context.custom_description = reply.get("custom_description")

            if reply.get("title"):
                self.context.title = reply.get("title")

            # Check if there was a change. If yes, touch the session
            changed = False
            for prop, default in self.monitored_properties.items():
                if prop == "existing_measures":
                    val = dumps([
                        entry for entry in loads(
                            getattr(self.context, prop, default)
                        ) if entry[1]
                    ])
                else:
                    val = getattr(self.context, prop, None)
                if (
                    val and val != old_values[prop]
                ):
                    changed = True
                    break
            if changed:
                SessionManager.session.touch()

            return self.proceed_to_next(reply)

        else:
            self._prepare_risk()
            if self.is_custom_risk:
                template = ViewPageTemplateFile(
                    'templates/risk_identification_custom.pt').__get__(self, "")  # noqa
                next = FindNextQuestion(
                    self.context,
                    filter=self.question_filter)
                self.has_next_risk = next or False
            else:
                template = self.template
            return template()

    def _prepare_risk(self):
        self.tree = getTreeData(self.request, self.context)
        self.title = self.context.parent.title
        has_risk_description = (
            (self.risk and HasText(self.risk.description)) or
            getattr(self.context, 'custom_description', '')
        )
        self.show_info = (
            getattr(self.risk, "image", None) or
            (
                self.risk is None or
                HasText(self.risk.description)
            )
        )

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
        self.has_legal = HasText(getattr(self.risk, "legal_reference", None))
        self.show_resources = self.has_legal or self.has_files

        self.risk_number = self.context.number

        self.description_probability = _(
            u"help_default_probability", default=u"Indicate how "
            u"likely occurence of this risk is in a normal situation.")
        self.description_frequency = _(
            u"help_default_frequency", default=u"Indicate how often this "
            u"risk occurs in a normal situation.")
        self.description_severity = _(
            u"help_default_severity", default=u"Indicate the "
            u"severity if this risk occurs.")

        tool_types = self.tti()
        tt_default = self.tti.default_tool_type
        tool_type_data = tool_types.get(
            self.my_tool_type, tool_types[tt_default])
        default_type_data = tool_types['classic']
        self.show_existing_measures = False

        # Fill some labels with default texts
        self.answer_yes = default_type_data['answer_yes']
        self.answer_no = default_type_data['answer_no']
        self.answer_na = default_type_data['answer_na']
        self.intro_extra = ""
        if self.is_custom_risk:
            self.intro_extra = tool_type_data.get('custom_intro_extra', '')
            if self.use_existing_measures:
                self.answer_yes = tool_type_data['answer_yes']
                self.answer_no = tool_type_data['answer_no']
        self.button_add_extra = tool_type_data.get('button_add_extra', '')
        self.intro_questions = tool_type_data.get('intro_questions', '')
        self.placeholder_add_extra = tool_type_data.get(
                'placeholder_add_extra', '')
        self.button_remove_extra = ""
        if self.use_existing_measures:
            measures = self.get_existing_measures()
            # Only show the form to select and add existing measures if
            # at least one pre-existring measure is present
            # In this case, also change some labels
            if len(measures):
                self.show_existing_measures = True
                self.intro_extra = tool_type_data.get('intro_extra', '')
                self.button_remove_extra = tool_type_data.get(
                    'button_remove_extra', '')
                self.answer_yes = tool_type_data['answer_yes']
                self.answer_no = tool_type_data['answer_no']
                self.answer_na = tool_type_data['answer_na']
            if not self.context.existing_measures:
                existing_measures = [
                    (text, 0) for text in measures
                ]
                self.context.existing_measures = safe_unicode(
                    dumps(existing_measures))

        if getattr(self.request.survey, 'enable_custom_evaluation_descriptions', False):
            if self.request.survey.evaluation_algorithm != 'french':
                custom_dp = getattr(
                    self.request.survey, 'description_probability', '') or ''
                self.description_probability = custom_dp.strip() or self.description_probability
            custom_df = getattr(self.request.survey, 'description_frequency', '') or ''
            self.description_frequency = custom_df.strip() or self.description_frequency
            custom_ds = getattr(self.request.survey, 'description_severity', '') or ''
            self.description_severity = custom_ds.strip() or self.description_severity

        # compute training side template
        self.slide_template = (
            (has_risk_description or number_images) and "template-two-column"
            or "template-default"
        )

        # Italian special
        if IItalyIdentificationPhaseSkinLayer.providedBy(self.request):
            self.skip_evaluation = True

    def proceed_to_next(self, reply):
        if reply.get("next", None) == "previous":
            next = FindPreviousQuestion(
                self.context,
                filter=self.question_filter)
            if next is None:
                # We ran out of questions, step back to intro page
                url = "%s/identification" % \
                    self.request.survey.absolute_url()
                self.request.response.redirect(url)
                return
        elif reply.get("next", None) in ("next", "skip"):
            next = FindNextQuestion(
                self.context,
                filter=self.question_filter)
            if next is None:
                # We ran out of questions, proceed to the action plan
                url = "%s/actionplan" % self.request.survey.absolute_url()
                self.request.response.redirect(url)
                return

        elif reply.get("next", None) == "add_custom_risk":
            module = aq_parent(self.context)
            sql_module_q = Session.query(model.Module).filter(
                and_(
                    model.SurveyTreeItem.session == SessionManager.session,
                    model.Module.zodb_path == u'custom-risks',
                    )
            )
            if not sql_module_q.count():
                url = QuestionURL(
                    self.request.survey, self.context, phase="identification")
                self.request.response.redirect(url)
                return
            sql_module = sql_module_q.one()
            view = getMultiAdapter(
                (sql_module, self.request), name="index_html")
            risk_id = view.add_custom_risk()
            url = "%s/%d" % (module.absolute_url(), risk_id)
            self.request.response.redirect(url)
            return
        elif reply.get("next", None) == "actionplan":
            url = "%s/actionplan" % self.request.survey.absolute_url()
            self.request.response.redirect(url)
            return
        # stay on current risk
        else:
            next = self.context

        url = QuestionURL(self.request.survey, next, phase="identification")
        self.request.response.redirect(url)

    def get_existing_measures(self):
        if not self.risk:
            defined_measures = []
        else:
            defined_measures = (
                self.risk.get_pre_defined_measures(self.request) or "")
        try:
            saved_existing_measures = loads(
                self.context.existing_measures or "")
            # Backwards compat. We used to save dicts before we
            # switched to list of tuples.
            if isinstance(saved_existing_measures, dict):
                saved_existing_measures = [
                    (k, v) for (k, v) in saved_existing_measures.items()]

            saved_measure_texts = OrderedDict()
            for text, on in saved_existing_measures:
                saved_measure_texts.update({text: on})

            existing_measures = []
            # All the pre-defined measures are always shown, either
            # activated or deactivated
            for text in defined_measures:
                active = saved_measure_texts.get(text)
                if active is not None:
                    saved_measure_texts.pop(text)
                    existing_measures.append((text, active))
                else:
                    existing_measures.append((text, 0))

            # Finally, add the user-defined measures as well
            for text, on in saved_measure_texts.items():
                existing_measures.append((text, on))
        except ValueError:
            existing_measures = [
                (text, 0) for text in defined_measures
            ]
            self.context.existing_measures = safe_unicode(
                dumps(existing_measures))
        return existing_measures

    @property
    def use_problem_description(self):
        risk = self.request.survey.restrictedTraverse(
            self.context.zodb_path.split("/"))
        text = risk.problem_description
        return bool(text and text.strip())

    @property
    def is_custom_risk(self):
        return getattr(self.context, 'is_custom_risk', False)

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


class ActionPlanView(BrowserView):
    """Logic for creating new action plans.
    """

    phase = "actionplan"
    variation_class = "variation-risk-assessment"
    # The question filter will find modules AND risks
    question_filter = model.ACTION_PLAN_FILTER
    # The risk filter will only find risks
    risk_filter = model.RISK_PRESENT_OR_TOP5_FILTER
    # Skip evaluation?
    # The default value is False, can be overwritten by certain conditions
    skip_evaluation = False
    # Which fields should be skipped? Default are none, i.e. show all
    skip_fields = []
    # What extra style to use for buttons like "Add measure". Default is None.
    style_buttons = None

    @property
    @memoize
    def webhelpers(self):
        return self.context.restrictedTraverse('webhelpers')

    def get_existing_measures(self):
        if not self.use_existing_measures:
            return {}
        if not self.risk or not IRisk.providedBy(self.risk):
            defined_measures = []
        else:
            defined_measures = (
                self.risk.get_pre_defined_measures(self.request) or "")
        try:
            saved_existing_measures = (
                self.context.existing_measures and
                loads(self.context.existing_measures) or [])
            # Backwards compat. We used to save dicts before we
            # switched to list of tuples.
            if isinstance(saved_existing_measures, dict):
                saved_existing_measures = [
                    (k, v) for (k, v) in saved_existing_measures.items()]

            saved_measure_texts = OrderedDict()
            for text, on in saved_existing_measures:
                saved_measure_texts.update({text: on})

            existing_measures = []
            # Pick the pre-defined measures first
            for text in defined_measures:
                active = saved_measure_texts.get(text)
                if active is not None:
                    # Only add the measures that are active
                    if active:
                        existing_measures.append((text, 1))
                    saved_measure_texts.pop(text)

            # Finally, add the user-defined measures as well
            for text, active in saved_measure_texts.items():
                if active:
                    existing_measures.append((text, active))
        except ValueError:
            existing_measures = [
                (text, 0) for text in defined_measures
            ]
            self.context.existing_measures = safe_unicode(
                dumps(existing_measures))
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
        if IItalyActionPlanPhaseSkinLayer.providedBy(self.request):
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

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not (
            self.webhelpers.can_edit_session()
        ):
            return self.request.response.redirect(
                self.webhelpers.survey_url() + '/@@start'
            )
        if redirectOnSurveyUpdate(self.request):
            return
        context = aq_inner(self.context)

        if self.context.is_custom_risk:
            self.risk = self.context
        else:
            self.risk = self.request.survey.restrictedTraverse(
                context.zodb_path.split("/"))

        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.tti = getUtility(IToolTypesInfo)
        self.my_tool_type = get_tool_type(self.context)
        self.use_existing_measures = (
            asBool(settings.get('use_existing_measures', False)) and
            self.my_tool_type in self.tti.types_existing_measures
        )

        self.next_is_report = self.previous_is_identification = False
        # already compute "next" here, so that we can know in the template
        # if the next step might be the report phase, in which case we
        # need to switch off the sidebar
        next = FindNextQuestion(
            context, filter=self.risk_filter)
        if next is None:
            # We ran out of questions, proceed to the report
            url = "%s/report" % self.request.survey.absolute_url()
            self.next_is_report = True
        else:
            url = QuestionURL(
                self.request.survey, next, phase="actionplan")

        previous = FindPreviousQuestion(
            context, filter=self.risk_filter)
        if previous is None:
            # We ran out of questions, step back to identification phase
            previous_url = "%s/identification" % self.request.survey.absolute_url()
            self.previous_is_identification = True
        else:
            previous_url = QuestionURL(
                self.request.survey, previous, phase="actionplan")

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            session = Session()
            context.comment = reply.get("comment")
            context.priority = reply.get("priority")

            new_plans, changes = self.extract_plans_from_request()
            for plan in context.action_plans:
                session.delete(plan)
            context.action_plans.extend(new_plans)
            if changes:
                SessionManager.session.touch()

            if reply["next"] == "previous":
                url = previous_url
            return self.request.response.redirect(url)

        else:
            self.data = context
            if len(context.action_plans) == 0:
                self.data.empty_action_plan = [model.ActionPlan()]

        self.title = context.parent.title
        self.tree = getTreeData(
            self.request, context,
            filter=self.question_filter, phase="actionplan")

        # Italian special
        if IItalyActionPlanPhaseSkinLayer.providedBy(self.request):
            self.skip_evaluation = True
            measures_full_text = True
        else:
            measures_full_text = False
        if self.is_custom_risk:
            self.risk.description = u""
            number_images = 0
        else:
            number_images = getattr(self.risk, 'image', None) and 1 or 0
            if number_images:
                for i in range(2, 5):
                    number_images += getattr(
                        self.risk, 'image{0}'.format(i), None) and 1 or 0
            existing_measures = [
                txt.strip() for (txt, active) in self.get_existing_measures()
                if active]
            solutions = []
            for solution in self.risk.values():
                if not ISolution.providedBy(solution):
                    continue
                if measures_full_text:
                    match = u"%s: %s" % (
                        (getattr(solution, "description", "") or "").strip(),
                        (getattr(solution, "prevention_plan", "") or "").strip()
                    )
                else:
                    match = solution.description.strip()
                if match not in existing_measures:
                    solutions.append(
                        {
                            "description": StripMarkup(solution.description),
                            "action_plan": solution.action_plan,
                            "prevention_plan": solution.prevention_plan,
                            "requirements": solution.requirements,
                        }
                    )
            self.solutions = solutions

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
        return self.index()

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
        for i in range(0, len(form.get('measure', []))):
            measure = dict([p for p in form['measure'][i].items()
                            if p[1].strip()])
            form['action_plans'].append(measure)
            if len(measure):
                budget = measure.get("budget")
                budget = budget and budget.split(',')[0].split('.')[0]
                p_start = measure.get('planning_start')
                if p_start:
                    try:
                        datetime.datetime.strptime(p_start, '%Y-%m-%d')
                    except ValueError:
                        p_start = None
                p_end = measure.get('planning_end')
                if p_end:
                    try:
                        datetime.datetime.strptime(p_end, '%Y-%m-%d')
                    except ValueError:
                        p_end = None
                if measure.get('id', '-1') in existing_plans:
                    plan = existing_plans[measure.get('id')]
                    if (
                        measure.get("action_plan") != plan.action_plan or
                        measure.get("prevention_plan") != plan.prevention_plan or  # noqa
                        measure.get("requirements") != plan.requirements or
                        measure.get("responsible") != plan .responsible or (
                            plan.budget and (budget != str(plan.budget)) or
                            plan.budget is None and budget
                        ) or (
                            (plan.planning_start and
                                p_start != plan.planning_start.strftime('%Y-%m-%d')) or  # noqa
                            (plan.planning_start is None and p_start)
                        ) or (
                            (plan.planning_end and
                                p_end != plan.planning_end.strftime('%Y-%m-%d')) or  # noqa
                            (plan.planning_end is None and p_end)
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
                        planning_start=p_start,
                        planning_end=p_end,
                    )
                )
        removed = len(existing_plans)
        changes = True
        if added == 0 and updated == 0 and removed == 0:
            IStatusMessage(self.request).add(
                _(u"No changes were made to measures in your action plan."),
                type='info'
            )
            changes = False
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
        return (new_plans, changes)


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


class ConfirmationDeleteRisk(BrowserView):
    """View name: @@confirmation-delete-risk
    """

    @property
    def risk_title(self):
        return self.context.title

    @property
    def risk_id(self):
        return self.context.id

    @property
    def form_action(self):
        return "{0}/@@delete-risk".format(
            aq_parent(self.context).absolute_url())

    def __call__(self, *args, **kwargs):
        ''' Before rendering check if we can find session title
        '''
        self.risk_title
        self.no_splash = True
        return super(ConfirmationDeleteRisk, self).__call__(*args, **kwargs)


class DeleteRisk(BrowserView):
    """View name: @@delete-session
    """

    def __call__(self):
        risk_id = self.request.form.get('risk_id', None)
        if risk_id:
            try:
                risk_id = int(risk_id)
            except ValueError:
                pass
            else:
                keep_ids = [
                    risk.id for risk in self.context.children().all()
                    if risk.id != risk_id]
                self.context.removeChildren(excluded=keep_ids)

        self.request.response.redirect(self.context.absolute_url())
