"""
Upload
------

Form and browser view for importing a previously exported survey in XML format.

view: @@upload
"""

from ..risk import EnsureInterface
from ..risk import IFrenchEvaluation
from ..risk import IKinneyEvaluation
from ..risk import IRisk
from ..user import LoginField
from ..user import validLoginValue
from Acquisition import aq_inner
from euphorie.content import MessageFactory as _
from euphorie.content.behaviors.hide_from_training import IHideFromTraining
from euphorie.content.behaviors.toolcategory import IToolCategory
from euphorie.content.utils import IToolTypesInfo
from io import BytesIO
from markdownify import markdownify
from plone.autoform.form import AutoExtensibleForm
from plone.base.utils import safe_bytes
from plone.dexterity.utils import createContentInContainer
from plone.namedfile import field as filefield
from plone.namedfile.file import NamedBlobImage
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from z3c.form.interfaces import WidgetActionExecutionError
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import Invalid

import lxml.etree
import lxml.objectify
import mimetypes
import random


try:
    from base64 import decodebytes
except ImportError:
    # PY27
    from base64 import decodestring as decodebytes

ProfileQuestionLocationFields = [
    "label_multiple_present",
    "label_single_occurance",
    "label_multiple_occurances",
]

NSMAP = {None: "http://xml.simplon.biz/euphorie/survey/1.0"}
XMLNS = "{%s}" % NSMAP[None]
COMMA_REPLACEMENT = "__COMMA__"


def attr_unicode(node, attr, default=None):
    value = str(node.attrib.get(attr, "")).strip()
    if not value:
        return default
    return value


def attr_string(node, tag, attr, default=None):
    value = default
    element = getattr(node, tag, None)
    if element is not None:
        value = element.attrib.get(attr)
    return value


def attr_vocabulary(node, tag, field, default=None):
    value = node.get(tag, "").strip() if node else None
    if not value:
        return default
    try:
        return field.vocabulary.getTermByToken(value).value
    except LookupError:
        return default


def attr_bool(node, tag, attr, default=False):
    value = default
    element = getattr(node, tag, None)
    if element is not None:
        value = element.get(attr)
    return value == "true"


def attr_int(node, tag, attr, default=None):
    value = default
    element = getattr(node, tag, None)
    if element is not None:
        value = int(element.get(attr))
    return value


def el_unicode(
    node, tag, default=None, is_etranslate_compatible=False, convert_to_markdown=False
):
    value = getattr(node, tag, None)
    if value is None:
        return default
    if is_etranslate_compatible:
        # We need to remove the outer XML element e.g. <description>
        wrapped_xml = lxml.etree.tostring(value, encoding="unicode", pretty_print=True)
        end_of_first_tag = wrapped_xml.find(">") + 1
        start_of_last_tag = wrapped_xml.rfind("<")
        unwrapped_html = wrapped_xml[end_of_first_tag:start_of_last_tag]
        if convert_to_markdown:
            return markdownify(unwrapped_html)
        else:
            return unwrapped_html
    else:
        return str(value)


def el_string(node, tag, default=None):
    value = getattr(node, tag, None)
    if value is None:
        return default
    return str(value.text)


def el_bool(node, tag, default=False):
    value = getattr(node, tag, None)
    if value is None:
        return default
    return value.text == "true"


class IImportSector(Interface):
    """The fields used for importing a :obj:`euphorie.content.sector`."""

    sector_title = schema.TextLine(
        title=_("label_sector_title", default="Title of sector."),
        description=_(
            "help_sector_title",
            default="If you do not specify a title it will be taken "
            "from the input file.",
        ),
        required=False,
    )

    sector_login = LoginField(
        title=_("label_login_name", default="Login name"),
        required=True,
        constraint=validLoginValue,
    )

    surveygroup_title = schema.TextLine(
        title=_("label_surveygroup_title", default="Title of imported OiRA Tool"),
        description=_(
            "help_upload_surveygroup_title",
            default="If you do not specify a title it will be taken " "from the input.",
        ),
        required=False,
    )

    survey_title = schema.TextLine(
        title=_("label_upload_survey_title", default="Name for OiRA Tool version"),
        default=_("Standard"),
        required=True,
    )

    file = filefield.NamedFile(
        title=_("label_upload_filename", default="XML file"), required=True
    )


class IImportSurvey(Interface):
    """The fields used for importing a :obj:`euphorie.content.survey`."""

    surveygroup_title = schema.TextLine(
        title=_("label_surveygroup_title", default="Title of imported OiRA Tool"),
        description=_(
            "help_upload_surveygroup_title",
            default="If you do not specify a title it will be taken " "from the input.",
        ),
        required=False,
    )

    survey_title = schema.TextLine(
        title=_("label_upload_survey_title", default="Name for OiRA Tool version"),
        default=_("OiRA Tool import"),
        required=True,
    )

    file = filefield.NamedFile(
        title=_("label_upload_filename", default="XML file"), required=True
    )

    is_etranslate_compatible = schema.Bool(
        title=_(
            "label_is_etranslate_compatible",
            default="Import XML translation from eTranslate",
        ),
        required=False,
        default=False,
    )


class SurveyImporter:
    """Import a survey version from an XML file and create a new survey group
    and survey.

    This assumes the current context is a sector.
    """

    is_etranslate_compatible = False

    def __init__(self, context):
        self.context = context

    def ImportImage(self, node):
        """Import a base64 encoded image from an XML node.

        :param node: lxml.objectified XML node of image element
        :rtype: (:py:class:`NamedImage`, unicode) tuple
        """
        filename = attr_unicode(node, "filename")
        contentType = node.get("content-type", None)
        if not filename:
            basename = "image%d.%%s" % random.randint(1, 2**16)
            if contentType and "/" in contentType:
                filename = basename % contentType.split("/")[1]
            else:
                filename = basename % "jpg"
        image = NamedBlobImage(
            data=decodebytes(safe_bytes(str(node.text))),
            contentType=contentType,
            filename=filename,
        )
        if image.contentType is None and image.filename:
            image.contentType = mimetypes.guess_type(image.filename)[0]
        return (image, attr_unicode(node, "caption"))

    def ImportSolution(self, node, risk):
        """
        Create a new :obj:`euphorie.content.solution` object for a
        :obj:`euphorie.content.risk` given the details for a Solution as an XML
        node.

        :returns: :obj:`euphorie.content.solution`.
        """
        solution = createContentInContainer(risk, "euphorie.solution")
        solution.description = str(node.description)
        action = el_unicode(
            node,
            "action",
            is_etranslate_compatible=self.is_etranslate_compatible,
            convert_to_markdown=True,
        )
        solution.action = action or node.description
        solution.action_plan = str(getattr(node, "action-plan", ""))
        solution.prevention_plan = el_unicode(node, "prevention-plan")
        solution.requirements = el_unicode(node, "requirements")
        solution.external_id = attr_unicode(node, "external-id")
        return solution

    def ImportRisk(self, node, module):
        """
        Create a new :obj:`euphorie.content.risk` object for a
        :obj:`euphorie.content.module` given the details for a Risk as an XML
        node.

        :returns: :obj:`euphorie.content.risk`.
        """
        risk = createContentInContainer(module, "euphorie.risk", title=str(node.title))
        EnsureInterface(risk)
        risk.type = node.get("type")
        risk.description = el_unicode(
            node, "description", is_etranslate_compatible=self.is_etranslate_compatible
        )
        risk.problem_description = el_unicode(
            node,
            "problem-description",
            is_etranslate_compatible=self.is_etranslate_compatible,
        )
        risk.legal_reference = el_unicode(node, "legal-reference")
        risk.show_notapplicable = el_bool(node, "show-not-applicable")
        risk.external_id = attr_unicode(node, "external-id")

        if risk.type == "risk":
            em = getattr(node, "evaluation-method", None)
            risk.evaluation_method = em.text if em else "estimated"
            if risk.evaluation_method == "calculated":
                evaluation_algorithm = risk.evaluation_algorithm()
                if evaluation_algorithm == "kinney":
                    risk.default_probability = attr_vocabulary(
                        em,
                        "default-probability",
                        IKinneyEvaluation["default_probability"],
                    )
                    risk.default_frequency = attr_vocabulary(
                        em, "default-frequency", IKinneyEvaluation["default_frequency"]
                    )
                    risk.default_effect = attr_vocabulary(
                        em, "default-effect", IKinneyEvaluation["default_effect"]
                    )
                elif evaluation_algorithm == "french":
                    risk.default_severity = attr_vocabulary(
                        em, "default-severity", IFrenchEvaluation["default_severity"]
                    )
                    risk.default_frequency = attr_vocabulary(
                        em, "default-frequency", IFrenchEvaluation["default_frequency"]
                    )
            else:
                risk.default_priority = attr_vocabulary(
                    em, "default-priority", IRisk["default_priority"]
                )

        for index, child in enumerate(node.iterchildren(tag=XMLNS + "image")):
            postfix = "" if not index else str(index + 1)
            (image, caption) = self.ImportImage(child)
            setattr(risk, "image" + postfix, image)
            setattr(risk, "caption" + postfix, caption)
            if index == 3:
                break

        if hasattr(node, "solutions"):
            for child in node.solutions.solution:
                self.ImportSolution(child, risk)
        return risk

    def ImportModule(self, node, survey):
        """
        Create a new :obj:`euphorie.content.module` object for a
        :obj:`euphorie.content.survey` given the details for a Module as an XML
        node.

        :returns: :obj:`euphorie.content.module`.
        """
        module = createContentInContainer(
            survey, "euphorie.module", title=str(node.title)
        )
        module.optional = node.get("optional") == "true"
        module.description = el_unicode(
            node, "description", is_etranslate_compatible=self.is_etranslate_compatible
        )
        module.external_id = attr_unicode(node, "external-id")
        if module.optional:
            module.question = str(node.question)
        module.solution_direction = el_unicode(node, "solution-direction")

        for child in node.iterchildren(tag=XMLNS + "risk"):
            self.ImportRisk(child, module)

        for child in node.iterchildren(tag=XMLNS + "module"):
            self.ImportModule(child, module)

        image = getattr(node, "image", None)
        if image is not None:
            (image, caption) = self.ImportImage(image)
            module.image = image
            module.caption = caption

        if node.get("hide_from_training"):
            behavior = IHideFromTraining(module, None)
            if behavior:
                behavior.hide_from_training = True

        return module

    def ImportProfileQuestion(self, node, survey):
        """
        Create a new :obj:`euphorie.content.profilequestion` object for a
        :obj:`euphorie.content.survey` given the details for a Profile Question
        as an XML node.

        :returns: :obj:`euphorie.content.profilequestion`.
        """
        type = node.get("type")
        if type == "optional":
            profile = createContentInContainer(
                survey, "euphorie.module", title=str(node.title)
            )
            profile.optional = True
        else:
            profile = createContentInContainer(
                survey, "euphorie.profilequestion", title=str(node.title)
            )
        profile.description = el_unicode(
            node, "description", is_etranslate_compatible=self.is_etranslate_compatible
        )
        profile.question = str(node.question)
        profile.external_id = attr_unicode(node, "external-id")
        for fname in ProfileQuestionLocationFields:
            setattr(profile, fname, el_unicode(node, fname.replace("_", "-")))
        profile.use_location_question = el_bool(node, "use-location-question", True)

        for child in node.iterchildren(tag=XMLNS + "risk"):
            self.ImportRisk(child, profile)

        for child in node.iterchildren(tag=XMLNS + "module"):
            self.ImportModule(child, profile)
        return profile

    def ImportTrainingQuestion(self, node, survey):
        """
        Create a new :obj:`euphorie.training_question` object for a
        :obj:`euphorie.training_question` given the details for a Training Question
        as an XML node.

        :returns: :obj:`euphorie.training_question`.
        """
        training_question = createContentInContainer(
            survey, "euphorie.training_question", title=str(node.title)
        )
        training_question.right_answer = str(node.right_answer)
        training_question.wrong_answer_1 = str(node.wrong_answer_1)
        training_question.wrong_answer_2 = str(node.wrong_answer_2)
        return training_question

    def ImportSurvey(self, node, group, version_title):
        """
        Create a new :obj:`euphorie.content.survey` object for a
        :obj:`euphorie.content.surveygroup` given the details for a Survey as an
        XML node.

        :returns: :obj:`euphorie.content.survey`.
        """
        survey = createContentInContainer(group, "euphorie.survey", title=version_title)
        survey.introduction = el_unicode(
            node, "introduction", is_etranslate_compatible=self.is_etranslate_compatible
        )
        survey.classification_code = el_unicode(node, "classification-code")
        survey.language = el_string(node, "language")
        tti = getUtility(IToolTypesInfo)
        survey.report_completion_threshold = attr_int(
            node, "report_completion_threshold", "value"
        )
        survey.enable_web_training = attr_bool(node, "enable_web_training", "value")
        survey.enable_test_questions = attr_bool(node, "enable_test_questions", "value")
        survey.enable_email_reminder = attr_bool(node, "enable_email_reminder", "value")
        survey.num_training_questions = attr_int(
            node, "num_training_questions", "value"
        )
        if self.is_etranslate_compatible:
            survey.tool_type = attr_string(
                node, "tool_type", "value", tti.default_tool_type
            )
            survey.measures_text_handling = attr_string(
                node, "measures_text_handling", "value", "full"
            )
            survey.integrated_action_plan = attr_bool(
                node, "integrated_action_plan", "value"
            )
            survey.evaluation_optional = attr_bool(node, "evaluation-optional", "value")
        else:
            survey.tool_type = el_string(node, "tool_type", tti.default_tool_type)
            survey.measures_text_handling = el_string(
                node, "measures_text_handling", "full"
            )
            survey.integrated_action_plan = el_bool(node, "integrated_action_plan")
            survey.evaluation_optional = el_bool(node, "evaluation-optional")
        survey.external_id = attr_unicode(node, "external-id")
        external_site_logo = getattr(node, "external_site_logo", None)
        if external_site_logo is not None:
            (image, caption) = self.ImportImage(external_site_logo)
            survey.external_site_logo = image
        lead_image = getattr(node, "image", None)
        if lead_image is not None:
            (image, caption) = self.ImportImage(lead_image)
            survey.image = image

        if IToolCategory.providedBy(survey):
            IToolCategory(survey).tool_category = [
                x.replace(COMMA_REPLACEMENT, ",").strip()
                for x in el_unicode(node, "tool-category", "").split(",")
            ]
        for child in node.iterchildren():
            if child.tag == XMLNS + "profile-question":
                self.ImportProfileQuestion(child, survey)
            elif child.tag == XMLNS + "module":
                self.ImportModule(child, survey)
            elif child.tag == XMLNS + "training_question":
                self.ImportTrainingQuestion(child, survey)
        return survey

    def __call__(
        self, input, surveygroup_title, survey_title, is_etranslate_compatible=False
    ):
        """Import a new survey from the XML data in `input` and create a new
        survey with the given `title`.

        `input` has to be either the raw XML input, or a
        `lxml.objectify` enablde DOM.
        """
        self.is_etranslate_compatible = is_etranslate_compatible
        if isinstance(input, (str,) + (bytes,)):
            try:
                sector = lxml.objectify.fromstring(safe_bytes(input))
            except Exception:
                # It might be that the file is huge, let's try a different approach
                parser = lxml.etree.XMLParser(huge_tree=True)
                sector_tree = lxml.objectify.parse(
                    BytesIO(safe_bytes(input)), parser=parser
                )
                sector = lxml.objectify.fromstring(lxml.etree.tostring(sector_tree))
        else:
            sector = input

        root = aq_inner(self.context)
        sg = createContentInContainer(
            root,
            "euphorie.surveygroup",
            title=surveygroup_title or str(sector.survey.title),
        )

        return self.ImportSurvey(sector.survey, sg, survey_title)


class SectorImporter(SurveyImporter):
    """:returns: :obj:`euphorie.content.survey` root"""

    def __call__(
        self, input, sector_title, sector_login, surveygroup_title, survey_title
    ):
        if isinstance(input, (str,) + (bytes,)):
            sector = lxml.objectify.fromstring(safe_bytes(input))
        else:
            sector = input

        country = aq_inner(self.context)

        if not sector_title:
            sector_title = str(sector.title)
        root = createContentInContainer(country, "euphorie.sector", title=sector_title)

        account = getattr(sector, "account", None)
        if account is not None:
            root.login = sector_login or account.get("login").lower()
            root.password = account.get("password")
        else:
            root.login = sector_login

        contact = getattr(sector, "contact", None)
        if contact is not None:
            root.contact_name = el_unicode(contact, "name")
            root.contact_email = el_string(contact, "email")

        logo = getattr(sector, "logo", None)
        if logo is not None:
            root.logo = self.ImportImage(logo)[0]

        if hasattr(sector, "survey"):
            sg = createContentInContainer(
                root,
                "euphorie.surveygroup",
                title=surveygroup_title or str(sector.survey.title),
            )
            self.ImportSurvey(sector.survey, sg, survey_title)

        return root


class ImportSurvey(AutoExtensibleForm, form.Form):
    """The upload view for a :obj:`euphorie.content.sector`

    View name: @@upload
    """

    schema = IImportSurvey
    ignoreContext = True
    form_name = _("Import OiRA Tool version")

    importer_factory = SurveyImporter

    @button.buttonAndHandler(_("Upload"))
    def handleUpload(self, action):
        (data, errors) = self.extractData()
        if errors:
            return
        input = data["file"].data
        importer = self.importer_factory(self.context)
        try:
            survey = importer(
                input,
                data["surveygroup_title"],
                data["survey_title"],
                data["is_etranslate_compatible"],
            )
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                "file",
                Invalid(
                    _("error_invalid_xml", default="Please upload a valid XML file")
                ),
            )

        IStatusMessage(self.request).addStatusMessage(
            _("upload_success", default="Successfully imported the OiRA Tool"),
            type="success",
        )
        state = getMultiAdapter((survey, self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())

    @button.buttonAndHandler(_("button_cancel", default="Cancel"))
    def handleCancel(self, action):
        state = getMultiAdapter(
            (aq_inner(self.context), self.request), name="plone_context_state"
        )
        self.request.response.redirect(state.view_url())
