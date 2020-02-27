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
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import getTreeData
from euphorie.client.subscribers.imagecropping import _initial_size
from euphorie.client import utils
from euphorie.content.risk import IRisk
from euphorie.content.solution import ISolution
from euphorie.content.survey import get_tool_type
from euphorie.content.survey import ISurvey
from euphorie.content.utils import IToolTypesInfo
from htmllaundry import StripMarkup
from io import BytesIO
from json import dumps
from json import loads
from plone import api
from plone.app.imaging.utils import getAllowedSizes
from plone.memoize.instance import memoize
from plone.namedfile import NamedBlobImage
from plone.namedfile.browser import DisplayFile
from plone.scale.scale import scaleImage
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sqlalchemy import and_
from z3c.appconfig.interfaces import IAppConfig
from z3c.appconfig.utils import asBool
from z3c.saconfig import Session
from zope.component import getUtility
from zope.publisher.interfaces import NotFound

import datetime
import PIL

IMAGE_CLASS = {0: "", 1: "twelve", 2: "six", 3: "four", 4: "three"}


class IdentificationView(BrowserView):
    """A view for displaying a question in the identification phase
    """

    default_template = ViewPageTemplateFile("templates/risk_identification.pt")
    custom_risk_template = ViewPageTemplateFile("templates/risk_identification_custom.pt")
    variation_class = "variation-risk-assessment"

    question_filter = None

    # default value is True, can be overwritten by certain conditions
    show_explanation_on_always_present_risks = True

    # default value for "always present" risks is "no", can be overwritten by certain conditions
    always_present_answer = "no"

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
        return api.content.get_view("webhelpers", self.context.aq_parent, self.request)

    @property
    @memoize
    def session(self):
        return self.webhelpers.traversed_session.session

    @property
    @memoize
    def survey(self):
        """ This is the survey dexterity object
        """
        return self.webhelpers._survey

    @property
    @memoize
    def next_question(self):
        return FindNextQuestion(
            self.context, dbsession=self.session, filter=self.question_filter
        )

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
    def italy_special(self):
        return self.webhelpers.country == "it"

    @property
    @memoize
    def skip_evaluation(self):
        """ Default value is False, but it can be tweaked in certain conditions"""
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
        """ In what circumstances will the Evaluation panel be shown, provided that
        evaluation is not skipped in general? """
        condition = "condition: answer=no"
        if self.italy_special and not self.skip_evaluation:
            condition = "condition: answer=no or answer=yes"
        return condition

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_edit_session:
            return self.request.response.redirect(
                "{session_url}/@@start".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return
        utils.setLanguage(self.request, self.survey, self.survey.language)

        appconfig = getUtility(IAppConfig)
        settings = appconfig.get("euphorie")
        self.tti = getUtility(IToolTypesInfo)
        self.my_tool_type = get_tool_type(self.context)
        self.use_existing_measures = (
            asBool(settings.get("use_existing_measures", False))
            and self.my_tool_type in self.tti.types_existing_measures
        )
        self.use_training_module = asBool(settings.get("use_training_module", False))

        if self.request.method == "POST":
            reply = self.request.form
            _next = reply.get("next", None)
            # In Safari browser we get a list
            if isinstance(_next, list):
                _next = _next.pop()
            # Don't persist anything if the user skipped the question
            if _next == "skip":
                return self.proceed_to_next(reply)
            old_values = {}
            for prop, default in self.monitored_properties.items():
                if prop == "existing_measures":
                    val = dumps(
                        [
                            entry
                            for entry in loads(getattr(self.context, prop, default))
                            if entry[1]
                        ]
                    )
                else:
                    val = getattr(self.context, prop, default)
                old_values[prop] = val
            answer = reply.get("answer", None)
            # If answer is not present in the request, do not attempt to set
            # any answer-related data, since the request might have come
            # from a sub-form.
            if answer:
                self.context.comment = reply.get("comment")
                self.context.postponed = answer == "postponed"
                if self.context.postponed:
                    self.context.identification = None
                else:
                    self.context.identification = answer
                    if getattr(self.risk, "type", "") in ("top5", "policy"):
                        self.context.priority = "high"
                    elif getattr(self.risk, "evaluation_method", "") == "calculated":
                        self.calculatePriority(self.risk, reply)
                    elif self.risk is None or self.risk.evaluation_method == "direct":
                        self.context.priority = reply.get("priority")

            if self.use_existing_measures and reply.get("handle_measures_in_place"):
                measures = self.get_existing_measures()
                new_measures = []
                seen = []
                for i, entry in enumerate(measures):
                    on = int(bool(reply.get("measure-{}".format(i))))
                    new_measures.append((entry[0], on))
                    if on:
                        seen.append(i)
                for k, val in reply.items():
                    if (
                        k.startswith("new-measure")
                        and isinstance(val, str)
                        and val.strip() != ""
                    ):
                        new_measures.append((val, 1))
                    elif k.startswith("present-measure") and val.strip() != "":
                        idx = k.rsplit("-", 1)[-1]
                        try:
                            idx = int(idx)
                        except (TypeError, ValueError):
                            continue
                        if idx in seen:
                            new_measures[idx] = (val, 1)

                # Only save the measures that are active
                self.context.existing_measures = safe_unicode(
                    dumps([entry for entry in new_measures if entry[1]])
                )

            # Check if there was a change. If yes, touch the session
            changed = False
            if self.use_training_module and reply.get("handle_training_notes"):
                self.context.training_notes = reply.get("training_notes")
                changed = True

            # This only happens on custom risks
            if reply.get("handle_custom_description"):
                self.context.custom_description = reply.get("custom_description")

            if reply.get("title"):
                self.context.title = reply.get("title")

            for prop, default in self.monitored_properties.items():
                if prop == "existing_measures":
                    val = dumps(
                        [
                            entry
                            for entry in loads(getattr(self.context, prop, default))
                            if entry[1]
                        ]
                    )
                else:
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

    @property
    @memoize
    def number_images(self):
        number_images = getattr(self.risk, "image", None) and 1 or 0
        if number_images:
            for i in range(2, 5):
                number_images += (
                    getattr(self.risk, "image{0}".format(i), None) and 1 or 0
                )
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
            number_files += getattr(self.risk, "file{0}".format(i), None) and 1 or 0
        self.has_files = number_files > 0
        self.has_legal = utils.HasText(getattr(self.risk, "legal_reference", None))
        self.show_resources = self.has_legal or self.has_files

        self.risk_number = self.context.number

        self.description_probability = _(
            u"help_default_probability",
            default=u"Indicate how "
            u"likely occurence of this risk is in a normal situation.",
        )
        self.description_frequency = _(
            u"help_default_frequency",
            default=u"Indicate how often this " u"risk occurs in a normal situation.",
        )
        self.description_severity = _(
            u"help_default_severity",
            default=u"Indicate the " u"severity if this risk occurs.",
        )

        tool_types = self.tti()
        tt_default = self.tti.default_tool_type
        tool_type_data = tool_types.get(self.my_tool_type, tool_types[tt_default])
        default_type_data = tool_types["classic"]
        self.show_existing_measures = False

        # Fill some labels with default texts
        self.answer_yes = default_type_data["answer_yes"]
        self.answer_no = default_type_data["answer_no"]
        self.answer_na = default_type_data["answer_na"]
        self.intro_extra = ""
        if self.is_custom_risk:
            self.intro_extra = tool_type_data.get("custom_intro_extra", "")
            if self.use_existing_measures:
                self.answer_yes = tool_type_data["answer_yes"]
                self.answer_no = tool_type_data["answer_no"]
        self.button_add_extra = tool_type_data.get("button_add_extra", "")
        self.intro_questions = tool_type_data.get("intro_questions", "")
        self.placeholder_add_extra = tool_type_data.get("placeholder_add_extra", "")
        self.button_remove_extra = ""
        if self.use_existing_measures:
            measures = self.get_existing_measures()
            # Only show the form to select and add existing measures if
            # at least one pre-existring measure is present
            # In this case, also change some labels
            if len(measures):
                self.show_existing_measures = True
                self.intro_extra = tool_type_data.get("intro_extra", "")
                self.button_remove_extra = tool_type_data.get("button_remove_extra", "")
                self.answer_yes = tool_type_data["answer_yes"]
                self.answer_no = tool_type_data["answer_no"]
                self.answer_na = tool_type_data["answer_na"]
            if not self.context.existing_measures:
                existing_measures = [(text, 0) for text in measures]
                self.context.existing_measures = safe_unicode(dumps(existing_measures))

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
                url = self.webhelpers.traversed_session.absolute_url() + "/@@actionplan"
                return self.request.response.redirect(url)

        elif _next == "add_custom_risk":
            sql_module = (
                Session.query(model.Module)
                .filter(
                    and_(
                        model.SurveyTreeItem.session == self.session,
                        model.Module.zodb_path == u"custom-risks",
                    )
                )
                .first()
            )
            if not sql_module:
                url = self.context.absolute_url() + "/@@identification"
                return self.request.response.redirect(url)

            view = api.content.get_view("identification", sql_module, self.request)
            risk_id = view.add_custom_risk()
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
    def get_existing_measures(self):
        if not self.risk:
            defined_measures = []
        else:
            defined_measures = self.risk.get_pre_defined_measures(self.request) or ""
        try:
            saved_existing_measures = loads(self.context.existing_measures or "")
            # Backwards compat. We used to save dicts before we
            # switched to list of tuples.
            if isinstance(saved_existing_measures, dict):
                saved_existing_measures = [
                    (k, v) for (k, v) in saved_existing_measures.items()
                ]

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
            existing_measures = [(text, 0) for text in defined_measures]
            self.context.existing_measures = safe_unicode(dumps(existing_measures))
        return existing_measures

    @property
    def use_problem_description(self):
        text = self.context.problem_description or ""
        return bool(text.strip())

    @property
    def is_custom_risk(self):
        return self.context.is_custom_risk

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
            "{}/@@identification".format(self.context.absolute_url())
        )

    def __call__(self):
        if self.request.form.get("image"):
            image = self.request.form["image"]
            new_data = image.read()
            if self.context.image_data != new_data:
                try:
                    PIL.Image.open(BytesIO(new_data))
                except IOError:
                    api.portal.show_message(
                        _(
                            "Invalid file format for image. Please use PNG, JPEG or GIF."
                        ),
                        request=self.request,
                        type="warning",
                    )
                    return self.redirect()
                self.context.image_data = new_data
                self.context.image_data_scaled = None
            new_name = safe_unicode(image.filename)
            if self.context.image_filename != new_name:
                self.context.image_filename = new_name
        elif self.request.form.get("image-remove"):
            self.context.image_data = None
            self.context.image_filename = u""
        return self.redirect()


class ImageDisplay(DisplayFile):
    """ Return the image stored in the risk (if present).
    Allows also to get the image scaled if invoked like:

    ../@@image-display/image_large/${here/image_filename}
    """

    def get_or_create_image_scaled(self):
        """ Get the image scaled
        """
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


class ActionPlanView(BrowserView):
    """Logic for creating new action plans.
    """

    phase = "actionplan"
    variation_class = "variation-risk-assessment"
    # The question filter will find modules AND risks
    question_filter = model.ACTION_PLAN_FILTER
    # The risk filter will only find risks
    risk_filter = model.RISK_PRESENT_OR_TOP5_FILTER
    # Which fields should be skipped? Default are none, i.e. show all
    skip_fields = []
    # What extra style to use for buttons like "Add measure". Default is None.
    style_buttons = None

    @property
    @memoize
    def webhelpers(self):
        return self.context.restrictedTraverse("webhelpers")

    @property
    @memoize
    def survey(self):
        """ This is the survey dexterity object
        """
        return self.webhelpers._survey

    @property
    @memoize
    def session(self):
        return self.webhelpers.traversed_session.session

    @property
    @memoize
    def skip_evaluation(self):
        """ Default value is False, but it can be tweaked in certain conditions"""
        if self.italy_special and (
            (
                self.risk
                and (self.risk.type == "top5" or self.risk.evaluation_method == "fixed")
            )
            or self.is_custom_risk
        ):
            return True
        return False

    def get_existing_measures(self):
        if not self.use_existing_measures:
            return {}
        if not self.risk or not IRisk.providedBy(self.risk):
            defined_measures = []
        else:
            defined_measures = self.risk.get_pre_defined_measures(self.request) or ""
        try:
            saved_existing_measures = (
                self.context.existing_measures
                and loads(self.context.existing_measures)
                or []
            )
            # Backwards compat. We used to save dicts before we
            # switched to list of tuples.
            if isinstance(saved_existing_measures, dict):
                saved_existing_measures = [
                    (k, v) for (k, v) in saved_existing_measures.items()
                ]

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
            existing_measures = [(text, 0) for text in defined_measures]
            self.context.existing_measures = safe_unicode(dumps(existing_measures))
        return existing_measures

    @property
    def risk_present(self):
        return self.context.identification == "no"

    @property
    def risk_postponed(self):
        return self.context.identification is None and (
            (self.italy_special and self.context.postponed) or True
        )

    @property
    def is_custom_risk(self):
        return self.context.is_custom_risk

    @property
    def italy_special(self):
        return self.webhelpers.country == "it"

    @property
    def use_problem_description(self):
        if self.is_custom_risk:
            return False
        if self.italy_special:
            return False
        text = self.risk.problem_description or ""
        return bool(text.strip())

    def _extractViewData(self):
        """Extract the data from the current context and build a data structure
        that is usable by the view.
        """

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
    def risk(self):
        if self.is_custom_risk:
            return self.context
        return self.context.aq_parent.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/")
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
                    number_images += (
                        getattr(self.risk, "image{0}".format(i), None) and 1 or 0
                    )

        return number_images

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_edit_session:
            return self.request.response.redirect(
                "{session_url}/@@start".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return
        context = aq_inner(self.context)
        utils.setLanguage(self.request, self.survey, self.survey.language)

        appconfig = getUtility(IAppConfig)
        settings = appconfig.get("euphorie")
        self.tti = getUtility(IToolTypesInfo)
        self.my_tool_type = get_tool_type(self.context)
        self.use_existing_measures = (
            asBool(settings.get("use_existing_measures", False))
            and self.my_tool_type in self.tti.types_existing_measures
        )

        self.next_is_report = self.previous_is_identification = False
        # already compute "next" here, so that we can know in the template
        # if the next step might be the report phase, in which case we
        # need to switch off the sidebar
        next_question = FindNextQuestion(
            context, dbsession=self.session, filter=self.risk_filter
        )
        if next_question is None:
            # We ran out of questions, proceed to the report
            url = "{session_url}/@@report".format(
                session_url=self.webhelpers.traversed_session.absolute_url()
            )
            self.next_is_report = True
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
            self.previous_is_identification = True

        if self.request.method == "POST":
            reply = self.request.form
            session = Session()
            context.comment = reply.get("comment")
            context.priority = reply.get("priority")

            new_plans, changes = self.extract_plans_from_request()
            for plan in context.action_plans:
                session.delete(plan)
            context.action_plans.extend(new_plans)
            if changes:
                self.session.touch()

            if reply["next"] == "previous":
                url = previous_url
            return self.request.response.redirect(url)

        else:
            self.data = context
            if len(context.action_plans) == 0:
                self.data.empty_action_plan = [model.ActionPlan()]

        self.title = context.parent.title

        # Italian special
        if self.is_custom_risk:
            self.risk.description = u""
            self.risk.evaluation_method = u""
        if self.italy_special:
            measures_full_text = True
        else:
            measures_full_text = False
        if not self.is_custom_risk:
            existing_measures = [
                txt.strip() for (txt, active) in self.get_existing_measures() if active
            ]
            solutions = []
            for solution in self.risk.values():
                if not ISolution.providedBy(solution):
                    continue
                description = (
                    getattr(solution, "description", "") or "").strip()
                prevention_plan = (
                    getattr(solution, "prevention_plan", "") or "").strip()
                match = description
                if measures_full_text and prevention_plan:
                    match = u"%s: %s" % (match, prevention_plan)
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

        self.image_class = IMAGE_CLASS[self.number_images]
        self.risk_number = self.context.number
        self.delete_confirmation = api.portal.translate(_(
            u"Are you sure you want to delete this measure? This action can "
            u"not be reverted."),
        )
        self.override_confirmation = api.portal.translate(_(
            u"The current text in the fields 'Action plan', 'Prevention plan' and "
            u"'Requirements' of this measure will be overwritten. This action cannot be "
            u"reverted. Are you sure you want to continue?"),
        )
        self.message_date_before = api.portal.translate(_(
            u"error_validation_before_end_date",
            default=u"This date must be on or before the end date."),
        )
        self.message_date_after = api.portal.translate(_(
            u"error_validation_after_start_date",
            default=u"This date must be on or after the start date."),
        )
        self.message_positive_number = api.portal.translate(_(
            u"error_validation_positive_whole_number",
            default=u"This value must be a positive whole number."),
        )
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
        for i in range(0, len(form.get("measure", []))):
            measure = dict([p for p in form["measure"][i].items() if p[1].strip()])
            form["action_plans"].append(measure)
            if len(measure):
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
                        measure.get("action_plan") != plan.action_plan
                        or measure.get("prevention_plan") != plan.prevention_plan
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
            changes = False
        return (new_plans, changes)


def calculate_priority(db_risk, risk):
    """Update the risk priority.

    This method can be used for risks using a calculated evaluation method
    to determine the priority absed on the subquestions.
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
            return getattr(parent, "evaluation_algorithm", u"kinney")
    else:
        return u"kinney"


class ConfirmationDeleteRisk(BrowserView):
    """View name: @@confirmation-delete-risk
    """

    no_splash = True

    @property
    def risk_title(self):
        return self.context.title

    @property
    def risk_id(self):
        return self.context.id

    @property
    def form_action(self):
        return "{0}/@@delete-risk".format(aq_parent(self.context).absolute_url())

    def __call__(self, *args, **kwargs):
        """ Before rendering check if we can find session title
        """
        self.risk_title
        return super(ConfirmationDeleteRisk, self).__call__(*args, **kwargs)


class DeleteRisk(BrowserView):
    """View name: @@delete-session
    """

    def __call__(self):
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

        self.request.response.redirect(
            "{session_url}/@@identification".format(
                session_url=self.context.absolute_url()
            )
        )
