"""
Risk
----

Views for the identification and action plan phases.
"""

from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie import MessageFactory as _
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.interfaces import CustomRisksModifiedEvent
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.subscribers.imagecropping import _initial_size
from euphorie.content.survey import get_tool_type
from euphorie.content.survey import ISurvey
from euphorie.content.utils import IToolTypesInfo
from euphorie.content.utils import parse_scaled_answers
from euphorie.content.utils import ToolTypesInfo
from euphorie.htmllaundry.utils import strip_markup
from io import BytesIO
from plone import api
from plone.base.utils import safe_text
from plone.memoize.instance import memoize
from plone.memoize.view import memoize_contextless
from plone.namedfile import NamedBlobImage
from plone.namedfile.browser import DisplayFile
from plone.scale.scale import scaleImage
from Products.CMFPlone.utils import getAllowedSizes
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sqlalchemy import and_
from z3c.saconfig import Session
from zope.component import getUtility
from zope.deprecation import deprecate
from zope.event import notify
from zope.publisher.interfaces import NotFound

import datetime
import PIL


IMAGE_CLASS = {0: "", 1: "twelve", 2: "six", 3: "four", 4: "three"}


class RiskBase(BrowserView):
    # Which fields should be skipped? Default are none, i.e. show all
    skip_fields = []
    # What extra style to use for buttons like "Add measure". Default is None.
    style_buttons = None

    def __call__(self):
        pass

    @property
    @memoize
    def delete_confirmation(self):
        return api.portal.translate(
            _(
                "Are you sure you want to delete this measure? This action can "
                "not be reverted."
            )
        )

    @property
    @memoize
    def override_confirmation(self):
        return api.portal.translate(
            _(
                "The current text in the fields 'Action plan', 'Prevention plan' and "
                "'Requirements' of this measure will be overwritten. "
                "This action cannot be reverted. Are you sure you want to continue?"
            )
        )

    @property
    @memoize
    def message_date_after(self):
        return api.portal.translate(
            _(
                "error_validation_after_start_date",
                default="This date must be on or after the start date.",
            )
        )

    @property
    @memoize
    def message_positive_number(self):
        return api.portal.translate(
            _(
                "error_validation_positive_whole_number",
                default="This value must be a positive whole number.",
            )
        )

    @property
    @memoize
    def message_date_before(self):
        return api.portal.translate(
            _(
                "error_validation_before_end_date",
                default="This date must be on or before the end date.",
            )
        )

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context.aq_parent, self.request)

    @property
    @memoize
    def session(self):
        return self.webhelpers.traversed_session.session

    @property
    @memoize
    def survey(self):
        """This is the survey dexterity object."""
        return self.webhelpers._survey

    @property
    @memoize_contextless
    def tti(self) -> ToolTypesInfo:
        return getUtility(IToolTypesInfo)

    @property
    @memoize
    def my_tool_type(self) -> str:
        return get_tool_type(self.survey)

    @property
    @memoize
    def use_existing_measures(self) -> bool:
        return (
            api.portal.get_registry_record(
                "euphorie.use_existing_measures", default=False
            )
            and self.my_tool_type in self.tti.types_existing_measures
        )

    @property
    @memoize
    def italy_special(self):
        return self.webhelpers.country == "it"

    @property
    def is_custom_risk(self):
        return self.context.is_custom_risk

    @property
    def solutions_provided_by_tool(self):
        """Return all the solutions that are defined for this risk in the
        CMS."""
        return getattr(self.risk, "_solutions", [])

    @property
    @memoize
    def solutions_available_for_action_plan(self):
        """Return those pre-defined solutions that are not already marked as
        being in place.

        Those remaining solutions are available as suggestions in the
        Action Plan
        """
        if self.is_custom_risk:
            return []
        existing_measure_ids = [
            measure.solution_id for measure in self.get_existing_measures()
        ]
        solutions = []
        for solution in self.solutions_provided_by_tool:
            solution_id = solution.id
            if solution_id not in existing_measure_ids:
                solutions.append(
                    {
                        "description": strip_markup(solution.description),
                        "action": getattr(solution, "action", "") or "",
                        "requirements": solution.requirements,
                        "id": solution_id,
                    }
                )
        return solutions

    @memoize
    def get_existing_measures(self):
        return list(self.context.in_place_standard_measures) + list(
            self.context.in_place_custom_measures
        )

    @property
    def active_standard_measures(self):
        if self.is_custom_risk:
            return {}
        return {
            getattr(measure, "solution_id", ""): measure
            for measure in self.context.standard_measures
        }

    @property
    def solutions_condition(self):
        return "condition: not ({})".format(
            " and ".join(
                [
                    "sm-%s" % solution["id"]
                    for solution in self.solutions_available_for_action_plan
                ]
            )
        )

    def extract_plans_from_request(self):
        """Create new ActionPlan objects by parsing the Request."""
        context = aq_inner(self.context)
        form = self.request.form
        context_measures = context.standard_measures + context.custom_measures
        if form.get("handle_training_measures"):
            # Gather all (database-) ids of the active measures. That means, those
            # measures where the checkboxes are ticked in the training configuration.
            # Remember: a measure that has been deselected (checkbox unticked)
            # does not appear in the REQUEST
            active_measures = []
            for entry in form:
                if entry.startswith("training-measure") and entry.find("-") >= 0:
                    measure_id = entry.split("-")[-1]
                    active_measures.append(measure_id)
            # Get the ids of all measures-in-place and map them to the solution-ids
            # Remember: the solution-id is the ZODB-id of the respective solution
            # inside the risk in the CMS. We us it to identify the standard measures.
            # The custom measures will not have a solution-id
            all_measures = {
                str(measure.id): measure.solution_id for measure in context_measures
            }
            # The following 2 mappings will be used if the handling of measures in
            # place is also part of this request (further down)
            # Make a mapping of solution-id to used-in-training state for the
            # standard measures
            saved_solutions = {
                v: k in active_measures for (k, v) in all_measures.items() if v
            }
            # Make a mapping of database-id to used-in-training state for the
            # custom measures
            saved_custom_measures = {
                k: k in active_measures for (k, v) in all_measures.items() if not v
            }
        else:
            # The following 2 mappings will be used if the handling of measures in
            # place is also part of this request (further down)
            # We do not have training configuration in the REQUEST. We need
            # to build the mapping of solution-id to used-in-training state
            # via the information stored in the the database...
            saved_solutions = {
                plan.solution_id: plan.used_in_training
                for plan in self.context.standard_measures
            }
            # ... and also for the custom measures
            saved_custom_measures = {
                str(plan.id): plan.used_in_training
                for plan in self.context.custom_measures
            }
        new_plans = []
        added = 0
        updated = 0
        existing_plans = {}
        form["action_plans"] = []
        for plan in context_measures:
            existing_plans[str(plan.id)] = plan
        for i in range(0, len(form.get("measure", []))):
            measure = dict([p for p in form["measure"][i].items() if p[1].strip()])
            form["action_plans"].append(measure)
            if len(measure):
                plan_type = measure.get("plan_type", "measure_custom")
                if plan_type == "measure_standard":
                    used_in_training = saved_solutions.get(
                        measure.get("solution_id"), True
                    )
                else:
                    used_in_training = saved_custom_measures.get(
                        measure.get("id"), True
                    )
                solution_id = measure.get("solution_id", None)
                if plan_type == "measure_standard" and not form.get(
                    "sm-%s" % solution_id
                ):
                    continue
                action = measure.get("action", "").strip()
                if not self.webhelpers.check_markup(action):
                    continue
                budget = measure.get("budget")
                budget = budget and budget.split(",")[0].split(".")[0]
                p_start = measure.get("planning_start")
                if p_start:
                    try:
                        datetime.datetime.strptime(p_start, "%Y-%m-%d")
                    except ValueError:
                        p_start = None
                p_end = measure.get("planning_end")
                if p_end:
                    try:
                        datetime.datetime.strptime(p_end, "%Y-%m-%d")
                    except ValueError:
                        p_end = None
                if measure.get("id", "-1") in existing_plans:
                    plan = existing_plans[measure.get("id")]
                    if (
                        action != plan.action
                        or measure.get("requirements") != plan.requirements  # noqa
                        or measure.get("responsible") != plan.responsible
                        or (
                            plan.budget
                            and (budget != str(plan.budget))
                            or plan.budget is None
                            and budget
                        )
                        or (
                            (
                                plan.planning_start
                                and p_start != plan.planning_start.strftime("%Y-%m-%d")
                            )
                            or (plan.planning_start is None and p_start)  # noqa
                        )
                        or (
                            (
                                plan.planning_end
                                and p_end != plan.planning_end.strftime("%Y-%m-%d")
                            )
                            or (plan.planning_end is None and p_end)  # noqa
                        )
                    ):
                        updated += 1
                    del existing_plans[measure.get("id")]
                else:
                    added += 1
                new_plans.append(
                    model.ActionPlan(
                        action=self.webhelpers.get_safe_html(measure.get("action")),
                        requirements=measure.get("requirements"),
                        responsible=measure.get("responsible"),
                        budget=budget,
                        planning_start=p_start,
                        planning_end=p_end,
                        plan_type=plan_type,
                        solution_id=solution_id,
                        used_in_training=used_in_training,
                    )
                )
        removed = len(existing_plans)
        changes = True
        if added == 0 and updated == 0 and removed == 0:
            changes = False
        return (new_plans, changes)

    @property
    def action_plan_instruction_text(self):
        if self.get_existing_measures():
            # Case: measures-in-place==true, solutions==true
            if self.solutions_available_for_action_plan:
                return api.portal.translate(
                    _(
                        "action_measures_true_solutions_true",
                        default="Select or describe any further measure to reduce the risk.",  # noqa: E501  # noqa: E501
                    )
                )
            # Case: measures-in-place==true, solutions==false
            else:
                return api.portal.translate(
                    _(
                        "action_measures_true_solutions_false",
                        default="Describe any further measure to reduce the risk.",
                    )
                )
        else:
            # Case: measures-in-place==false, solutions==true
            if self.solutions_available_for_action_plan:
                return api.portal.translate(
                    _(
                        "action_measures_false_solutions_true",
                        default="Select or describe the specific measures required to reduce the risk.",  # noqa: E501
                    )
                )
            # Case: measures-in-place==false, solutions==false
            else:
                return api.portal.translate(
                    _(
                        "action_measures_false_solutions_false",
                        default="Describe the specific measures required to reduce the risk.",  # noqa: E501
                    )
                )

    def _get_next(self, reply):
        _next = reply.get("next", None)
        # In Safari browser we get a list
        if isinstance(_next, list):
            _next = _next.pop()
        return _next

    @property
    def notes_placeholder(self):
        if self.webhelpers.use_training_module:
            return _(
                "placeholder_comment_field_training",
                default="These notes will be visible in the report and the training. "
                "Use it for anything else you might want to write about this risk.",
            )
        else:
            return _(
                "placeholder_comment_field",
                default="These notes will be visible in the report. Use it for "
                "anything else you might want to write about this risk.",
            )

    @property
    @memoize
    def scaled_answers(self):
        """Get values and answers if the scaled_answers field is used.

        This returns a list of dictionaries.
        """
        if not getattr(self.risk, "use_scaled_answer", False):
            return []
        return parse_scaled_answers(self.risk.scaled_answers)


class IdentificationView(RiskBase):
    """A view for displaying a question in the identification phase."""

    default_template = ViewPageTemplateFile("templates/risk_identification.pt")
    custom_risk_template = ViewPageTemplateFile(
        "templates/risk_identification_custom.pt"
    )
    variation_class = "variation-risk-assessment"

    question_filter = None

    # If False, an always_present risk will not have an explanation that no
    # identification is necessary
    # Default value is True, can be overwritten by certain conditions
    show_explanation_on_always_present_risks = True

    # default value for "always present" risks is "no",
    # can be overwritten by certain conditions
    always_present_answer = "no"

    monitored_properties = {
        "scaled_answer": None,
        "identification": None,
        "postponed": None,
        "frequency": None,
        "severity": None,
        "priority": None,
        "comment": "",
        "training_notes": None,
        "custom_description": None,
    }

    @property
    @memoize
    def risk(self):
        if self.is_custom_risk:
            return
        return self.context.aq_parent.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/")
        )

    @property
    @memoize
    def default_collapsible_sections(self):
        settings = self.webhelpers.content_country_obj
        default_collapsible_sections = getattr(
            settings,
            "risk_default_collapsible_sections",
            ["collapsible_section_information"],
        )
        return default_collapsible_sections

    @memoize
    def get_collapsible_section_state(self, collapsible_section_name):
        return (
            ""
            if f"collapsible_section_{collapsible_section_name}"
            in self.default_collapsible_sections
            else "closed"
        )

    @property
    @memoize
    def next_question(self):
        return FindNextQuestion(
            self.context, dbsession=self.session, filter=self.question_filter
        )

    @property
    @memoize
    def skip_evaluation(self):
        """Default value is False, but it can be tweaked in certain
        conditions."""
        if self.italy_special and (
            (
                self.risk
                and (self.risk.type == "top5" or self.risk.evaluation_method == "fixed")
            )
            or self.is_custom_risk
        ):
            return True
        return False

    @property
    @memoize
    def evaluation_condition(self):
        """In what circumstances will the Evaluation panel be shown, provided
        that evaluation is not skipped in general?

        If you are using scaled answers instead of yes/no, you likely want to
        override this.
        """
        condition = "condition: answer=no"
        if self.italy_special and not self.skip_evaluation:
            condition = "condition: answer=no or answer=yes"
        return condition

    @property
    def action_plan_condition(self):
        """In what circumstances will the integrated Action Plan be shown."""
        condition = "condition: answer=no"
        if not self.is_custom_risk and (
            self.risk.type == "top5" or self.risk.risk_always_present
        ):
            # No condition, that means, it will always be shown
            return None
        return condition

    def __call__(self):
        # Render the page only if the user has inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                self.context.aq_parent.absolute_url() + "/@@start"
            )
        super().__call__()
        self.check_render_condition()

        utils.setLanguage(self.request, self.survey, self.survey.language)

        if self.request.method == "POST":
            reply = self.request.form
            if not self.webhelpers.can_edit_session:
                return self.proceed_to_next(reply)
            _next = self._get_next(reply)
            # Don't persist anything if the user skipped the question
            if _next == "skip":
                return self.proceed_to_next(reply)
            old_values = {}
            for prop, default in self.monitored_properties.items():
                val = getattr(self.context, prop, default)
                old_values[prop] = val

            self.set_answer_data(reply)

            session = Session()
            changed = self.set_measure_data(reply, session)

            if reply.get("answer", None):
                # If answer is not present in the request, do not attempt to set
                # any action-related data, since the request might have come
                # from a sub-form.
                if self.webhelpers.integrated_action_plan:
                    new_plans, changes = self.extract_plans_from_request()
                    for plan in (
                        self.context.standard_measures + self.context.custom_measures
                    ):
                        session.delete(plan)
                    self.context.action_plans.extend(new_plans)
                    changed = changes or changed

            # This only happens on custom risks
            if reply.get("handle_custom_description"):
                self.context.custom_description = self.webhelpers.check_markup(
                    reply.get("custom_description")
                )

            if reply.get("title"):
                self.context.title = reply.get("title")

            if not changed:
                for prop, default in self.monitored_properties.items():
                    val = getattr(self.context, prop, None)
                    if val and val != old_values[prop]:
                        changed = True
                        break
            if changed:
                self.session.touch()

            return self.proceed_to_next(reply)

        else:
            self._prepare_risk()
            if self.is_custom_risk:
                next = FindNextQuestion(
                    self.context, self.context.session, filter=self.question_filter
                )
                self.has_next_risk = next or False
            return self.template()

    @property
    def template(self):
        if self.is_custom_risk:
            return self.custom_risk_template
        return self.default_template

    @property
    def tree(self):
        return getTreeData(self.request, self.context)

    @property
    def title(self):
        return self.session.title

    def check_render_condition(self):
        # Render the page only if the user can inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                "{session_url}/@@start".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return

    @deprecate(
        "This method does not do anything anymore. The set attributes have been moved to properties."  # noqa: E501
    )
    def set_parameter_values(self):
        """This method will be removed. It was used to set the values of:

        - tti
        - my_tool_type
        - use_existing_measures

        These values are now properties of the RiskBase class.
        """
        pass

    def get_identification_from_scaled_answer(self, scaled_answer):
        """Determine the yes/no identification based on the scaled answer.

        A simplistic implementation could be:

          return "no" if scaled_answer in ("1", "2") else "yes"

        You likely want to override this if you actually use scaled answers,
        so by default we return nothing, making the identification empty.
        """
        pass

    def set_answer_data(self, reply):
        """Set answer data from the reply.

        For years the only answer possibilities were yes, no, n/a or postponed.
        Now we may have an extra field scaled_answer, for answers in the
        range of (usually) 1-5.
        We might want to merge these two possibilities, but for now they are
        separate.
        Currently, when scaled_answer is in the reply, we also get
        'postponed' as answer.  We can ignore this: scaled_answer is filled
        in, so the answer is not postponed.
        We make sure that either 'identification' is set (yes/no) or
        'scaled_answer' is set (1-5), and the other None.
        Or both None in the case the answer is really postponed.
        """
        answer = reply.get("answer", None)
        # If answer is not present in the request, do not attempt to set
        # any answer-related data, since the request might have come
        # from a sub-form.
        if not answer:
            return
        self.context.comment = self.webhelpers.get_safe_html(reply.get("comment"))
        scaled_answer = reply.get("scaled_answer", None)
        if scaled_answer:
            # We have an answer on the scale of 1-5 (or similar).
            self.context.scaled_answer = scaled_answer
            self.context.postponed = False
            self.context.identification = self.get_identification_from_scaled_answer(
                scaled_answer
            )
        else:
            self.context.scaled_answer = None
            self.context.postponed = answer == "postponed"
            if self.context.postponed:
                self.context.identification = None
                return
            self.context.identification = answer
        if getattr(self.risk, "type", "") in ("top5", "policy"):
            self.context.priority = "high"
        elif getattr(self.risk, "evaluation_method", "") == "calculated":
            self.calculatePriority(self.risk, reply)
        elif self.risk is None or self.risk.evaluation_method == "direct":
            self.context.priority = reply.get("priority")

    def set_measure_data(self, reply, session):
        changed = False
        # Case: the user has selected or de-selected a measure
        # from the training configuration
        if reply.get("handle_training_measures"):
            # Gather all (database-) ids of the active measures. That means, those
            # measures where the checkboxes are ticked in the training configuration.
            # Remember: a measure that has been deselected (checkbox unticked)
            # does not appear in the REQUEST
            active_measures_in_place = []
            active_measures_planned = []
            for entry in reply:
                if (
                    entry.startswith("training-measure-in-place")
                    and entry.find("-") >= 0
                ):
                    measure_id = entry.split("-")[-1]
                    active_measures_in_place.append(measure_id)
                elif (
                    entry.startswith("training-measure-planned")
                    and entry.find("-") >= 0
                ):
                    measure_id = entry.split("-")[-1]
                    active_measures_planned.append(measure_id)
            # Get the ids of all measures-in-place and map them to the solution-ids
            # Remember: the solution-id is the ZODB-id of the respective solution
            # inside the risk in the CMS. We us it to identify the standard measures.
            # The custom measures will not have a solution-id
            all_in_place_measures = {
                str(measure.id): measure.solution_id
                for measure in list(self.context.in_place_standard_measures)
                + list(self.context.in_place_custom_measures)
            }
            all_planned_measures = {
                str(measure.id): measure.solution_id
                for measure in list(self.context.standard_measures)
                + list(self.context.custom_measures)
            }
            # The following 2 mappings will be used if the handling of measures in
            # place is also part of this request (further down)
            # Make a mapping of solution-id to used-in-training state for the
            # standard measures
            saved_in_place_solutions = {
                v: k in active_measures_in_place
                for (k, v) in all_in_place_measures.items()
                if v
            }
            # Make a mapping of database-id to used-in-training state for the
            # custom measures
            saved_in_place_custom_measures = {
                k: k in active_measures_in_place
                for (k, v) in all_in_place_measures.items()
                if not v
            }
            # Additionally store the (database) ids of all measures that have been
            # deactivated. In case we do not handle measures in place in this
            # request further down, we need to make sure that those measues get
            # set to used_in_training=False at the end of this method
            deselected_in_place_measures = [
                k for k in all_in_place_measures if k not in active_measures_in_place
            ]
            deselected_planned_measures = [
                k for k in all_planned_measures if k not in active_measures_planned
            ]
        else:
            # The following 2 mappings will be used if the handling of measures in
            # place is also part of this request (further down)
            # We do not have training configuration in the REQUEST. We need
            # to build the mapping of solution-id to used-in-training state
            # via the information stored in the the database...
            saved_in_place_solutions = {
                plan.solution_id: plan.used_in_training
                for plan in self.context.in_place_standard_measures
            }
            # ... and also for the custom measures
            saved_in_place_custom_measures = {
                str(plan.id): plan.used_in_training
                for plan in self.context.in_place_custom_measures
            }
            deselected_in_place_measures = deselected_planned_measures = []
            active_measures_in_place = active_measures_planned = []

        if reply.get("handle_measures_in_place"):
            new_measures = []
            # First, check which of the standard solutions were selected
            for solution in self.solutions_provided_by_tool:
                # If the solution was already added as a measure, retrieve the info
                # whether it was de-selected for the training, so that we don't
                # forcefully activate all measures for the training again.
                used_in_training = saved_in_place_solutions.get(solution.id, True)
                if reply.get("measure-standard-%s" % solution.id):
                    new_measures.append(
                        model.ActionPlan(
                            action=solution.action,
                            requirements=solution.requirements,
                            plan_type="in_place_standard",
                            solution_id=solution.id,
                            used_in_training=used_in_training,
                        )
                    )
            # Clean up, remove all standard in-place measures. The active
            # ones will be created freshly again below
            for plan in self.context.in_place_standard_measures:
                session.delete(plan)

            # Now loop over the form data to find out which new custom measures
            # to add and which already present custom measures to keep.
            # (Present custom measures are deleted and added again, since their
            # text might have changed. But their original order is preserved.)
            new_custom_measures = {}
            for k, val in reply.items():
                if (
                    k.startswith("new-measure")
                    and isinstance(val, str)
                    and val.strip() != ""
                ):
                    new_custom_measures[k] = model.ActionPlan(
                        action=val, plan_type="in_place_custom"
                    )
                elif k.startswith("measure-custom"):
                    _id = k.rsplit("-", 1)[-1]
                    new_custom_measures[_id] = model.ActionPlan(
                        action=val,
                        plan_type="in_place_custom",
                        used_in_training=saved_in_place_custom_measures.get(_id, True),
                    )
                # This only happens on custom risks
                elif k.startswith("present-measure") and val.strip() != "":
                    _id = k.rsplit("-", 1)[-1]
                    if int(bool(reply.get(f"measure-{_id}"))):
                        new_measures.append(
                            model.ActionPlan(
                                action=val,
                                plan_type="in_place_custom",
                                used_in_training=saved_in_place_custom_measures.get(
                                    _id, True
                                ),
                            )
                        )
            # Now add the custom measures in their correct order
            for k in sorted(new_custom_measures.keys()):
                new_measures.append(new_custom_measures[k])
            # Delete all custom in-place measures
            for plan in self.context.in_place_custom_measures:
                session.delete(plan)
                changed = True

            if new_measures:
                self.context.action_plans.extend(new_measures)
                changed = True
        else:
            # If we did not handle any measures in place, check if we need to take
            # care of training measures that need to be activated or deactivated
            if active_measures_in_place:
                session.execute(
                    "UPDATE action_plan set used_in_training=true where id in ({ids})".format(  # noqa: E501
                        ids=",".join(active_measures_in_place)
                    )
                )
                changed = True
            if deselected_in_place_measures:
                session.execute(
                    "UPDATE action_plan set used_in_training=false where id in ({ids})".format(  # noqa: E501
                        ids=",".join(deselected_in_place_measures)
                    )
                )
                changed = True
        # In case we're not dealing with an integrated action plan, de-/ activate
        # planned measures as necessary
        if not self.webhelpers.integrated_action_plan:
            if active_measures_planned:
                session.execute(
                    "UPDATE action_plan set used_in_training=true where id in ({ids})".format(  # noqa: E501
                        ids=",".join(active_measures_planned)
                    )
                )
                changed = True
            if deselected_planned_measures:
                session.execute(
                    "UPDATE action_plan set used_in_training=false where id in ({ids})".format(  # noqa: E501
                        ids=",".join(deselected_planned_measures)
                    )
                )
                changed = True
        return changed

    @property
    @memoize
    def number_images(self):
        number_images = getattr(self.risk, "image", None) and 1 or 0
        if number_images:
            for i in range(2, 5):
                number_images += getattr(self.risk, f"image{i}", None) and 1 or 0
        return number_images

    def _prepare_risk(self):
        has_risk_description = (
            self.risk and utils.HasText(self.risk.description)
        ) or getattr(self.context, "custom_description", "")
        self.show_info = getattr(self.risk, "image", None) or (
            self.risk is None or utils.HasText(self.risk.description)
        )
        self.image_class = IMAGE_CLASS[self.number_images]
        number_files = 0
        for i in range(1, 5):
            number_files += getattr(self.risk, f"file{i}", None) and 1 or 0
        self.has_files = number_files > 0
        self.has_legal = utils.HasText(getattr(self.risk, "legal_reference", None))
        self.show_resources = self.has_legal or self.has_files

        self.risk_number = self.context.number

        self.description_probability = _(
            "help_default_probability",
            default="Indicate how "
            "likely occurence of this risk is in a normal situation.",
        )
        self.description_frequency = _(
            "help_default_frequency",
            default="Indicate how often this " "risk occurs in a normal situation.",
        )
        self.description_severity = _(
            "help_default_severity",
            default="Indicate the " "severity if this risk occurs.",
        )

        tool_types = self.tti()
        tt_default = self.tti.default_tool_type
        tool_type_data = tool_types.get(self.my_tool_type, tool_types[tt_default])
        default_type_data = tool_types["classic"]
        self.show_existing_measures = False

        # Fill some labels with default texts
        self.answer_yes = tool_type_data.get(
            "answer_yes", default_type_data["answer_yes"]
        )
        self.answer_no = tool_type_data.get("answer_no", default_type_data["answer_no"])
        self.answer_na = tool_type_data.get("answer_na", default_type_data["answer_na"])
        self.intro_extra = ""
        self.intro_questions = tool_type_data.get("intro_questions", "")
        if getattr(self.risk, "risk_always_present", False):
            self.placeholder_add_extra = tool_type_data.get(
                "placeholder_add_extra_always_present", ""
            )
            self.button_add_extra = tool_type_data.get(
                "button_add_extra_always_present", ""
            )
        else:
            self.placeholder_add_extra = tool_type_data.get("placeholder_add_extra", "")
            self.button_add_extra = tool_type_data.get("button_add_extra", "")

        self.button_remove_extra = ""
        if self.use_existing_measures:
            measures = self.get_existing_measures_with_activation()
            # Only show the form to select and add existing measures if
            # at least one pre-existring measure is present
            # In this case, also change some labels
            if len(measures):
                self.show_existing_measures = True
                if getattr(self.risk, "risk_always_present", False):
                    self.intro_extra = tool_type_data.get(
                        "intro_extra_always_present", ""
                    )
                    self.button_remove_extra = tool_type_data.get(
                        "button_remove_extra_always_present", ""
                    )
                else:
                    self.intro_extra = tool_type_data.get("intro_extra", "")
                    self.button_remove_extra = tool_type_data.get(
                        "button_remove_extra", ""
                    )
                if self.webhelpers.integrated_action_plan:
                    self.answer_yes = tool_type_data.get(
                        "answer_yes_integrated_ap", tool_type_data["answer_yes"]
                    )
                    self.answer_no = tool_type_data.get(
                        "answer_no_integrated_ap", tool_type_data["answer_no"]
                    )
                else:
                    self.answer_yes = tool_type_data["answer_yes"]
                    self.answer_no = tool_type_data["answer_no"]
                self.answer_na = tool_type_data["answer_na"]
        if self.is_custom_risk:
            self.intro_extra = tool_type_data.get("custom_intro_extra", "")
            self.intro_questions = tool_type_data.get("custom_intro_questions", "")
            self.button_add_extra = tool_type_data.get("custom_button_add_extra", "")
            self.placeholder_add_extra = tool_type_data.get(
                "custom_placeholder_add_extra", ""
            )

        survey = self.context.aq_parent.aq_parent
        if getattr(survey, "enable_custom_evaluation_descriptions", False):
            if survey.evaluation_algorithm != "french":
                custom_dp = getattr(survey, "description_probability", "") or ""
                self.description_probability = (
                    custom_dp.strip() or self.description_probability
                )
            custom_df = getattr(survey, "description_frequency", "") or ""
            self.description_frequency = custom_df.strip() or self.description_frequency
            custom_ds = getattr(survey, "description_severity", "") or ""
            self.description_severity = custom_ds.strip() or self.description_severity

        # compute training side template
        self.slide_template = (
            (has_risk_description or self.number_images)
            and "template-two-column"
            or "template-default"
        )

    @property
    @memoize
    def previous_question(self):
        return FindPreviousQuestion(
            self.context, dbsession=self.session, filter=self.question_filter
        )

    def proceed_to_next(self, reply):
        _next = reply.get("next", None)
        # In Safari browser we get a list
        if isinstance(_next, list):
            _next = _next.pop()
        if _next == "previous":
            target = self.previous_question
            if target is None:
                # We ran out of questions, step back to intro page
                url = "{session_url}/@@identification".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
                return self.request.response.redirect(url)
        elif _next in ("next", "skip"):
            target = self.next_question
            if target is None:
                # We ran out of questions, proceed to the action plan
                if self.webhelpers.use_action_plan_phase:
                    next_view_name = "@@actionplan"
                elif self.webhelpers.use_consultancy_phase:
                    next_view_name = "@@consultancy"
                else:
                    next_view_name = "@@report"
                base_url = self.webhelpers.traversed_session.absolute_url()
                url = f"{base_url}/{next_view_name}"
                return self.request.response.redirect(url)

        elif _next == "add_custom_risk" and self.webhelpers.can_edit_session:
            sql_module = (
                Session.query(model.Module)
                .filter(
                    and_(
                        model.SurveyTreeItem.session == self.session,
                        model.Module.zodb_path == "custom-risks",
                    )
                )
                .first()
            )
            if not sql_module:
                url = self.context.absolute_url() + "/@@identification"
                return self.request.response.redirect(url)

            view = api.content.get_view("identification", sql_module, self.request)
            view.add_custom_risk()
            notify(CustomRisksModifiedEvent(self.context.aq_parent))
            risk_id = self.context.aq_parent.children().count()
            # Construct the path to the newly added risk: We know that there
            # is only one custom module, so we can take its id directly. And
            # to that we can append the risk id.
            url = "{session_url}/{module}/{risk}/@@identification".format(
                session_url=self.webhelpers.traversed_session.absolute_url(),
                module=sql_module.getId(),
                risk=risk_id,
            )
            return self.request.response.redirect(url)
        elif _next == "actionplan":
            url = self.webhelpers.traversed_session.absolute_url() + "/@@actionplan"
            return self.request.response.redirect(url)
        # stay on current risk
        else:
            target = self.context
        url = ("{session_url}/{path}/@@identification").format(
            session_url=self.webhelpers.traversed_session.absolute_url(),
            path="/".join(target.short_path),
        )
        return self.request.response.redirect(url)

    @memoize
    def get_existing_measures_with_activation(self):
        saved_standard_measures = {
            getattr(measure, "solution_id", ""): measure
            for measure in self.context.in_place_standard_measures
        }
        existing_measures = []
        for solution in self.solutions_provided_by_tool:
            if getattr(self.survey, "measures_text_handling", "full") == "simple":
                title = solution.action
                text = ""
            else:
                title = solution.description
                text = solution.action
            existing_measures.append(
                {
                    "title": title,
                    "text": text,
                    "active": solution.id in saved_standard_measures,
                    "solution_id": solution.id,
                    "plan_type": "in_place_standard",
                }
            )
        for measure in self.context.in_place_custom_measures:
            existing_measures.append(
                {
                    "text": measure.action,
                    "active": True,
                    "solution_id": measure.id,
                    "plan_type": "in_place_custom",
                }
            )
        return existing_measures

    @property
    def use_problem_description(self):
        text = self.context.problem_description or ""
        return bool(text.strip())

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


class ImageUpload(BrowserView):
    def redirect(self):
        return self.request.response.redirect(
            f"{self.context.absolute_url()}/@@identification"
        )

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context.aq_parent, self.request)

    def __call__(self):
        if not self.webhelpers.can_view_session:
            # The user cannot call this view to go the sessions overview.
            return self.request.response.redirect(self.webhelpers.client_url)
        if self.request.form.get("image"):
            image = self.request.form["image"]
            new_data = image.read()
            if self.context.image_data != new_data:
                try:
                    pil_img = PIL.Image.open(BytesIO(new_data))
                    pil_img.crop()
                except OSError:
                    api.portal.show_message(
                        _(
                            "Invalid file format for image. Please use PNG, JPEG or GIF."  # noqa: E501
                        ),
                        request=self.request,
                        type="warning",
                    )
                    return self.redirect()
                self.context.image_data = new_data
                self.context.image_data_scaled = None
            new_name = safe_text(image.filename)
            if self.context.image_filename != new_name:
                self.context.image_filename = new_name
        elif self.request.form.get("image-remove"):
            self.context.image_data = None
            self.context.image_filename = ""
        return self.redirect()


class ImageDisplay(DisplayFile):
    """Return the image stored in the risk (if present). Allows also to get the
    image scaled if invoked like:

    ../@@image-display/image_large/${here/image_filename}
    """

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context.aq_parent, self.request)

    def get_or_create_image_scaled(self):
        """Get the image scaled."""
        if self.context.image_data_scaled:
            return self.context.image_data_scaled
        image = PIL.Image.open(BytesIO(self.context.image_data))
        image_format = image.format or self.DEFAULT_FORMAT
        params = list(image.size)
        scale = getAllowedSizes().get(self.fieldname, (1500, 791))
        params.extend(scale)
        box = _initial_size(*params)

        cropped_image = image.crop(box).resize(scale)
        cropped_image_io = BytesIO()
        cropped_image.save(cropped_image_io, image_format, quality=100)
        scaled_image_io, scaled_image_format, scaled_image_size = scaleImage(
            cropped_image_io, width=scale[0], height=scale[1]
        )
        if isinstance(scaled_image_io, bytes):
            self.context.image_data_scaled = scaled_image_io
        else:
            self.context.image_data_scaled = scaled_image_io.getvalue()
        return self.context.image_data_scaled

    def _getFile(self):
        if self.context.image_data is None:
            raise NotFound(self, self.fieldname, self.request)

        if self.fieldname and "training" in self.fieldname:
            image_data = self.get_or_create_image_scaled()
        else:
            image_data = self.context.image_data

        return NamedBlobImage(image_data, filename=self.context.image_filename)

    def __call__(self):
        if not self.webhelpers.can_view_session:
            # The user cannot call this view to go the sessions overview.
            return self.request.response.redirect(self.webhelpers.client_url)
        return super().__call__()


class ActionPlanView(RiskBase):
    """Logic for creating new action plans."""

    phase = "actionplan"
    variation_class = "variation-risk-assessment"
    # The question filter will find modules AND risks
    question_filter = model.ACTION_PLAN_FILTER
    # The risk filter will only find risks
    risk_filter = model.RISK_PRESENT_OR_TOP5_FILTER

    @property
    @memoize
    def risk(self):
        if self.is_custom_risk:
            return self.context
        return self.context.aq_parent.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/")
        )

    @property
    @memoize
    def skip_evaluation(self):
        """Default value is False, but it can be tweaked in certain
        conditions."""
        if self.italy_special and (
            (
                self.risk
                and (self.risk.type == "top5" or self.risk.evaluation_method == "fixed")
            )
            or self.is_custom_risk
        ):
            return True
        return False

    @property
    def risk_present(self):
        return self.context.identification == "no"

    @property
    def risk_postponed(self):
        return self.context.identification is None

    @property
    def use_problem_description(self):
        if self.is_custom_risk:
            return False
        if self.italy_special:
            return False
        text = self.risk.problem_description or ""
        return bool(text.strip())

    @property
    def scaled_answer_chosen(self):
        if not self.risk.use_scaled_answer:
            return ""
        if self.context.scaled_answer is None:
            return ""
        answer = self.context.scaled_answer
        # answer is a string like '1'.
        # Use it to find the textual representation of the answer.
        for info in self.scaled_answers:
            # Note: currently both info value and answer are strings ('1', '2', etc).
            if info["value"] == answer:
                return info
        return answer

    def _extractViewData(self):
        """Extract the data from the current context and build a data structure
        that is usable by the view."""

    def _fieldsToDate(self, year, month, day):
        if not day or not year:
            return None
        return datetime.date(year, month, day)

    @property
    def tree(self):
        return getTreeData(
            self.request, self.context, filter=self.question_filter, phase="actionplan"
        )

    @property
    @memoize
    def number_images(self):
        if self.is_custom_risk:
            return int(bool(self.context.image_filename))
        else:
            number_images = getattr(self.risk, "image", None) and 1 or 0
            if number_images:
                for i in range(2, 5):
                    number_images += getattr(self.risk, f"image{i}", None) and 1 or 0

        return number_images

    def __call__(self):
        super().__call__()
        # Render the page only if the user has inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                "{session_url}/@@start".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return
        context = aq_inner(self.context)
        utils.setLanguage(self.request, self.survey, self.survey.language)

        # already compute "next" here, so that we can know in the template
        # if the next step might be the report phase, in which case we
        # need to switch off the sidebar
        next_question = FindNextQuestion(
            context, dbsession=self.session, filter=self.risk_filter
        )
        if next_question is None:
            # We ran out of questions, proceed to the next phase
            url = "{session_url}/{next_view_name}".format(
                session_url=self.webhelpers.traversed_session.absolute_url(),
                next_view_name=(
                    "@@consultancy"
                    if self.webhelpers.use_consultancy_phase
                    else "@@report"
                ),
            )
        else:
            url = "{session_url}/{path}/@@actionplan".format(
                path="/".join(next_question.short_path),
                session_url=self.webhelpers.traversed_session.absolute_url(),
            )

        previous = FindPreviousQuestion(
            context, dbsession=self.session, filter=self.risk_filter
        )
        if previous is None:
            previous_url = "{session_url}/@@identification".format(
                session_url=self.webhelpers.traversed_session.absolute_url()
            )
        else:
            previous_url = "{session_url}/{path}/@@actionplan".format(
                path="/".join(previous.short_path),
                session_url=self.webhelpers.traversed_session.absolute_url(),
            )

        if self.request.method == "POST":
            reply = self.request.form
            if self.webhelpers.can_edit_session:
                session = Session()
                context.comment = self.webhelpers.get_safe_html(reply.get("comment"))
                context.priority = reply.get("priority")

                new_plans, changes = self.extract_plans_from_request()
                for plan in context.standard_measures + context.custom_measures:
                    session.delete(plan)
                context.action_plans.extend(new_plans)
                if changes:
                    self.session.touch()

            _next = self._get_next(reply)
            if _next == "previous":
                url = previous_url
            return self.request.response.redirect(url)

        self.title = context.parent.title

        if self.is_custom_risk:
            self.risk.description = ""
            self.risk.evaluation_method = ""

        self.image_class = IMAGE_CLASS[self.number_images]
        self.risk_number = self.context.number
        return self.index()


def calculate_priority(db_risk, risk):
    """Update the risk priority.

    This method can be used for risks using a calculated evaluation
    method to determine the priority absed on the subquestions.
    """
    assert risk.evaluation_method == "calculated"
    if risk.type in ["top5", "policy"]:
        db_risk.priority = "high"
    elif evaluation_algorithm(risk) == "french":
        priority = db_risk.frequency * db_risk.effect
        if priority < 10:
            db_risk.priority = "low"
        elif priority <= 45:
            db_risk.priority = "medium"
        else:
            db_risk.priority = "high"
    else:
        priority = db_risk.frequency * db_risk.effect * db_risk.probability
        if priority <= 15:
            db_risk.priority = "low"
        elif priority <= 50:
            db_risk.priority = "medium"
        else:
            db_risk.priority = "high"
    return db_risk.priority


def evaluation_algorithm(risk):
    for parent in aq_chain(aq_inner(risk)):
        if ISurvey.providedBy(parent):
            return getattr(parent, "evaluation_algorithm", "kinney")
    else:
        return "kinney"


class ConfirmationDeleteRisk(BrowserView):
    """View name: @@confirmation-delete-risk."""

    no_splash = True

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def risk_title(self):
        return self.context.title

    @property
    def risk_id(self):
        return self.context.id

    @property
    def form_action(self):
        return f"{aq_parent(self.context).absolute_url()}/@@delete-risk"

    def __call__(self, *args, **kwargs):
        """Before rendering check if we can find session title."""
        if not self.webhelpers.can_view_session:
            # The user cannot call this view to go the sessions overview.
            return self.request.response.redirect(self.webhelpers.client_url)
        self.risk_title
        return super().__call__(*args, **kwargs)


class DeleteRisk(BrowserView):
    """View name: @@delete-risk."""

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def __call__(self):
        if not self.webhelpers.can_view_session:
            # The user cannot call this view to go the sessions overview.
            return self.request.response.redirect(self.webhelpers.client_url)

        risk_id = self.request.form.get("risk_id", None)
        if risk_id:
            try:
                risk_id = int(risk_id)
            except ValueError:
                pass
            else:
                keep_ids = [
                    risk.id
                    for risk in self.context.children().all()
                    if risk.id != risk_id
                ]
                self.context.removeChildren(excluded=keep_ids)
                notify(CustomRisksModifiedEvent(self.context))

        self.request.response.redirect(
            "{session_url}/@@identification".format(
                session_url=self.context.absolute_url()
            )
        )
