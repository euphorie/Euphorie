import mimetypes
from Acquisition import aq_inner
import lxml.etree
import lxml.objectify
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid
from plone.namedfile.file import NamedImage
from euphorie.content import MessageFactory as _
from euphorie.content.risk import InformationLink
from plone.namedfile import field as filefield
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from plone.dexterity.utils import createContentInContainer
from zope.component import getMultiAdapter
from Products.statusmessages.interfaces import IStatusMessage

NSMAP = {None : "http://xml.simplon.biz/euphorie/survey/1.0",
        "rie": "http://xml.simplon.biz/rie/euphorie-export/1.0"}
XMLNS = "{%s}" % NSMAP[None]
XMLNS_RIE = "{%s}" % NSMAP["rie"]


def el_string(node, tag, default=None):
    value = getattr(node, tag, None)
    if value is None:
        return default
    return value.text


def el_bool(node, tag, default=False):
    value = getattr(node, tag, None)
    if value is None:
        return default
    return value.text=="yes"



class IImportSector(Interface):
    sector_title = schema.TextLine(
            title = _(u"Title of sector."),
            description = _(u"If you do not specify a title it will be taken "
                            u"from the input file."),
            required = False)

    surveygroup_title = schema.TextLine(
            title = _(u"Title of imported survey."),
            description = _(u"If you do not specify a title it will be taken "
                            u"from the input."),
            required = False)

    survey_title = schema.TextLine(
            title = _(u"Title of imported survey version"),
            default = _(u"Standard"), 
            required = True)

    file = filefield.NamedImage(
            title = _(u"XML file"),
            description = _(u"A survey in standard XML format."),
            required = True)



class IImportSurvey(Interface):
    title = schema.TextLine(
            title = _(u"Title of imported survey version"),
            default = _(u"Survey import"),
            required = True)

    file = filefield.NamedImage(
            title = _(u"XML file"),
            description = _(u"A survey in standard XML format."),
            required = True)



class SurveyImporter(object):
    """Import a survey version from a XML file. This assumes the current
    context is a survey group instance.
    """

    def __init__(self, context):
        self.context=context


    def ImportSolution(self, node, risk):
        solution=createContentInContainer(risk, "euphorie.solution")
        solution.description=node.description.text
        solution.action_plan=getattr(node, "action-plan").text
        solution.prevention_plan=el_string(node, "prevention-plan")
        solution.requirements=el_string(node, "requirements")


    def ImportRisk(self, node, module):
        risk=createContentInContainer(module, "euphorie.risk",
                                      title=node.title.text)
        risk.type=node.get("type")
        risk.description=node.description.text
        risk.problem_description=el_string(node, "problem-description")
        risk.legal_reference=el_string(node, "legal-reference")
        risk.show_notapplicable=el_bool(node, "show-not-applicable")
        risk.evaluation_method=getattr(node, "evaluation-method").text
        if risk.evaluation_method=="calculated":
            em=getattr(node, "evaluation-method")
            risk.default_probability=int(em.get("default-probability"))
            risk.default_frequency=int(em.get("default-frequency"))
            risk.default_effect=int(em.get("default-effect"))

        if hasattr(node, "solutions"):
            for child in node.solutions.solution:
                self.ImportSolution(child, risk)

        if hasattr(node, "links"):
            for child in node.links.link:
                if risk.links is None:
                    risk.links=[]
                risk.links.append(InformationLink(dict(
                    url=child.url.text,
                    title=child.title.text)))


    def ImportModule(self, node, survey):
        module=createContentInContainer(survey, "euphorie.module",
                                        title=node.title.text)
        module.optional=node.get("optional")=="yes"
        module.description=node.description.text
        if module.optional:
            module.question=node.question.text
        module.solution_direction=el_string(node, "solution-direction")

        for child in node.iterchildren(tag=XMLNS+"risk"):
            self.ImportRisk(child, module)

        for child in node.iterchildren(tag=XMLNS+"module"):
            self.ImportModule(child, module)


    def ImportProfileQuestion(self, node, survey):
        profile=createContentInContainer(survey, "euphorie.profilequestion",
                                        title=node.title.text)
        profile.type=node.get("type")
        profile.description=node.description.text
        profile.question=node.question.text

        for child in node.iterchildren(tag=XMLNS+"risk"):
            self.ImportRisk(child, profile)

        for child in node.iterchildren(tag=XMLNS+"module"):
            self.ImportModule(child, profile)


    def ImportSurvey(self, node, group, version_title):
        group.classification_code=el_string(node, "classification-code")
        survey=createContentInContainer(group, "euphorie.survey",
                                        title=version_title)
        survey.evaluation_optional=el_bool(node, "evaluation-optional")

        for child in node.iterchildren():
            if child.tag==XMLNS+"profile-question":
                self.ImportProfileQuestion(child, survey)
            elif child.tag==XMLNS+"module":
                self.ImportModule(child, survey)

        return survey


    def __call__(self, input, title):
        """Import a new survey from the XML data in `input` and create a
        new survey with the given `title`.

        `input` has to be either the raw XML input, or a `lxml.objectify`
        enablde DOM.
        """
        if isinstance(input, basestring):
            sector=lxml.objectify.fromstring(input)
        else:
            sector=input

# TODO: switch security manager to sector
        self.ImportSurvey(sector.survey, aq_inner(self.context), title)



class SectorImporter(SurveyImporter):
    def __call__(self, input, sector_title, surveygroup_title, survey_title):
        if isinstance(input, basestring):
            sector=lxml.objectify.fromstring(input)
        else:
            sector=input

        country=aq_inner(self.context)

        if not sector_title:
            sector_title=sector.title.text
        root=createContentInContainer(country, "euphorie.sector", title=sector_title)

        account=getattr(sector, "account", None)
        if account is not None:
# TODO: check for duplicate login names and user ids
            root.login=account.get("login").lower()
            root.password=account.get("password")

        contact=getattr(sector, "contact", None)
        if contact is not None:
            root.contact_name=el_string(contact, "name")
            root.contact_email=el_string(contact, "email")

        logo=getattr(sector, "logo", None)
        if logo is not None:
            root.logo=NamedImage(
                data=logo.text.decode("base64"),
                contentType=logo.get("content-type", None),
                filename=logo.get("filename", None))
            if root.logo.contentType is None and root.logo.filename:
                root.logo.contentType=mimetypes.guess_type(root.logo.filename)[0]

        if hasattr(sector, "survey"):
            if not surveygroup_title:
                surveygroup_title=sector.survey.title.text

            # TODO: switch security manager to sector
            sg=createContentInContainer(root, "euphorie.surveygroup",
                    title=surveygroup_title)

            self.ImportSurvey(sector.survey, sg, survey_title)

        return root



class ImportSurvey(form.Form):
    fields = field.Fields(IImportSurvey)
    ignoreContext = True
    label = _(u"Import survey version")

    @button.buttonAndHandler(_(u"Upload"))
    def handleUpload(self, action):
        (data,errors) = self.extractData()
        input=data["file"].data

        importer=SurveyImporter(self.context)

        try:
            survey=importer(input, data["title"])
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                    "file",
                    Invalid(_(u"Please upload a valid XML file")))

        IStatusMessage(self.request).addStatusMessage(
                _(u"Succesfully imported the survey"), type="info")
        state=getMultiAdapter((survey, self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())



ImportSurveyView = wrap_form(ImportSurvey)



class ImportSector(form.Form):
    fields = field.Fields(IImportSector)
    ignoreContext = True
    label = _(u"Import sector and survey")

    @button.buttonAndHandler(_(u"Upload"))
    def handleUpload(self, action):
        (data,errors) = self.extractData()
        input=data["file"].data

        importer=SectorImporter(self.context)

        try:
            sector=importer(input, data["sector_title"],
                    data["surveygroup_title"], data["survey_title"])
        except lxml.etree.XMLSyntaxError:
            raise WidgetActionExecutionError(
                    "file",
                    Invalid(_(u"Please upload a valid XML file")))

        IStatusMessage(self.request).addStatusMessage(
                _(u"Succesfully imported the sector"), type="info")
        state=getMultiAdapter((sector, self.request), name="plone_context_state")
        self.request.response.redirect(state.view_url())


ImportSectorView = wrap_form(ImportSector)
