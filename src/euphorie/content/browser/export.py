"""
Export Survey
-------------

Browser view for exporting a complete survey as XML.

View name: @@export
"""

from Acquisition import aq_inner
from Acquisition import aq_parent
from bs4 import BeautifulSoup
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
from euphorie.content.training_question import ITrainingQuestion
from euphorie.content.utils import StripMarkup
from euphorie.content.utils import StripUnwanted
from io import BytesIO
from lxml import etree
from lxml import html
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.base.utils import safe_bytes
from plonetheme.nuplone.z3cform.directives import depends
from z3c.form import button
from z3c.form import form
from zipfile import ZipFile
from zope import schema
from zope.interface import Interface

import re


all_breaks = re.compile("(\n|\r)+")

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
    """Fields used for configuring the export."""

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

    depends("export_as_plain_text", "include_images", "off")
    export_as_plain_text = schema.Bool(
        title=_(
            "label_export_as_plain_text",
            default="Export additionally as plain text file",
        ),
        description=_(
            "description_export_as_plain_text",
            default="The plain text file will contain all translatable text without "
            "formatting. This file can be used to determine a word count for "
            "estimating the cost of translation.",
        ),
        required=False,
        default=False,
    )
    is_etranslate_compatible = schema.Bool(
        title=_(
            "label_export_etranslate_compatible",
            default="Export in eTranslate compatible XML",
        ),
        description=_(
            "description_is_etranslate_compatible",
            default="The default export escapes HTML, which is not supported"
            "by eTranslate",
        ),
        required=False,
        default=False,
    )


class ExportSurvey(AutoExtensibleForm, form.Form):
    """The upload view for a :obj:`euphorie.content.sector`

    View name: @@upload
    """

    schema = IExportSurveySchema
    ignoreContext = True
    form_name = _("Export OiRA Tool")
    # defaults
    include_images = False
    include_intro_text = True
    include_module_solution_texts = False
    include_module_description_texts = True
    include_risk_legal_texts = False
    include_measures = True
    export_as_plain_text = False
    is_etranslate_compatible = False

    def _add_string_or_html(self, node, text, element):
        stripped_text = StripUnwanted(text)
        if self.is_etranslate_compatible:
            html_fragment = html.fragment_fromstring(stripped_text, element)
            node.append(html_fragment)
        else:
            etree.SubElement(node, element).text = stripped_text
        return node

    @button.buttonAndHandler(_("Export"))
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
        self.export_as_plain_text = data.get("export_as_plain_text")
        self.is_etranslate_compatible = data.get("is_etranslate_compatible")
        rendered_output = self.render_output()
        self.request.response.write(rendered_output)

    @button.buttonAndHandler(_("button_cancel", default="Cancel"), name="cancel")
    def handleCancel(self, action):
        state = api.content.get_view(
            "plone_context_state", aq_inner(self.context), self.request
        )
        self.request.response.redirect(state.view_url())

    def render_output(self):
        output = etree.Element("sector", nsmap=NSMAP)
        self.exportSurvey(output, self.context)
        response = self.request.response
        rendered_xml = etree.tostring(
            output, pretty_print=True, xml_declaration=True, encoding="utf-8"
        )
        context_id = aq_parent(aq_inner(self.context)).id
        if self.export_as_plain_text and not self.include_images:
            outer_soup = BeautifulSoup(rendered_xml, "lxml")
            # Some tags of the survey contain only functional information, such
            # as true/false or calculated/evaluated
            # Strip them for the word counting
            functional_tags = (
                "classification-code",
                "evaluation-method",
                "evaluation-algorithm",
                "evaluation-optional",
                "integrated_action_plan",
                "language",
                "measures_text_handling",
                "show-not-applicable",
                "tool_type",
            )
            for tag in functional_tags:
                entities = outer_soup.findAll(tag)
                [entity.extract() for entity in entities]
            # The extracted texts contain HTML entities such as &lt;p&gt;
            # We need to convert them to real tags to be able to strip them too for
            # word counting
            inner_soup = BeautifulSoup(outer_soup.get_text(), "html.parser")
            text = inner_soup.get_text()
            text = all_breaks.sub(" ", text)
            zip_output = BytesIO()
            with ZipFile(zip_output, mode="w") as zip:
                zip.writestr(f"{context_id}_word_count.txt", text)
                zip.writestr(f"{context_id}.xml", rendered_xml)
            self.request.response.setHeader("Content-Type", "application/zip")
            self.request.response.setHeader(
                "Content-Disposition", f'attachment; filename="{context_id}.zip"'
            )
            return zip_output.getvalue()
        else:
            response.setHeader(
                "Content-Disposition", f'attachment; filename="{context_id}.xml"'
            )
            response.setHeader("Content-Type", "text/xml")
            return rendered_xml

    def render(self):
        if self.request.response.headers.get("content-disposition", "").startswith(
            "attachment"
        ):
            # We just generated an attachment, no need to render the form
            return ""
        return super().render()

    def exportImage(self, parent, image, caption=None, tagname="image"):
        """:returns: base64 encoded image."""
        if not self.include_images:
            return
        node = etree.SubElement(parent, tagname)
        if image.contentType:
            node.attrib["content-type"] = image.contentType
        if image.filename:
            node.attrib["filename"] = image.filename
        if caption:
            node.attrib["caption"] = caption
        node.text = encodebytes(safe_bytes(image.data))
        return node

    def exportSurvey(self, parent, survey):
        """Export a survey given a parent and the survey itself.

        :returns: An XML node with the details of an :obj:`euphorie.content.survey`.
        """
        node = etree.SubElement(parent, "survey")
        if getattr(survey, "external_id", None):
            node.attrib["external-id"] = survey.external_id
        etree.SubElement(node, "title").text = aq_parent(survey).title
        if self.include_intro_text and StripMarkup(survey.introduction):
            node = self._add_string_or_html(node, survey.introduction, "introduction")
        if survey.classification_code:
            etree.SubElement(node, "classification-code").text = (
                survey.classification_code
            )
        etree.SubElement(node, "language").text = survey.language
        report_completion_threshold = getattr(
            survey, "report_completion_threshold", False
        )
        if report_completion_threshold:
            etree.SubElement(
                node,
                "report_completion_threshold",
                attrib={"value": str(report_completion_threshold)},
            )
        enable_web_training = getattr(survey, "enable_web_training", False)
        if enable_web_training:
            etree.SubElement(node, "enable_web_training", attrib={"value": "true"})

        enable_test_questions = getattr(survey, "enable_test_questions", False)
        if enable_test_questions:
            etree.SubElement(node, "enable_test_questions", attrib={"value": "true"})

        enable_email_reminder = getattr(survey, "enable_email_reminder", False)
        if enable_email_reminder:
            etree.SubElement(node, "enable_email_reminder", attrib={"value": "true"})
        num_training_questions = getattr(survey, "num_training_questions", False)
        if num_training_questions:
            etree.SubElement(
                node,
                "num_training_questions",
                attrib={"value": str(num_training_questions)},
            )
        if self.is_etranslate_compatible:
            etree.SubElement(node, "tool_type", attrib={"value": get_tool_type(survey)})
            etree.SubElement(
                node,
                "measures_text_handling",
                attrib={"value": getattr(survey, "measures_text_handling", "full")},
            )
            etree.SubElement(
                node,
                "integrated_action_plan",
                attrib={
                    "value": (
                        "true"
                        if getattr(survey, "integrated_action_plan", False)
                        else "false"
                    )
                },
            )
            etree.SubElement(
                node,
                "evaluation-algorithm",
                attrib={"value": aq_parent(survey).evaluation_algorithm},
            )
            etree.SubElement(
                node,
                "evaluation-optional",
                attrib={"value": "true" if survey.evaluation_optional else "false"},
            )
        else:
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
            self.exportImage(
                node, survey.external_site_logo, tagname="external_site_logo"
            )
        if getattr(survey, "image", None):
            self.exportImage(node, survey.image)

        for child in survey.values():
            if IProfileQuestion.providedBy(child):
                self.exportProfileQuestion(node, child)
            if IModule.providedBy(child):
                self.exportModule(node, child)
            if ITrainingQuestion.providedBy(child):
                self.exportTrainingQuestion(node, child)
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
        if HasText(profile.question):
            node = self._add_string_or_html(node, profile.question, "question")
        else:
            etree.SubElement(node, "question").text = profile.title
        if HasText(profile.description):
            node = self._add_string_or_html(node, profile.description, "description")
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

        module_kwargs = {"optional": "true" if module.optional else "false"}
        if getattr(module, "hide_from_training", False):
            module_kwargs["hide_from_training"] = "true"
        node = etree.SubElement(parent, "module", **module_kwargs)

        if getattr(module, "external_id", None):
            node.attrib["external-id"] = module.external_id
        etree.SubElement(node, "title").text = module.title
        if self.include_module_description_texts and HasText(module.description):
            node = self._add_string_or_html(node, module.description, "description")
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
        node = self._add_string_or_html(node, risk.description, "description")
        if self.include_risk_legal_texts and StripMarkup(risk.legal_reference):
            node = self._add_string_or_html(
                node, risk.legal_reference, "legal-reference"
            )
        if self.is_etranslate_compatible:
            etree.SubElement(
                node,
                "show-not-applicable",
                attrib={"value": "true" if risk.show_notapplicable else "false"},
            )
        else:
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
        stripped_action = StripUnwanted(solution.action)
        if ISolution.providedBy(solution) and self.is_etranslate_compatible:
            solution_view = api.content.get_view(
                context=solution, name="nuplone-view", request=self.request
            )
            action_with_br = stripped_action.replace("\n", "<br/>")
            action_html = solution_view.render_md(action_with_br)
            fragment = html.fragment_fromstring(action_html, "action")
            node.append(fragment)
        else:
            etree.SubElement(node, "action").text = stripped_action
        if solution.requirements:
            etree.SubElement(node, "requirements").text = StripUnwanted(
                solution.requirements
            )
        return node

    def exportTrainingQuestion(self, parent, training_question):
        """:returns: An XML node with the details
        of an :obj:`euphorie.training_question`."""
        node = etree.SubElement(parent, "training_question")
        etree.SubElement(node, "title").text = StripUnwanted(training_question.title)
        etree.SubElement(node, "right_answer").text = StripUnwanted(
            training_question.right_answer
        )
        etree.SubElement(node, "wrong_answer_1").text = StripUnwanted(
            training_question.wrong_answer_1
        )
        etree.SubElement(node, "wrong_answer_2").text = StripUnwanted(
            training_question.wrong_answer_2
        )
        return node
