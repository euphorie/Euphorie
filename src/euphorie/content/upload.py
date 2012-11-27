import mimetypes
import random
from Acquisition import aq_inner
import lxml.etree
import lxml.objectify
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from plone.namedfile.file import NamedBlobImage
from euphorie.content import MessageFactory as _
from plone.namedfile import field as filefield
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from plone.dexterity.utils import createContentInContainer
from zope.component import getMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage
from euphorie.content.risk import IRisk
from euphorie.content.risk import IFrenchEvaluation
from euphorie.content.risk import IKinneyEvaluation
from euphorie.content.risk import EnsureInterface
from euphorie.content.user import LoginField
from euphorie.content.user import validLoginValue


NSMAP = {None: "http://xml.simplon.biz/euphorie/survey/1.0"}
XMLNS = "{%s}" % NSMAP[None]


def attr_unicode(node, attr, default=None):
    value = unicode(node.attrib.get(attr, u"")).strip()
    if not value:
        return default
    return value


def attr_vocabulary(node, tag, field, default=None):
    value = node.get(tag, u"").strip()
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
    return unicode(value)


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
    sector_title = schema.TextLine(
            title=_("label_sector_title", default=u"Title of sector."),
            description=_("help_sector_title",
                default=u"If you do not specify a title it will be taken "
                        u"from the input file."),
            required=False)

    sector_login = LoginField(
            title=_("label_login_name", default=u"Login name"),
            required=True,
            constraint=validLoginValue)

    surveygroup_title = schema.TextLine(
            title=_("label_surveygroup_title",
                default=u"Title of imported survey."),
            description=_("help_upload_surveygroup_title",
                default=u"If you do not specify a title it will be taken "
                        u"from the input."),
            required=False)

    survey_title = schema.TextLine(
            title=_("label_upload_survey_title",
                default=u"Name for survey version"),
            default=_(u"Standard"),
            required=True)

    file = filefield.NamedFile(
            title=_("label_upload_filename", default=u"XML file"),
            required=True)


class IImportSurvey(Interface):
    surveygroup_title = schema.TextLine(
            title=_("label_surveygroup_title",
                default=u"Title of imported survey."),
            description=_("help_upload_surveygroup_title",
                default=u"If you do not specify a title it will be taken "
                        u"from the input."),
            required=False)

    survey_title = schema.TextLine(
            title=_("label_upload_survey_title",
                default=u"Name for survey version"),
            default=_(u"Survey import"),
            required=True)

    file = filefield.NamedFile(
            title=_("label_upload_filename", default=u"XML file"),
            required=True)


class SurveyImporter(object):
    """Import a survey version from a XML file and creates a new survey group
    and survey. This assumes the current context is a sector.
    """

    def __init__(self, context):
        self.context = context

    def ImportImage(self, node):
        """
        Import an image from an XML node.

        :param node: lxml.objectified XML node of image element
        :rtype: (:py:class:`NamedImage`, unicode) tuple
        """
        filename = attr_unicode(node, 'filename')
        contentType = node.get("content-type", None)
        if not filename:
            basename = u'image%d.%%s' % random.randint(1, 2 ** 16)
            if contentType and '/' in contentType:
                filename = basename % contentType.split(u'/')[1]
            else:
                filename = basename % u'jpg'
        image = NamedBlobImage(data=node.text.decode("base64"),
                contentType=contentType, filename=filename)
        if image.contentType is None and image.filename:
            image.contentType = mimetypes.guess_type(image.filename)[0]
        return (image, attr_unicode(node, "caption"))

    def ImportSolution(self, node, risk):
        solution = createContentInContainer(risk, "euphorie.solution")
        solution.description = unicode(node.description)
        solution.action_plan = unicode(getattr(node, "action-plan"))
        solution.prevention_plan = el_unicode(node, "prevention-plan")
        solution.requirements = el_unicode(node, "requirements")
        solution.external_id = attr_unicode(node, "external-id")

    def ImportRisk(self, node, module):
        risk = createContentInContainer(module, "euphorie.risk",
                                      title=unicode(node.title))
        EnsureInterface(risk)
        risk.type = node.get("type")
        risk.description = unicode(node.description)
        risk.problem_description = el_unicode(node, "problem-description")
        risk.legal_reference = el_unicode(node, "legal-reference")
        risk.show_notapplicable = el_bool(node, "show-not-applicable")
        risk.external_id = attr_unicode(node, "external-id")
        if risk.type == "risk":
            em = getattr(node, "evaluation-method")
            risk.evaluation_method = em.text
            if risk.evaluation_method == "calculated":
                evaluation_algorithm = risk.evaluation_algorithm()
                if evaluation_algorithm == u"kinney":
                    risk.default_probability = attr_vocabulary(em,
                            "default-probability",
                            IKinneyEvaluation["default_probability"])
                    risk.default_frequency = attr_vocabulary(em,
                            "default-frequency",
                            IKinneyEvaluation["default_frequency"])
                    risk.default_effect = attr_vocabulary(em,
                            "default-effect",
                            IKinneyEvaluation["default_effect"])
                elif evaluation_algorithm == u"french":
                    risk.default_severity = attr_vocabulary(em,
                            "default-severity",
                            IFrenchEvaluation["default_severity"])
                    risk.default_frequency = attr_vocabulary(em,
                            "default-frequency",
                            IFrenchEvaluation["default_frequency"])
            else:
                risk.default_priority = attr_vocabulary(em, "default-priority",
                        IRisk["default_priority"])

        for (index, child) in \
                enumerate(node.iterchildren(tag=XMLNS + "image")):
            postfix = "" if not index else str(index + 1)
            (image, caption) = self.ImportImage(child)
            setattr(risk, "image" + postfix, image)
            setattr(risk, "caption" + postfix, caption)
            if index == 3:
                break

        if hasattr(node, "solutions"):
            for child in node.solutions.solution:
                self.ImportSolution(child, risk)

    def ImportModule(self, node, survey):
        module = createContentInContainer(survey, "euphorie.module",
                                        title=unicode(node.title))
        module.optional = node.get("optional") == "true"
        module.description = el_unicode(node, 'description')
        module.external_id = attr_unicode(node, "external-id")
        if module.optional:
            module.question = unicode(node.question)
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

    def ImportProfileQuestion(self, node, survey):
        type = node.get("type")
        if type == 'optional':
            profile = createContentInContainer(survey, "euphorie.module",
                                            title=unicode(node.title))
            profile.optional = True
        else:
            profile = createContentInContainer(survey,
                    "euphorie.profilequestion", title=unicode(node.title))
        profile.description = el_unicode(node, 'description')
        profile.question = unicode(node.question)
        profile.external_id = attr_unicode(node, "external-id")

        for child in node.iterchildren(tag=XMLNS + "risk"):
            self.ImportRisk(child, profile)

        for child in node.iterchildren(tag=XMLNS + "module"):
            self.ImportModule(child, profile)

    def ImportSurvey(self, node, group, version_title):
        survey = createContentInContainer(group, "euphorie.survey",
                                        title=version_title)
        survey.classification_code = el_string(node, "classification-code")
        survey.language = el_string(node, "language")
        survey.evaluation_optional = el_bool(node, "evaluation-optional")
        survey.external_id = attr_unicode(node, "external-id")

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
        if isinstance(input, basestring):
            sector = lxml.objectify.fromstring(input)
        else:
            sector = input

        root = aq_inner(self.context)
        sg = createContentInContainer(root, "euphorie.surveygroup",
                title=surveygroup_title or unicode(sector.survey.title))

        return self.ImportSurvey(sector.survey, sg, survey_title)


class SectorImporter(SurveyImporter):
    def __call__(self, input, sector_title, sector_login, surveygroup_title,
            survey_title):
        if isinstance(input, basestring):
            sector = lxml.objectify.fromstring(input)
        else:
            sector = input

        country = aq_inner(self.context)

        if not sector_title:
            sector_title = unicode(sector.title)
        root = createContentInContainer(country, "euphorie.sector",
                title=sector_title)

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
            sg = createContentInContainer(root, "euphorie.surveygroup",
                    title=surveygroup_title or unicode(sector.survey.title))
            self.ImportSurvey(sector.survey, sg, survey_title)

        return root


class ImportSurvey(form.Form):
    fields = field.Fields(IImportSurvey)
    ignoreContext = True
    form_name = _(u"Import survey version")

    @button.buttonAndHandler(_(u"Upload"))
    def handleUpload(self, action):
        (data, errors) = self.extractData()
        input = data["file"].data
        importer = SurveyImporter(self.context)
        try:
            survey = importer(input,
                    data["surveygroup_title"], data["survey_title"])
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                    "file",
                    Invalid(_("error_invalid_xml",
                        default=u"Please upload a valid XML file")))

        IStatusMessage(self.request).addStatusMessage(
            _("upload_success",
                default=u"Succesfully imported the survey"), type="success")
        state = getMultiAdapter((survey, self.request),
                name="plone_context_state")
        self.request.response.redirect(state.view_url())


ImportSurveyView = wrap_form(ImportSurvey)


class ImportSector(form.Form):
    fields = field.Fields(IImportSector)
    ignoreContext = True
    label = _("title_import_sector_survey",
            default=u"Import sector and survey")

    @button.buttonAndHandler(_("button_upload", default=u"Upload"))
    def handleUpload(self, action):
        (data, errors) = self.extractData()
        input = data["file"].data

        importer = SectorImporter(self.context)

        try:
            sector = importer(input, data["sector_title"],
                    data["sector_login"], data["surveygroup_title"],
                    data["survey_title"])
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                    "file",
                    Invalid(_("error_invalid_xml",
                        default=u"Please upload a valid XML file")))

        IStatusMessage(self.request).addStatusMessage(
                _("upload_success",
                    default=u"Succesfully imported the survey"),
                type="success")
        state = getMultiAdapter((sector, self.request),
                name="plone_context_state")
        self.request.response.redirect(state.view_url())


ImportSectorView = wrap_form(ImportSector)
