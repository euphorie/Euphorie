"""
Export Survey
-------------

Browser view for exporting a complete survey as XML.

View name: @@export
"""

from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client.utils import HasText
from euphorie.content import MessageFactory as _
from euphorie.content.behaviors.toolcategory import IToolCategory
from euphorie.content.browser.upload import COMMA_REPLACEMENT
from euphorie.content.browser.upload import NSMAP
from euphorie.content.browser.upload import ProfileQuestionLocationFields
from euphorie.content.module import IModule
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.risk import IKinneyEvaluation
from euphorie.content.risk import IRisk
from euphorie.content.solution import ISolution
from euphorie.content.survey import get_tool_type
from euphorie.content.utils import StripMarkup
from euphorie.content.utils import StripUnwanted
from lxml import etree
from plone.autoform.form import AutoExtensibleForm
from Products.CMFPlone.utils import safe_bytes
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.interface import Interface


try:
    from base64 import encodebytes
except ImportError:
    # PY27
    from base64 import encodestring as encodebytes


def getToken(field, value, default=None):
    """Looks up a term in the vocabulary associated with a field and returns
    its token, or raises a LookupError.

    :rtype: str
    :raises: LookupError
    """
    try:
        return field.vocabulary.getTerm(value).token
    except LookupError:
        return default


class IExportSurveySchema(Interface):
    """Fields used for configuring the export"""

    include_images = schema.Bool(
        title=_("label_survey_export_include_images", default="Include images"),
        description=_(
            "description_survey_export_include_images",
            default="All images contained in the OiRA tool can be exported along "
            "with the textual content. When the OiRA tool is then imported again, "
            "all images will be present. Please note that including images may "
            "result in a considerably larger file size.",
        ),
        required=False,
        default=False,
    )
    include_intro_text = schema.Bool(
        title=_(
            "label_survey_export_include_intro_text",
            default="Include introduction text",
        ),
        description=_(
            "description_survey_export_include_intro_text",
            default="The introduction text describes the general purpose of the OiRA "
            "tool. It usually gives the end users an idea what to expect in the tool "
            "and whether it will be relevant for them. The default is to include "
            "this text.",
        ),
        required=False,
        default=True,
    )
    include_module_solution_texts = schema.Bool(
        title=_(
            "label_survey_export_include_module_solution_texts",
            default="Include “Solution” texts on modules",
        ),
        description=_(
            "description_survey_export_include_module_solution_texts",
            "The “Solution” description” on modules is a deprecated kind of text "
            "that is no longer being used. The default is to skip this.",
        ),
        required=False,
        default=False,
    )
    include_module_description_texts = schema.Bool(
        title=_(
            "label_survey_export_include_module_description_texts",
            default="Include “Description” texts on modules",
        ),
        description=_(
            "description_survey_export_include_module_description_texts",
            default="Every module comes with an introductive description. The default "
            "is to include this text.",
        ),
        required=False,
        default=True,
    )
    include_risk_legal_texts = schema.Bool(
        title=_(
            "label_survey_export_include_risk_legal_texts",
            default="Include “Legal and policy references” texts on risks",
        ),
        description=_(
            "description_survey_export_include_risk_legal_texts",
            default="If the OiRA tool is exported because it should be made available "
            "for a different country, the legal texts might not apply there. Therefore "
            "the default is to skip these texts.",
        ),
        required=False,
        default=True,
    )
    include_measures = schema.Bool(
        title=_("label_survey_export_include_measures", default="Include measures"),
        description=_(
            "description_survey_export_include_measures",
            default="For each risk, a number of common measures – sometimes also "
            "referred to as “Solutions” – can be defined. While the default setting "
            "is to include them in the export, they may be excluded if required, "
            "for example to accommodate for a limited translation budget.",
        ),
        required=False,
        default=True,
    )


class ExportSurvey(AutoExtensibleForm, form.Form):
    """The upload view for a :obj:`euphorie.content.sector`

    View name: @@upload
    """

    schema = IExportSurveySchema
    ignoreContext = True
    form_name = _(u"Export OiRA Tool")

    @button.buttonAndHandler(_(u"Export"))
    def handleExport(self, action):
        (data, errors) = self.extractData()
        self.include_images = data.get("include_images")
        self.include_intro_text = data.get("include_intro_text")
        self.include_module_solution_texts = data.get("include_module_solution_texts")
        self.include_module_description_texts = data.get(
            "include_module_description_texts"
        )
        self.include_risk_legal_texts = data.get("include_risk_legal_texts")
        self.include_measures = data.get("include_measures")
        output = etree.Element("sector", nsmap=NSMAP)
        self.exportSurvey(output, self.context)
        response = self.request.response
        filename = "%s.xml" % aq_parent(aq_inner(self.context)).id
        response.setHeader(
            "Content-Disposition", u'attachment; filename="%s"' % filename
        )
        response.setHeader("Content-Type", "text/xml")
        self.request.response.write(
            etree.tostring(
                output, pretty_print=True, xml_declaration=True, encoding="utf-8"
            )
        )

    def render(self):
        if self.request.response.headers.get("content-disposition", "").startswith(
            "attachment"
        ):
            # We just generated an attachment, no need to render the form
            return ""
        return super().render()

    def exportImage(self, parent, image, caption=None):
        """:returns: base64 encoded image."""
        if not self.include_images:
            return
        node = etree.SubElement(parent, "image")
        if image.contentType:
            node.attrib["content-type"] = image.contentType
        if image.filename:
            node.attrib["filename"] = image.filename
        if caption:
            node.attrib["caption"] = caption
        node.text = encodebytes(safe_bytes(image.data))
        return node

    def exportSurvey(self, parent, survey):
        """Export a survey given a parent and the survey itself

        :returns: An XML node with the details of an :obj:`euphorie.content.survey`.
        """
        node = etree.SubElement(parent, "survey")
        if getattr(survey, "external_id", None):
            node.attrib["external-id"] = survey.external_id
        etree.SubElement(node, "title").text = aq_parent(survey).title
        if self.include_intro_text and StripMarkup(survey.introduction):
            etree.SubElement(node, "introduction").text = StripUnwanted(
                survey.introduction
            )
        if survey.classification_code:
            etree.SubElement(
                node, "classification-code"
            ).text = survey.classification_code
        etree.SubElement(node, "language").text = survey.language
        etree.SubElement(node, "tool_type").text = get_tool_type(survey)
        etree.SubElement(node, "measures_text_handling").text = getattr(
            survey, "measures_text_handling", "full"
        )
        etree.SubElement(node, "integrated_action_plan").text = (
            "true" if getattr(survey, "integrated_action_plan", False) else "false"
        )
        etree.SubElement(node, "evaluation-algorithm").text = aq_parent(
            survey
        ).evaluation_algorithm
        etree.SubElement(node, "evaluation-optional").text = (
            "true" if survey.evaluation_optional else "false"
        )
        if IToolCategory.providedBy(survey):
            tool_category = IToolCategory(survey).tool_category or []
            etree.SubElement(node, "tool-category").text = ", ".join(
                [x.replace(",", COMMA_REPLACEMENT) for x in tool_category]
            )

        if getattr(survey, "external_site_logo", None):
            self.exportImage(node, survey.external_site_logo)

        for child in survey.values():
            if IProfileQuestion.providedBy(child):
                self.exportProfileQuestion(node, child)
            if IModule.providedBy(child):
                self.exportModule(node, child)
        return node

    def exportProfileQuestion(self, parent, profile):
        """:returns: An XML node with the details of an
        :obj:`euphorie.content.profilequestion`.
        """
        node = etree.SubElement(parent, "profile-question")
        if getattr(profile, "external_id", None):
            node.attrib["external-id"] = profile.external_id
        etree.SubElement(node, "title").text = profile.title
        # Use title if question is not available (Euphorie < 2.0rc2 data)
        etree.SubElement(node, "question").text = profile.question or profile.title
        if HasText(profile.description):
            etree.SubElement(node, "description").text = StripUnwanted(
                profile.description
            )

        for fname in ProfileQuestionLocationFields:
            value = getattr(profile, fname, None)
            if value:
                etree.SubElement(node, fname.replace("_", "-")).text = value

        etree.SubElement(node, "use-location-question").text = (
            "true" if getattr(profile, "use_location_question", True) else "false"
        )

        for child in profile.values():
            if IModule.providedBy(child):
                self.exportModule(node, child)
            elif IRisk.providedBy(child):
                self.exportRisk(node, child)
        return node

    def exportModule(self, parent, module):
        """:returns: An XML node with the details of an
        :obj:`euphorie.content.module`."""
        node = etree.SubElement(
            parent, "module", optional="true" if module.optional else "false"
        )
        if getattr(module, "external_id", None):
            node.attrib["external-id"] = module.external_id
        etree.SubElement(node, "title").text = module.title
        if self.include_module_description_texts and HasText(module.description):
            etree.SubElement(node, "description").text = StripUnwanted(
                module.description
            )
        if module.optional:
            etree.SubElement(node, "question").text = module.question
        if self.include_module_solution_texts and StripMarkup(
            module.solution_direction
        ):
            etree.SubElement(node, "solution-direction").text = StripUnwanted(
                module.solution_direction
            )
        if module.image is not None:
            self.exportImage(node, module.image, module.caption)

        for child in module.values():
            if IModule.providedBy(child):
                self.exportModule(node, child)
            elif IRisk.providedBy(child):
                self.exportRisk(node, child)
        return node

    def exportRisk(self, parent, risk):
        """:returns: An XML node with the details of an :obj:`euphorie.content.risk`."""
        node = etree.SubElement(parent, "risk", type=risk.type)
        if getattr(risk, "external_id", None):
            node.attrib["external-id"] = risk.external_id
        etree.SubElement(node, "title").text = risk.title
        etree.SubElement(node, "problem-description").text = StripUnwanted(
            risk.problem_description
        )
        etree.SubElement(node, "description").text = StripUnwanted(risk.description)
        if self.include_risk_legal_texts and StripMarkup(risk.legal_reference):
            etree.SubElement(node, "legal-reference").text = StripUnwanted(
                risk.legal_reference
            )
        etree.SubElement(node, "show-not-applicable").text = (
            "true" if risk.show_notapplicable else "false"
        )
        if risk.type == "risk":
            method = etree.SubElement(node, "evaluation-method")
            method.text = risk.evaluation_method
            if risk.evaluation_method == "calculated":
                if risk.evaluation_algorithm() == "kinney":
                    if risk.default_probability:
                        method.attrib["default-probability"] = getToken(
                            IKinneyEvaluation["default_probability"],
                            risk.default_probability,
                            "0",
                        )
                    if risk.default_frequency:
                        method.attrib["default-frequency"] = getToken(
                            IKinneyEvaluation["default_frequency"],
                            risk.default_frequency,
                            "0",
                        )
                    if risk.default_effect:
                        method.attrib["default-effect"] = getToken(
                            IKinneyEvaluation["default_effect"],
                            risk.default_effect,
                            "0",
                        )
            elif risk.evaluation_method == "direct":
                if risk.default_priority:
                    method.attrib["default-priority"] = getToken(
                        IRisk["default_priority"], risk.default_priority
                    )

        for index in range(4):
            postfix = "" if not index else str(index + 1)
            image = getattr(risk, "image" + postfix, None)
            if image is not None:
                self.exportImage(node, image, getattr(risk, "caption" + postfix, None))

        if self.include_measures:
            solutions = [
                child for child in risk.values() if ISolution.providedBy(child)
            ]
            if solutions:
                sols = etree.SubElement(node, "solutions")
                for solution in solutions:
                    self.exportSolution(sols, solution)
        return node

    def exportSolution(self, parent, solution):
        """:returns: An XML node with the details
        of an :obj:`euphorie.content.solution`."""
        node = etree.SubElement(parent, "solution")
        if getattr(solution, "external_id", None):
            node.attrib["external-id"] = solution.external_id
        etree.SubElement(node, "description").text = StripUnwanted(solution.description)
        etree.SubElement(node, "action").text = StripUnwanted(solution.action)
        if solution.requirements:
            etree.SubElement(node, "requirements").text = StripUnwanted(
                solution.requirements
            )
        return node
