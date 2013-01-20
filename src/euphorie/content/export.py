from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from lxml import etree
from euphorie.content.survey import ISurvey
from euphorie.content.solution import ISolution
from euphorie.content.risk import IRisk
from euphorie.content.risk import IKinneyEvaluation
from euphorie.content.module import IModule
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.content.upload import NSMAP
from euphorie.content.utils import StripMarkup
from euphorie.client.utils import HasText


def getToken(field, value, default=None):
    try:
        return field.vocabulary.getTerm(value).token
    except LookupError:
        return None


class ExportSurvey(grok.View):
    grok.context(ISurvey)
    grok.require("zope2.View")
    grok.name("export")

    def __init__(self, context, request):
        super(ExportSurvey, self).__init__(context, request)
        nsmap = NSMAP.copy()
        del nsmap[None]

    def exportImage(self, parent, image, caption=None):
        node = etree.SubElement(parent, "image")
        if image.contentType:
            node.attrib["content-type"] = image.contentType
        if image.filename:
            node.attrib["filename"] = image.filename
        if caption:
            node.attrib["caption"] = caption
        node.text = image.data.encode("base64")
        return node

    def exportSurvey(self, parent, survey):
        node = etree.SubElement(parent, "survey")
        if getattr(survey, "external_id", None):
            node.attrib["external-id"] = survey.external_id
        etree.SubElement(node, "title").text = aq_parent(survey).title
        if StripMarkup(survey.introduction):
            etree.SubElement(node, "introduction").text = survey.introduction
        if survey.classification_code:
            etree.SubElement(node, "classification_code").text = \
                    survey.classification_code
        etree.SubElement(node, "language").text = survey.language
        etree.SubElement(node, "evaluation-algorithm").text = \
                aq_parent(survey).evaluation_algorithm
        etree.SubElement(node, "evaluation-optional").text = \
                "true" if survey.evaluation_optional else "false"

        for child in survey.values():
            if IProfileQuestion.providedBy(child):
                self.exportProfileQuestion(node, child)
            if IModule.providedBy(child):
                self.exportModule(node, child)
        return node

    def exportProfileQuestion(self, parent, profile):
        node = etree.SubElement(parent, "profile-question")
        if getattr(profile, "external_id", None):
            node.attrib["external-id"] = profile.external_id
        etree.SubElement(node, "title").text = profile.title
        # Use title if question is not available (Euphorie < 2.0rc2 data)
        etree.SubElement(node, "question").text = \
                profile.question or profile.title
        if HasText(profile.description):
            etree.SubElement(node, "description").text = profile.description

        for child in profile.values():
            if IModule.providedBy(child):
                self.exportModule(node, child)
            elif IRisk.providedBy(child):
                self.exportRisk(node, child)
        return node

    def exportModule(self, parent, module):
        node = etree.SubElement(parent, "module",
                optional="true" if module.optional else "false")
        if getattr(module, "external_id", None):
            node.attrib["external-id"] = module.external_id
        etree.SubElement(node, "title").text = module.title
        if HasText(module.description):
            etree.SubElement(node, "description").text = module.description
        if module.optional:
            etree.SubElement(node, "question").text = module.question
        if StripMarkup(module.solution_direction):
            etree.SubElement(node, "solution-direction").text = \
                    module.solution_direction
        if module.image is not None:
            self.exportImage(node, module.image, module.caption)

        for child in module.values():
            if IModule.providedBy(child):
                self.exportModule(node, child)
            elif IRisk.providedBy(child):
                self.exportRisk(node, child)
        return node

    def exportRisk(self, parent, risk):
        node = etree.SubElement(parent, "risk", type=risk.type)
        if getattr(risk, "external_id", None):
            node.attrib["external-id"] = risk.external_id
        etree.SubElement(node, "title").text = risk.title
        etree.SubElement(node, "problem-description").text = \
                risk.problem_description
        etree.SubElement(node, "description").text = risk.description
        if StripMarkup(risk.legal_reference):
            etree.SubElement(node, "legal-reference").text = \
                    risk.legal_reference
        etree.SubElement(node, "show-not-applicable").text = \
                "true" if risk.show_notapplicable else "false"
        if risk.type == "risk":
            method = etree.SubElement(node, "evaluation-method")
            method.text = risk.evaluation_method
            if risk.evaluation_method == "calculated":
                if risk.evaluation_algorithm() == "kinney":
                    if risk.default_probability:
                        method.attrib["default-probability"] = getToken(
                                IKinneyEvaluation["default_probability"],
                                risk.default_probability)
                    if risk.default_frequency:
                        method.attrib["default-frequency"] = getToken(
                                IKinneyEvaluation["default_frequency"],
                                risk.default_frequency)
                    if risk.default_effect:
                        method.attrib["default-effect"] = getToken(
                                IKinneyEvaluation["default_effect"],
                                risk.default_effect)
            elif risk.evaluation_method == "direct":
                if risk.default_priority:
                    method.attrib["default-priority"] = getToken(
                            IRisk["default_priority"], risk.default_priority)

        for index in range(4):
            postfix = "" if not index else str(index + 1)
            image = getattr(risk, "image" + postfix, None)
            if image is not None:
                self.exportImage(node, image,
                        getattr(risk, "caption" + postfix, None))

        solutions = [child for child in risk.values()
                        if ISolution.providedBy(child)]
        if solutions:
            sols = etree.SubElement(node, "solutions")
            for solution in solutions:
                self.exportSolution(sols, solution)
        return node

    def exportSolution(self, parent, solution):
        node = etree.SubElement(parent, "solution")
        if getattr(solution, "external_id", None):
            node.attrib["external-id"] = solution.external_id
        etree.SubElement(node, "description").text = solution.description
        etree.SubElement(node, "action-plan").text = solution.action_plan
        if solution.prevention_plan:
            etree.SubElement(node, "prevention-plan").text = \
                    solution.prevention_plan
        if solution.requirements:
            etree.SubElement(node, "requirements").text = solution.requirements
        return node

    def render(self):
        output = etree.Element("sector", nsmap=NSMAP)
        self.exportSurvey(output, self.context)
        response = self.request.response
        filename = "%s.xml" % aq_parent(aq_inner(self.context)).id
        response.setHeader(
                "Content-Disposition", u"attachment; filename=\"%s\"" %
                filename)
        response.setHeader("Content-Type", "text/xml")
        return etree.tostring(output, pretty_print=True, xml_declaration=True,
                encoding="utf-8")
