from Acquisition import aq_base
from collections import OrderedDict
from datetime import date
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import survey
from euphorie.client import utils
from euphorie.client import utils as client_utils
from euphorie.client.model import Risk
from euphorie.client.model import Training
from euphorie.content.behaviors.hide_from_training import IHideFromTraining
from json import dumps
from json import loads
from logging import getLogger
from plone import api
from plone.base.utils import safe_text
from plone.memoize.instance import memoize
from plone.memoize.view import memoize as view_memoize
from Products.Five import BrowserView
from random import sample
from random import shuffle
from sqlalchemy.orm.exc import NoResultFound
from z3c.saconfig import Session
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import markdown


logger = getLogger(__name__)


class TrainingSlide(BrowserView):
    """Template / macro to hold the training slide markup Currently not active
    in default Euphorie."""

    @property
    @view_memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

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
        obj = self.context.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/"), None
        )
        if obj is None:
            logger.warning(
                "Could not traverse to: %r from %r",
                self.context.zodb_path,
                self.context.aq_parent,
            )
        return obj

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
            number = f"{number}.0"
        return number

    @property
    def number_id(self):
        number = self.number.replace(".", "-")
        if self.is_custom:
            number = number.replace("Ω", "omega")
        return number

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
        return getattr(self.zodb_elem, "description", "") or ""

    @property
    def training_notes(self):
        training_notes = getattr(self.context, "comment", "") or ""
        if self.for_download:
            training_notes = markdown.markdown(training_notes)
        if self.webhelpers.check_markup(training_notes):
            return training_notes

    @property
    def measures_in_place(self):
        if self.item_type != "risk":
            return {}
        measures = OrderedDict()
        for measure in list(self.context.in_place_standard_measures) + list(
            self.context.in_place_custom_measures
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
    def measures_planned(self):
        if self.item_type != "risk":
            return {}
        measures = OrderedDict()
        for measure in list(self.context.standard_measures) + list(
            self.context.custom_measures
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
    def measures(self):
        measures = self.measures_in_place
        measures.update(self.measures_planned)
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

        try:
            image = self.zodb_elem.image.data
        except AttributeError:
            image = None

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

    def slide_contents(self):
        return {
            "slide_type": self.item_type,
            "slide_template": self.slide_template,
            "measures_in_place": self.measures_in_place,
            "measures_planned": self.measures_planned,
            "measures": self.measures,  # BBB
            "training_notes": self.training_notes,
        }

    @property
    def existing_measures_training(self):
        measures = dict()
        for measure in list(self.context.in_place_standard_measures) + list(
            self.context.in_place_custom_measures
        ):
            measures.update(
                {
                    measure.id: {
                        "action": measure.action,
                        "active": measure.used_in_training,
                    }
                }
            )
        return measures

    @property
    def planned_measures_training(self):
        measures = dict()
        for measure in list(self.context.standard_measures) + list(
            self.context.custom_measures
        ):
            measures.update(
                {
                    measure.id: {
                        "action": measure.action,
                        "active": measure.used_in_training,
                    }
                }
            )
        return measures


class TrainingView(BrowserView, survey._StatusHelper):
    """The view that shows the main-menu Training module."""

    variation_class = "variation-risk-assessment"
    skip_unanswered = False
    for_download = False
    more_menu_contents = []
    heading_measures_in_place = _(
        "label_existing_measures", default="Already implemented measures"
    )
    heading_measures_planned = _("label_planned_measures", default="Planned measures")
    show_slide_byline = True

    @property
    @view_memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @view_memoize
    def session(self):
        """Return the session for this context/request."""
        return self.context.session

    @property
    @memoize
    def timestamp(self):
        return self.session.modified.strftime("%s%M%H%d%m")

    def get_initial_answers(self):
        """Pick a subset of questions, shuffle them, and initialize the answers
        with None."""
        survey = self.webhelpers._survey
        all_questions = survey.listFolderContents(
            {"portal_type": "euphorie.training_question"}
        )
        num_training_questions = min(
            getattr(survey, "num_training_questions", None) or len(all_questions),
            len(all_questions),
        )
        questions = sample(all_questions, k=num_training_questions)
        return {q.getId(): None for q in questions}

    def get_training_by_id(self, training_id):
        """Return the training for this session with the given id."""
        # check the session id to make sure we are not displaying a training in the
        # context of a different session
        session_id = self.webhelpers.session_id
        try:
            return (
                Session.query(Training)
                .filter(Training.session_id == session_id, Training.id == training_id)
                .one()
            )
        except NoResultFound as exc:
            raise NotFound from exc

    @memoize
    def get_or_create_training(self):
        """Return the current user's training for this session."""
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
        answers = self.get_initial_answers()
        status = "in_progress" if answers else "correct"

        training = Training(
            account_id=account_id,
            session_id=session_id,
            status=status,
            time=datetime.now(),
            answers=dumps(answers),
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
        if not getattr(aq_base(survey), "enable_test_questions", False):
            return ""
        view_name = "slide_question_success"
        if survey.listFolderContents(
            {"portal_type": "euphorie.training_question"}
        ) and self.training_status not in ("correct", "success"):
            view_name = "slide_question_intro"
        return f"{self.context.absolute_url()}/@@{view_name}"

    @property
    @view_memoize
    def question_ids(self):
        training = self.get_or_create_training()
        answer_history = loads(training.answers)
        return list(answer_history)

    @property
    def enable_training_questions(self):
        """Explicit property that can be overwritten in subpackages."""
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
        return f"{self.webhelpers.portal_url}/++resource++euphorie.resources/assets/oira/style/oira-logo-colour.svg"  # noqa: E501

    @property
    @view_memoize
    def slide_data(self):
        modules = self.getModulePaths()
        risks = self.getRisks(modules, skip_unanswered=self.skip_unanswered)
        seen_modules = []
        hidden_modules = []
        data = OrderedDict()
        for module, risk in risks:
            module_path = module.path
            if module_path in hidden_modules:
                continue
            if module_path not in seen_modules:
                # Get the ZODB representation of the module.
                zodb_module = self.webhelpers.traversed_session.restrictedTraverse(
                    module.zodb_path.split("/")
                )
                # Check if the module is allowed in trainings.
                if (
                    getattr(
                        IHideFromTraining(zodb_module, None),
                        "hide_from_training",
                        False,
                    )
                    is True
                ):
                    hidden_modules.append(module_path)
                    continue

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
            for measure_id in data["slide_contents"]["measures_in_place"]:
                if data["slide_contents"]["measures_in_place"][measure_id]["active"]:
                    count += 1
                    break
            for measure_id in data["slide_contents"]["measures_planned"]:
                if data["slide_contents"]["measures_planned"][measure_id]["active"]:
                    count += 1
                    break
            if (
                data["item"].type != "module"
                and data["slide_contents"]["training_notes"]
            ):
                count += 1
        return count

    def handle_measure_configuration(self, reply):
        session = Session()
        risk = session.query(Risk).filter(Risk.id == reply["risk_id"]).first()
        if not risk:
            return
        # Gather all (database-) ids of the active measures. That means, those
        # measures where the checkboxes are ticked in the training configuration.
        # Remember: a measure that has been deselected (checkbox unticked)
        # does not appear in the REQUEST
        active_measures_in_place = []
        active_measures_planned = []
        for entry in reply:
            if entry.startswith("training-measure-in-place") and entry.find("-") >= 0:
                measure_id = entry.split("-")[-1]
                active_measures_in_place.append(measure_id)
            elif entry.startswith("training-measure-planned") and entry.find("-") >= 0:
                measure_id = entry.split("-")[-1]
                active_measures_planned.append(measure_id)
        # Get the (database-) ids of all measures-in-place / planned measures
        all_in_place_measures = {
            str(measure.id)
            for measure in list(risk.in_place_standard_measures)
            + list(risk.in_place_custom_measures)
        }
        all_planned_measures = {
            str(measure.id)
            for measure in list(risk.standard_measures) + list(risk.custom_measures)
        }
        # Additionally store the (database-) ids of all measures that have been
        # deactivated.
        deselected_in_place_measures = [
            k for k in all_in_place_measures if k not in active_measures_in_place
        ]
        deselected_planned_measures = [
            k for k in all_planned_measures if k not in active_measures_planned
        ]

        changed = False
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
        if changed:
            self.webhelpers.traversed_session.session.touch()

    def __call__(self):
        if self.webhelpers.redirectOnSurveyUpdate():
            return

        survey = self.webhelpers._survey
        utils.setLanguage(self.request, survey, survey.language)

        if (
            self.request.environ["REQUEST_METHOD"] == "POST"
            and self.webhelpers.can_edit_session
        ):
            reply = self.request.form
            if "risk_id" in reply:
                self.handle_measure_configuration(reply)

        # XXX This is commented because it causes problems on logout, see:
        # - https://github.com/euphorie/Euphorie/issues/475
        #
        # We should come out with a better solution that does not require setting
        # the cache headers here.
        # self.request.RESPONSE.addHeader("Cache-Control", "public,max-age=60")
        return self.index()


class SlideQuestionIntro(TrainingView):
    """The slide that introduces the questions."""

    @property
    @view_memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def survey_title(self):
        return self.webhelpers._survey.title

    def first_question_url(self):
        """Check the questions in the survey and take the first one."""
        if not self.question_ids:
            return ""
        return "{base_url}/@@slide_question/{slide_id}".format(
            base_url=self.context.absolute_url(), slide_id=self.question_ids[0]
        )


@implementer(IPublishTraverse)
class SlideQuestion(SlideQuestionIntro):
    """The view for a question slide, the question id has to be passed as a
    traversal parameter."""

    def publishTraverse(self, request, name):
        self.question_id = name
        return self

    @property
    @view_memoize
    def question(self):
        """The question we want to display."""
        return self.webhelpers._survey[self.question_id]

    @property
    @view_memoize
    def answers(self):
        """Return the randomized answers for this question."""
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
        """Return a progress indicator, something like 2/3."""
        idx = self.question_ids.index(self.question_id)
        return f"{idx + 1}/{len(self.question_ids)}"

    @property
    @view_memoize
    def previous_question_id(self):
        idx = self.question_ids.index(self.question_id)
        if idx == 0:
            return
        try:
            return self.question_ids[idx - 1]
        except IndexError:
            pass

    @property
    @view_memoize
    def next_question_id(self):
        idx = self.question_ids.index(self.question_id)
        try:
            return self.question_ids[idx + 1]
        except IndexError:
            pass

    @property
    def next_url(self):
        """Go to next question (if we have one) or to the success or try again
        slides."""
        next_question_id = self.next_question_id
        if next_question_id:
            next_slide = f"slide_question/{next_question_id}"
        elif self.get_or_create_training().status == "correct":
            next_slide = "slide_question_success"
        else:
            next_slide = "slide_question_try_again"
        return f"{self.context.absolute_url()}/@@{next_slide}"

    def initialize_training(self):
        """Initialize the training.

        This is particularly important if the user starts again the
        training after a first attempt
        """
        training = self.get_or_create_training()
        answer_history = loads(training.answers)
        if not all([answer is None for answer in answer_history.values()]):
            answer_history = {q_id: None for q_id in answer_history}
            training.answers = dumps(answer_history)
        training.status = "in_progress" if answer_history else "correct"
        training.time = datetime.now()

    def post(self):
        if not self.previous_question_id:
            self.initialize_training()
        training = self.get_or_create_training()
        answer = safe_text(self.request.form["answer"])
        answer_history = loads(training.answers)
        answer_history[self.question_id] = answer == self.question.right_answer
        training.answers = dumps(answer_history)
        training.time = datetime.now()
        if not self.next_question_id:
            training.status = (
                "correct"
                if all([answer is True for answer in answer_history.values()])
                else "failed"
            )

    def posted(self):
        if self.request.method != "POST":
            return False
        self.post()
        return True

    def validate(self):
        previous_question_id = self.previous_question_id
        if not previous_question_id:
            return
        training = self.get_or_create_training()
        try:
            answers = loads(training.answers)
        except ValueError:
            answers = {}
        if all([answer is None for answer in answers]):
            raise Unauthorized(_("You should start the training from the beginning"))
        if answers.get(previous_question_id) is None:
            raise Unauthorized(_("It seems you missed a slide"))

    def __call__(self):
        self.validate()
        if self.posted():
            return self.request.response.redirect(self.next_url)
        return super().__call__()


class SlideQuestionSuccess(SlideQuestionIntro):
    variation_class = ""

    def post(self):
        pass

    @property
    @view_memoize
    def organisation_logo(self):
        organisation = self.context.session.account.organisation
        if not organisation or not organisation.image_filename:
            return None
        country_url = self.webhelpers.country_obj.absolute_url()
        return (
            f"{country_url}/@@organisation-logo/{organisation.organisation_id}"
            f"?q={organisation.image_filename}"
        )

    def __call__(self):
        training = self.get_or_create_training()
        if training.status not in ("correct", "success"):
            raise Unauthorized("You do not own the certificate")
        if self.request.method == "POST":
            return self.post()
        return super().__call__()


class SlideQuestionTryAgain(SlideQuestionIntro):
    @property
    def failed_questions(self):
        training = self.get_or_create_training()
        try:
            answers = loads(training.answers)
        except ValueError:
            answers = {}
        survey = self.webhelpers._survey
        return [
            survey.get(question_id).title
            for question_id in self.question_ids
            if answers.get(question_id) is False
        ]


class MyTrainingsPortlet(BrowserView):
    columns = "1"
    element_id = "portlet-training"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def available(self):
        return self.my_unfinished_trainings or self.my_certificates

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

    def get_certificate(self, session):
        traversed_session = session.traversed_session
        # we cannot call the certificate view directly because if the tool was updated
        # the view will try to redirect (redirectOnSurveyUpdate)
        certificate_view = api.content.get_view(
            name="training-certificate-inner",
            context=traversed_session,
            request=self.request,
        )
        return certificate_view.index()
