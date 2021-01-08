"""
Upload
------

Form and browser view for importing a previously exported survey in XML format.

view: @@upload
"""
from .. import MessageFactory as _
from .country import ICountry
from .risk import EnsureInterface
from .risk import IFrenchEvaluation
from .risk import IKinneyEvaluation
from .risk import IRisk
from .sector import ISector
from .user import LoginField
from .user import validLoginValue
from Acquisition import aq_inner
from euphorie.content.behaviors.toolcategory import IToolCategory
from euphorie.content.utils import IToolTypesInfo
from five import grok
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from plone.namedfile import field as filefield
from plone.namedfile.file import NamedBlobImage
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from z3c.form import button
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
import six


ProfileQuestionLocationFields = [
    "label_multiple_present",
    "label_single_occurance",
    "label_multiple_occurances",
]

NSMAP = {None: "http://xml.simplon.biz/euphorie/survey/1.0"}
XMLNS = "{%s}" % NSMAP[None]
COMMA_REPLACEMENT = "__COMMA__"


def attr_unicode(node, attr, default=None):
    value = six.text_type(node.attrib.get(attr, u"")).strip()
    if not value:
        return default
    return value


def attr_vocabulary(node, tag, field, default=None):
    value = node.get(tag, u"").strip() if node else None
    if not value:
        return default
    try:
        return field.vocabulary.getTermByToken(value).value
    except LookupError:
        return default


def el_unicode(node, tag, default=None):
    value = getattr(node, tag, None)
    if value is None:
        return default
    return six.text_type(value)


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
        title=_("label_sector_title", default=u"Title of sector."),
        description=_(
            "help_sector_title",
            default=u"If you do not specify a title it will be taken "
            u"from the input file.",
        ),
        required=False,
    )

    sector_login = LoginField(
        title=_("label_login_name", default=u"Login name"),
        required=True,
        constraint=validLoginValue,
    )

    surveygroup_title = schema.TextLine(
        title=_("label_surveygroup_title", default=u"Title of imported OiRA Tool"),
        description=_(
            "help_upload_surveygroup_title",
            default=u"If you do not specify a title it will be taken "
            u"from the input.",
        ),
        required=False,
    )

    survey_title = schema.TextLine(
        title=_("label_upload_survey_title", default=u"Name for OiRA Tool version"),
        default=_(u"Standard"),
        required=True,
    )

    file = filefield.NamedFile(
        title=_("label_upload_filename", default=u"XML file"), required=True
    )


class IImportSurvey(Interface):
    """The fields used for importing a :obj:`euphorie.content.survey`."""

    surveygroup_title = schema.TextLine(
        title=_("label_surveygroup_title", default=u"Title of imported OiRA Tool"),
        description=_(
            "help_upload_surveygroup_title",
            default=u"If you do not specify a title it will be taken "
            u"from the input.",
        ),
        required=False,
    )

    survey_title = schema.TextLine(
        title=_("label_upload_survey_title", default=u"Name for OiRA Tool version"),
        default=_(u"OiRA Tool import"),
        required=True,
    )

    file = filefield.NamedFile(
        title=_("label_upload_filename", default=u"XML file"), required=True
    )


class SurveyImporter(object):
    """Import a survey version from an XML file and create a new survey group
    and survey. This assumes the current context is a sector.
    """

    def __init__(self, context):
        self.context = context
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get("euphorie")
        self.use_existing_measures = settings.get("use_existing_measures", False)

    def ImportImage(self, node):
        """
        Import a base64 encoded image from an XML node.

        :param node: lxml.objectified XML node of image element
        :rtype: (:py:class:`NamedImage`, unicode) tuple
        """
        filename = attr_unicode(node, "filename")
        contentType = node.get("content-type", None)
        if not filename:
            basename = u"image%d.%%s" % random.randint(1, 2 ** 16)
            if contentType and "/" in contentType:
                filename = basename % contentType.split(u"/")[1]
            else:
                filename = basename % u"jpg"
        image = NamedBlobImage(
            data=node.text.decode("base64"), contentType=contentType, filename=filename
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
        solution.description = six.text_type(node.description)
        solution.action = six.text_type(
            getattr(node, "action", None) or node.description
        )
        solution.action_plan = six.text_type(getattr(node, "action-plan", ""))
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
        risk = createContentInContainer(
            module, "euphorie.risk", title=six.text_type(node.title)
        )
        EnsureInterface(risk)
        risk.type = node.get("type")
        risk.description = six.text_type(node.description)
        risk.problem_description = el_unicode(node, "problem-description")
        risk.legal_reference = el_unicode(node, "legal-reference")
        risk.show_notapplicable = el_bool(node, "show-not-applicable")
        risk.external_id = attr_unicode(node, "external-id")
        if self.use_existing_measures:
            risk.existing_measures = el_unicode(node, "existing_measures")

        if risk.type == "risk":
            em = getattr(node, "evaluation-method", None)
            risk.evaluation_method = em.text if em else "estimated"
            if risk.evaluation_method == "calculated":
                evaluation_algorithm = risk.evaluation_algorithm()
                if evaluation_algorithm == u"kinney":
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
                elif evaluation_algorithm == u"french":
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

        for (index, child) in enumerate(node.iterchildren(tag=XMLNS + "image")):
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
            survey, "euphorie.module", title=six.text_type(node.title)
        )
        module.optional = node.get("optional") == "true"
        module.description = el_unicode(node, "description")
        module.external_id = attr_unicode(node, "external-id")
        if module.optional:
            module.question = six.text_type(node.question)
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
                survey, "euphorie.module", title=six.text_type(node.title)
            )
            profile.optional = True
        else:
            profile = createContentInContainer(
                survey, "euphorie.profilequestion", title=six.text_type(node.title)
            )
        profile.description = el_unicode(node, "description")
        profile.question = six.text_type(node.question)
        profile.external_id = attr_unicode(node, "external-id")
        for fname in ProfileQuestionLocationFields:
            setattr(profile, fname, el_unicode(node, fname.replace("_", "-")))
        profile.use_location_question = el_bool(node, "use-location-question", True)

        for child in node.iterchildren(tag=XMLNS + "risk"):
            self.ImportRisk(child, profile)

        for child in node.iterchildren(tag=XMLNS + "module"):
            self.ImportModule(child, profile)
        return profile

    def ImportSurvey(self, node, group, version_title):
        """
        Create a new :obj:`euphorie.content.survey` object for a
        :obj:`euphorie.content.surveygroup` given the details for a Survey as an
        XML node.

        :returns: :obj:`euphorie.content.survey`.
        """
        survey = createContentInContainer(group, "euphorie.survey", title=version_title)
        survey.introduction = el_unicode(node, "introduction")
        survey.classification_code = el_unicode(node, "classification-code")
        survey.language = el_string(node, "language")
        tti = getUtility(IToolTypesInfo)
        survey.tool_type = el_string(node, "tool_type", tti.default_tool_type)
        survey.measures_text_handling = el_string(
            node, "measures_text_handling", "full"
        )
        survey.integrated_action_plan = el_bool(node, "integrated_action_plan")
        survey.evaluation_optional = el_bool(node, "evaluation-optional")
        survey.external_id = attr_unicode(node, "external-id")
        external_site_logo = getattr(node, "image", None)
        if external_site_logo is not None:
            (image, caption) = self.ImportImage(external_site_logo)
            survey.external_site_logo = image

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
        return survey

    def __call__(self, input, surveygroup_title, survey_title):
        """Import a new survey from the XML data in `input` and create a
        new survey with the given `title`.

        `input` has to be either the raw XML input, or a `lxml.objectify`
        enablde DOM.
        """
        if isinstance(input, six.string_types):
            sector = lxml.objectify.fromstring(input)
        else:
            sector = input

        root = aq_inner(self.context)
        sg = createContentInContainer(
            root,
            "euphorie.surveygroup",
            title=surveygroup_title or six.text_type(sector.survey.title),
        )

        return self.ImportSurvey(sector.survey, sg, survey_title)


class SectorImporter(SurveyImporter):
    """:returns: :obj:`euphorie.content.survey` root"""

    def __call__(
        self, input, sector_title, sector_login, surveygroup_title, survey_title
    ):
        if isinstance(input, six.string_types):
            sector = lxml.objectify.fromstring(input)
        else:
            sector = input

        country = aq_inner(self.context)

        if not sector_title:
            sector_title = six.text_type(sector.title)
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
                title=surveygroup_title or six.text_type(sector.survey.title),
            )
            self.ImportSurvey(sector.survey, sg, survey_title)

        return root


class ImportSurvey(form.SchemaForm):
    """The upload view for a :obj:`euphorie.content.sector`

    View name: @@upload
    """

    grok.context(ISector)
    grok.require("euphorie.content.AddNewRIEContent")
    grok.name("upload")
    form.wrap(True)

    schema = IImportSurvey
    ignoreContext = True
    form_name = _(u"Import OiRA Tool version")

    importer_factory = SurveyImporter

    @button.buttonAndHandler(_(u"Upload"))
    def handleUpload(self, action):
        (data, errors) = self.extractData()
        input = data["file"].data
        importer = self.importer_factory(self.context)
        try:
            survey = importer(input, data["surveygroup_title"], data["survey_title"])
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                "file",
                Invalid(
                    _("error_invalid_xml", default=u"Please upload a valid XML file")
                ),
            )

        IStatusMessage(self.request).addStatusMessage(
            _("upload_success", default=u"Succesfully imported the OiRA Tool"),
            type="success",
        )
        state = getMultiAdapter((survey, self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())


class ImportSector(form.SchemaForm):
    """The upload view for a :obj:`euphorie.content.country`

    View name: @@upload
    """

    grok.context(ICountry)
    grok.require("euphorie.content.ManageCountry")
    grok.name("upload")
    form.wrap(True)

    schema = IImportSector
    ignoreContext = True
    label = _("title_import_sector_survey", default=u"Import sector and OiRA Tool")

    importer_factory = SectorImporter

    @button.buttonAndHandler(_("button_upload", default=u"Upload"))
    def handleUpload(self, action):
        (data, errors) = self.extractData()
        input = data["file"].data

        importer = self.importer_factory(self.context)

        try:
            sector = importer(
                input,
                data["sector_title"],
                data["sector_login"],
                data["surveygroup_title"],
                data["survey_title"],
            )
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                "file",
                Invalid(
                    _("error_invalid_xml", default=u"Please upload a valid XML file")
                ),
            )

        IStatusMessage(self.request).addStatusMessage(
            _("upload_success", default=u"Succesfully imported the OiRA Tool"),
            type="success",
        )
        state = getMultiAdapter((sector, self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())
