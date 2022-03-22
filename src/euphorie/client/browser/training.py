# coding=utf-8
from collections import OrderedDict
from datetime import date
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import survey
from euphorie.client import utils
from euphorie.client import utils as client_utils
from euphorie.client.model import Training
from json import dumps
from json import loads
from logging import getLogger
from plone import api
from plone.memoize.instance import memoize
from plone.memoize.view import memoize as view_memoize
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from random import shuffle
from sqlalchemy.orm.exc import NoResultFound
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import markdown


logger = getLogger(__name__)


class TrainingSlide(BrowserView):
    """Template / macro to hold the training slide markup
    Currently not active in default Euphorie
    """
    heading_measures = _("header_measures", default="Measures")

    @property
    @view_memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @view_memoize
    def session(self):
        """Return the session for this context/request"""
        return self.context.session

    @property
    @memoize
    def is_custom(self):
        return "custom-risks" in self.context.zodb_path

    @property
    @memoize
    def item_type(self):
        return self.context.type

    @property
    @memoize
    def zodb_elem(self):
        if self.is_custom:
            return None
        return self.context.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/")
        )

    @property
    @memoize
    def risk_type(self):
        elem = self.zodb_elem
        if not elem:
            return ""
        return getattr(elem, "type", "")

    @property
    @memoize
    def for_download(self):
        return "for_download" in self.request and self.request["for_download"]

    @property
    @memoize
    def number(self):
        if self.is_custom:
            num_elems = self.context.number.split(".")
            number = ".".join(["Ω"] + num_elems[1:])
        else:
            number = self.context.number
        if self.item_type == "module":
            number = "{}.0".format(number)
        return number

    @property
    def number_id(self):
        return self.number.replace(".", "-")

    @property
    def slide_title(self):
        if self.is_custom and self.item_type == "module":
            return client_utils.get_translated_custom_risks_title(self.request)
        return self.context.title

    @property
    def slide_template(self):
        if self.item_type == "module":
            return "template-module"
        # there seems to be a profile template, don't when that should be used.
        return "template-default"

    @property
    def slide_type(self):
        # Perhaps this will not be needed any more...
        return self.item_type

    @property
    def slide_date(self):
        return date.today().strftime("%Y-%m-%d")

    @property
    def department(self):
        # XXX tbd - maybe in webhelpers?
        return "-"

    @property
    def description(self):
        if self.is_custom:
            return markdown.markdown(
                getattr(self.context, "custom_description", "") or ""
            )
        return self.zodb_elem.description or ""

    @property
    def training_notes(self):
        training_notes = getattr(self.context, "comment", "") or ""
        if self.for_download:
            training_notes = markdown.markdown(training_notes)
        if self.webhelpers.check_markup(training_notes):
            return training_notes

    @property
    def measures(self):
        if self.item_type != "risk":
            return {}
        measures = OrderedDict()
        for measure in list(self.context.in_place_standard_measures) + list(
            self.context.in_place_custom_measures
            + list(self.context.standard_measures)
            + list(self.context.custom_measures)
        ):
            if not measure.action:
                continue
            measures.update(
                {
                    measure.id: {
                        "action": self.webhelpers.get_safe_html(measure.action),
                        "active": measure.used_in_training,
                    }
                }
            )

        return measures

    @property
    def image(self):
        if self.is_custom:
            if not getattr(self.context, "image_data", None):
                return None
            _view = self.context.__of__(
                self.webhelpers.traversed_session.aq_parent["custom-risks"]
            ).restrictedTraverse("image-display")
            return _view.get_or_create_image_scaled()
        image = self.zodb_elem.image and self.zodb_elem.image.data or None
        if image and self.for_download:
            try:
                scales = self.zodb_elem.restrictedTraverse("images", None)
                if scales:
                    if self.item_type == "module":
                        scale_name = "training_title"
                    else:
                        scale_name = "training"
                    scale = scales.scale(fieldname="image", scale=scale_name)
                    if scale and scale.data:
                        image = scale.data.data
            except Exception:
                image = None
                logger.warning(
                    "Image data could not be fetched on %s", self.context.absolute_url()
                )
        return image

    @property
    def image_urls(self):
        urls = []
        if self.is_custom:
            if not getattr(self.context, "image_data", None):
                return None
            urls.append(
                f"{self.webhelpers.traversed_session.absolute_url()}/"
                f"{'/'.join(self.context.short_path)}"
                f"/@@image-display/training_export?name=${self.context.image_filename}"
            )
            return urls
        field_names = ["image"]
        scale_name = "training_title"
        if self.item_type == "risk":
            field_names.extend(["image2", "image3", "image4"])
            scale_name = "training"
        for fname in field_names:
            image = getattr(self.zodb_elem, fname, None)
            if image and image.data:
                urls.append(
                    f"{self.zodb_elem.absolute_url()}/@@images/{fname}/{scale_name}"
                )
        return urls

    def slide_contents(self, standalone=False):

        return {
            "slide_type": self.item_type,
            "slide_template": self.slide_template,
            "measures": self.measures,
            "training_notes": self.training_notes,
        }


class TrainingView(BrowserView, survey._StatusHelper):
    """The view that shows the main-menu Training module"""

    variation_class = "variation-risk-assessment"
    skip_unanswered = False
    for_download = False
    more_menu_contents = []
    heading_measures = _("header_measures", default="Measures")

    @property
    @view_memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @view_memoize
    def session(self):
        """Return the session for this context/request"""
        return self.context.session

    @memoize
    def get_or_create_training(self):
        """Return the training for this session"""
        account_id = self.webhelpers.get_current_account().id
        session_id = self.webhelpers.session_id
        try:
            return (
                Session.query(Training)
                .filter(
                    Training.session_id == session_id, Training.account_id == account_id
                )
                .one()
            )
        except NoResultFound:
            pass
        status = "in_progress" if self.questions else "correct"
        training = Training(
            account_id=account_id,
            session_id=session_id,
            status=status,
            time=datetime.now(),
            answers="{}",
        )
        Session.add(training)
        return training

    @property
    @view_memoize
    def training_status(self):
        return self.get_or_create_training().status

    @property
    @view_memoize
    def question_intro_url(self):
        survey = self.webhelpers._survey
        if not getattr(survey, "enable_web_training", False):
            return ""
        view_name = "slide_question_success"
        if survey.listFolderContents(
            {"portal_type": "euphorie.training_question"}
        ) and self.training_status not in ("correct", "success"):
            view_name = "slide_question_intro"
        return "{}/@@{}".format(self.context.absolute_url(), view_name)

    @property
    @view_memoize
    def questions(self):
        survey = self.webhelpers._survey
        return survey.listFolderContents({"portal_type": "euphorie.training_question"})

    @property
    def enable_training_questions(self):
        """Explicit property that can be overwritten in subpackages"""
        return bool(self.question_intro_url)

    def slicePath(self, path):
        while path:
            yield path[:3].lstrip("0")
            path = path[3:]

    @property
    @view_memoize
    def title_image(self):
        try:
            return self.context.aq_parent.external_site_logo.data
        except AttributeError:
            logger.warning(
                "Image data (logo) could not be fetched on survey  %s",
                self.context.absolute_url(),
            )
            return

    @property
    @view_memoize
    def tool_image_url(self):
        survey = self.context.aq_parent
        if getattr(survey, "image", None):
            return f"{survey.absolute_url()}/@@images/image/large"

    @property
    def logo_url(self):
        logo = self.webhelpers.get_sector_logo
        if logo:
            return f"{self.webhelpers.portal_url}/{logo.url}"
        return f"{self.webhelpers.portal_url}/++resource++euphorie.resources/media/oira-logo-colour.png"  # noqa: E501

    @property
    @view_memoize
    def slide_data(self):
        modules = self.getModulePaths()
        risks = self.getRisks(modules, skip_unanswered=self.skip_unanswered)
        seen_modules = []
        data = OrderedDict()
        for (module, risk) in risks:
            module_path = module.path
            if module_path not in seen_modules:
                module_in_context = module.__of__(self.webhelpers.traversed_session)
                module_in_context.REQUEST["for_download"] = self.for_download
                _view = module_in_context.restrictedTraverse("training_slide")
                slide_contents = _view.slide_contents()
                data.update(
                    {
                        module_path: {
                            "item": module_in_context,
                            "training_view": _view,
                            "slide_contents": slide_contents,
                        }
                    }
                )
                seen_modules.append(module_path)
            risk_in_context = risk.__of__(self.webhelpers.traversed_session)
            risk_in_context.REQUEST["for_download"] = self.for_download
            _view = risk_in_context.restrictedTraverse("training_slide")
            slide_contents = _view.slide_contents()
            data.update(
                {
                    risk.path: {
                        "item": risk_in_context,
                        "training_view": _view,
                        "slide_contents": slide_contents,
                    }
                }
            )
        return data

    @property
    def slide_total_count(self):
        count = 0
        for data in self.slide_data.values():
            count += 1
            for measure_id in data["slide_contents"]["measures"]:
                if data["slide_contents"]["measures"][measure_id]["active"]:
                    count += 1
                    break
            if (
                data["item"].type != "module"
                and data["slide_contents"]["training_notes"]
            ):
                count += 1
        return count

    def __call__(self):
        if self.webhelpers.redirectOnSurveyUpdate():
            return

        survey = self.webhelpers._survey
        utils.setLanguage(self.request, survey, survey.language)

        # XXXX This whole block is not being used at the moment, since the
        # training page does not post anything.
        # We don't yet know where the handling of measure selection will happen
        if self.request.environ["REQUEST_METHOD"] == "POST":
            active_measures = set()
            for entry in self.request.form:
                # Case A: the user has modified the notes of the "text" training slides
                if entry.startswith("training_notes"):
                    index = entry.split("-")[-1]
                    sql_item = self.slide_data[index]["item"]
                    value = safe_unicode(self.request[entry])
                    sql_item.training_notes = value
                # an entry of this kind is relevant for Case B below
                elif entry.startswith("measure"):
                    measure_id = entry.split("-")[-1]
                    active_measures.add(measure_id)
            # Case B: the user has selected or de-selected a measure
            # from one of the "measures" training slides
            if "handle_training_measures_for" in self.request.form:
                index = self.request.form["handle_training_measures_for"].split("-")[-1]
                sql_item = self.slide_data[index]["item"]
                view = self.slide_data[index]["training_view"]
                all_measures = set([str(key) for key in view.existing_measures.keys()])
                deselected_measures = all_measures - active_measures
                session = Session()
                if active_measures:
                    session.execute(
                        "UPDATE action_plan set used_in_training=true "
                        "where id in ({ids})".format(ids=",".join(active_measures))
                    )
                if deselected_measures:
                    session.execute(
                        "UPDATE action_plan set used_in_training=false "
                        "where id in ({ids})".format(ids=",".join(deselected_measures))
                    )
                self.webhelpers.traversed_session.session.touch()
                # We need to compute the URL manually from the "path"
                # given in the sql-element
                # Reason: the sql_item has the context of our session,
                # but is not aware of the full parent-hierarchy of module/submodule
                self.request.RESPONSE.redirect(
                    "{session}/{path}/@@training_slide".format(
                        session=self.context.absolute_url(),
                        path="/".join(self.slicePath(sql_item.path)),
                    )
                )
            self.webhelpers.traversed_session.session.touch()

        self.request.RESPONSE.addHeader("Cache-Control", "public,max-age=60")
        return self.index()


class SlideQuestionIntro(TrainingView):
    """The slide that introduces the questions"""

    @property
    @view_memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def survey_title(self):
        return self.webhelpers._survey.title

    def first_question_url(self):
        """Check the questions in the survey and take the first one"""
        if not self.questions:
            return ""
        return "{base_url}/@@slide_question/{slide_id}".format(
            base_url=self.context.absolute_url(), slide_id=self.questions[0].getId()
        )


@implementer(IPublishTraverse)
class SlideQuestion(SlideQuestionIntro):
    """The view for a question slide, the question id has to be passed
    as a traversal parameter
    """

    def publishTraverse(self, request, name):
        self.question_id = name
        return self

    @property
    @view_memoize
    def question(self):
        """The question we want to display"""
        return self.webhelpers._survey[self.question_id]

    @property
    @view_memoize
    def answers(self):
        """Return the randomized answers for this question"""
        question = self.question
        answers = [
            question.right_answer,
            question.wrong_answer_1,
            question.wrong_answer_2,
        ]
        shuffle(answers)
        return answers

    @property
    def progress(self):
        """Return a progress indicator, something like 2/3"""
        idx = self.questions.index(self.question)
        return "{}/{}".format(idx + 1, len(self.questions))

    @property
    @view_memoize
    def previous_question(self):
        idx = self.questions.index(self.question)
        if idx == 0:
            return
        try:
            return self.questions[idx - 1]
        except IndexError:
            pass

    @property
    @view_memoize
    def next_question(self):
        idx = self.questions.index(self.question)
        try:
            return self.questions[idx + 1]
        except IndexError:
            pass

    @property
    def next_url(self):
        """Go to next question (if we have one) or to the success or try again slides"""
        next_question = self.next_question
        if next_question:
            next_slide = "slide_question/{}".format(next_question.getId())
        elif self.get_or_create_training().status == "correct":
            next_slide = "slide_question_success"
        else:
            next_slide = "slide_question_try_again"
        return "{}/@@{}".format(self.context.absolute_url(), next_slide)

    def initialize_training(self):
        """Initialize the training.
        This is particularly important if the user starts again the training
        after a first attempt
        """
        training = self.get_or_create_training()
        training.answers = "{}"
        training.status = "in_progress"
        training.time = datetime.now()

    def post(self):
        if not self.previous_question:
            self.initialize_training()
        training = self.get_or_create_training()
        answer = safe_unicode(self.request.form["answer"])
        answer_history = loads(training.answers)
        answer_history[self.question_id] = answer == self.question.right_answer
        training.answers = dumps(answer_history)
        training.time = datetime.now()
        if not self.next_question:
            training.status = "correct" if all(answer_history.values()) else "failed"

    def posted(self):
        if self.request.method != "POST":
            return False
        self.post()
        return True

    def validate(self):
        previous_question = self.previous_question
        if not previous_question:
            return
        training = self.get_or_create_training()
        try:
            answers = loads(training.answers)
        except ValueError:
            answers = {}
        if not answers:
            raise Unauthorized(_("You should start the training from the beginning"))
        if previous_question.getId() not in answers:
            raise Unauthorized(_("It seems you missed a slide"))

    def __call__(self):
        self.validate()
        if self.posted():
            return self.request.response.redirect(self.next_url)
        return super(SlideQuestion, self).__call__()


class SlideQuestionSuccess(SlideQuestionIntro):
    variation_class = ""

    def post(self):
        pass

    def __call__(self):
        training = self.get_or_create_training()
        if training.status not in ("correct", "success"):
            raise Unauthorized("You do not own the certificate")
        if self.request.method == "POST":
            return self.post()
        return super(SlideQuestionSuccess, self).__call__()


class SlideQuestionTryAgain(SlideQuestionIntro):
    @property
    def failed_questions(self):
        training = self.get_or_create_training()
        try:
            answers = loads(training.answers)
        except ValueError:
            answers = {}
        return [
            question.title
            for question in self.questions
            if not answers.get(question.getId())
        ]


class MyTrainingsPortlet(BrowserView):
    columns = "1"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def my_unfinished_trainings(self):
        account_id = self.webhelpers.get_current_account().id
        return [
            session
            for session in (
                Session.query(Training)
                .filter(Training.account_id == account_id, Training.status != "correct")
                .order_by(Training.time.desc())
                .all()
            )
            if session.session.tool
        ]

    @property
    @memoize
    def my_certificates(self):
        account_id = self.webhelpers.get_current_account().id
        return [
            session
            for session in (
                Session.query(Training)
                .filter(Training.account_id == account_id, Training.status == "correct")
                .order_by(Training.time.desc())
                .all()
            )
            if session.session.tool
        ]
