# coding=utf-8
from collections import OrderedDict
from datetime import date
from docx.api import Document
from euphorie.client import MessageFactory as _
from euphorie.client import model
from euphorie.client.docx.html import HtmlToWord
from euphorie.client.interfaces import IItalyReportPhaseSkinLayer
from euphorie.client.session import SessionManager
from euphorie.content.survey import get_tool_type
from euphorie.content.utils import IToolTypesInfo
from euphorie.content.utils import UNWANTED
from json import loads
from lxml import etree
from pkg_resources import resource_filename
from plonetheme.nuplone.utils import formatDate
from z3c.appconfig.interfaces import IAppConfig
from zope.component import getUtility
from zope.i18n import translate
import htmllaundry
import re
from plone.memoize.view import memoize

all_breaks = re.compile('(\n|\r)+')
multi_spaces = re.compile('( )+')


def _sanitize_html(txt):
    txt = all_breaks.sub(" ", txt)
    txt = UNWANTED.sub("", txt)
    txt = multi_spaces.sub(" ", txt)
    return txt


def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


def node_title(node, zodbnode):
    # 2885: Non-present risks and unanswered risks are shown affirmatively,
    # i.e 'title'
    if node.type != "risk" or node.identification in [u"n/a", u"yes", None]:
        return node.title
    # The other two groups of risks are shown negatively, i.e
    # 'problem_description'
    if zodbnode.problem_description and zodbnode.problem_description.strip():
        return zodbnode.problem_description
    return node.title


class BaseOfficeCompiler(object):

    def xmlprint(self, obj):
        ''' Utility method that pretty prints the xml serialization of obj.
        Useful in tests and in depug
        '''
        obj = getattr(obj, '_element', obj)
        return etree.tostring(obj, pretty_print=True)

    def t(self, txt):
        return translate(txt, context=self.request)

    @property
    @memoize
    def lang(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        return lang

    @property
    def title_custom_risks(self):
        return translate(_(
            'title_other_risks', default=u'Added risks (by you)'),
            target_language=self.lang)

    @property
    def session(self):
        return SessionManager.session


class DocxCompiler(BaseOfficeCompiler):

    # The template is the compiled one taken from #15664
    # The not compiled one has different styles
    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira.docx',
    )

    def __init__(self, context, request=None):
        ''' Read the docx template and initialize some instance attributes
        that will be used to compile the template
        '''
        self.context = context
        self.request = request
        self.template = Document(self._template_filename)
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.use_existing_measures = settings.get(
            'use_existing_measures', False)
        self.tool_type = get_tool_type(self.context)
        self.tti = getUtility(IToolTypesInfo)

    def set_session_title_row(self, data):
        ''' This fills the workspace activity run with some text
        '''
        request = self.request
        self.template.paragraphs[0].text = data['heading']
        txt = self.t(_("toc_header", default=u"Contents"))
        par_contents = self.template.paragraphs[1]
        par_contents.text = txt
        par_toc = self.template.paragraphs[2]
        for nodes, heading in zip(data["nodes"], data["section_headings"]):
            if not nodes:
                continue
            par_toc.insert_paragraph_before(heading, style="TOC Heading 1")
        survey = request.survey

        header = self.template.sections[0].header
        header_table = header.tables[0]
        header_table.cell(0, 0).paragraphs[0].text = data['title']
        header_table.cell(0, 1).paragraphs[0].text = formatDate(
            request, date.today())

        footer_txt = self.t(
            _("report_survey_revision",
                default=u"This document was based on the OiRA Tool '${title}' "
                        u"of revision date ${date}.",
                mapping={"title": survey.published[1],
                         "date": formatDate(request, survey.published[2])}))
        footer = self.template.sections[0].footer
        paragraph = footer.tables[0].cell(0, 0).paragraphs[0]
        paragraph.style = "Footer"
        paragraph.text = footer_txt

    def set_body(self, data, **extra):
        for nodes, heading in zip(data["nodes"], data["section_headings"]):
            if not nodes:
                continue
            self.add_report_section(nodes, heading, **extra)

    def add_report_section(self, nodes, heading, **extra):
        doc = self.template
        doc.add_paragraph(heading, style="Heading 1")

        survey = self.request.survey
        for node in nodes:
            zodb_node = None
            if node.zodb_path == 'custom-risks':
                title = self.title_custom_risks
            elif getattr(node, 'is_custom_risk', None):
                title = node.title
            else:
                zodb_node = survey.restrictedTraverse(
                    node.zodb_path.split("/"))
                title = node_title(node, zodb_node)

            number = node.number
            if 'custom-risks' in node.zodb_path:
                num_elems = number.split('.')
                number = u".".join([u"Ω"] + num_elems[1:])

            doc.add_paragraph(
                u"%s %s" % (number, title),
                style="Heading %d" % (node.depth + 1))

            if node.type != "risk":
                continue

            if extra.get('show_risk_state', False):
                msg = ''
                if node.identification == 'no':
                    msg = _("risk_present",
                            default="Risk is present.")
                elif node.postponed or not node.identification:
                    msg = _(
                        "risk_unanswered",
                        default=u"This risk still needs to be inventorised.")
                elif (
                    node.identification in [u"n/a", u"yes"] and
                    node.risk_type == "top5"
                ):
                    msg = _(
                        "top5_risk_not_present",
                        default=u"This risk is not present in your "
                        u"organisation, but since the sector organisation "
                        u"considers this one of the priority risks it must "
                        u"be included in this report.")
                if msg:
                    doc.add_paragraph(self.t(msg), style="RiskPriority")

            if node.priority and extra.get('show_priority', True):
                if node.priority == "low":
                    level = _("risk_priority_low", default=u"low")
                elif node.priority == "medium":
                    level = _("risk_priority_medium", default=u"medium")
                elif node.priority == "high":
                    level = _("risk_priority_high", default=u"high")

                msg = _("risk_priority",
                        default="This is a ${priority_value} priority risk.",
                        mapping={'priority_value': level})

                doc.add_paragraph(self.t(msg), style="RiskPriority")

            print_description = True
            # In the report for Italy, don't print the description
            if IItalyReportPhaseSkinLayer.providedBy(self.request):
                print_description = False
            if not getattr(node, 'identification', None) == 'no':
                if not extra.get('always_print_description', None) is True:
                    print_description = False

            if print_description:
                if zodb_node is None:
                    description = node.title
                else:
                    description = zodb_node.description

                doc = HtmlToWord(_sanitize_html(description), doc)

            if node.comment and node.comment.strip():
                doc.add_paragraph(node.comment, style="Comment")

            if not extra.get('skip_legal_references', True):
                legal_reference = getattr(zodb_node, "legal_reference", None)
                if legal_reference and legal_reference.strip():
                    doc.add_paragraph()
                    legal_heading = translate(_(
                                'header_legal_references',
                                default=u'Legal and policy references'),
                                target_language=self.lang,
                    )
                    doc.add_paragraph(legal_heading, style="Legal Heading")
                    doc = HtmlToWord(_sanitize_html(legal_reference), doc)

            skip_planned_measures = extra.get('skip_planned_measures', False)
            if (
                self.use_existing_measures and
                self.tool_type in self.tti.types_existing_measures and
                not extra.get('skip_existing_measures', False)
            ):
                if IItalyReportPhaseSkinLayer.providedBy(self.request):
                    skip_planned_measures = True
                if zodb_node is None:
                    defined_measures = []
                else:
                    defined_measures = zodb_node.get_pre_defined_measures(
                        self.request)
                try:
                    # We try to get at least some order in: First, the pre-
                    # defined measures that the user has confirmed, then the
                    # additional custom-defined ones.
                    existing_measures = OrderedDict()
                    saved_measures = loads(node.existing_measures)
                    for text in defined_measures:
                        if saved_measures.get(text):
                            existing_measures.update(
                                {htmllaundry.StripMarkup(text): 1})
                            saved_measures.pop(text)
                    # Finally, add the user-defined measures as well
                    existing_measures.update({
                        htmllaundry.StripMarkup(key): val for (key, val)
                        in saved_measures.items()})
                    measures = existing_measures.keys()
                except:
                    measures = []
                for (idx, measure) in enumerate(measures):
                    heading = self.t(
                        _(
                            "label_existing_measure",
                            default="Measure already implemented"
                        )
                    ) + " " + str(idx + 1)
                    action_plan = model.ActionPlan()
                    action_plan.action_plan = measure
                    self.add_measure(
                        doc, heading, action_plan, implemented=True)

            if not skip_planned_measures:
                for (idx, measure) in enumerate(node.action_plans):
                    if not measure.action_plan:
                        continue

                    if len(node.action_plans) == 1:
                        heading = self.t(
                            _("header_measure_single", default=u"Measure"))
                    else:
                        heading = self.t(
                            _("header_measure",
                                default=u"Measure ${index}",
                                mapping={"index": idx + 1}))
                    self.add_measure(doc, heading, measure)

    def add_measure(self, doc, heading, measure, implemented=False):
        doc.add_paragraph(heading, style="Measure Heading")
        headings = [
            self.t(_(
                "label_measure_action_plan",
                default=u"General approach (to "
                u"eliminate or reduce the risk)")),
        ]
        if not implemented:
            headings = headings + [
                self.t(_(
                    "label_measure_prevention_plan",
                    default=u"Specific action(s) required to implement this "
                    u"approach")),
                self.t(_(
                    "label_measure_requirements",
                    default=u"Level of expertise and/or requirements needed")),
                self.t(_(
                    "label_action_plan_responsible",
                    default=u"Who is responsible?")),
                self.t(_(
                    "label_action_plan_budget", default=u"Budget")),
                self.t(_(
                    "label_action_plan_start", default=u"Planning start")),
                self.t(_(
                    "label_action_plan_end", default=u"Planning end")),
            ]

        m = measure
        values = [
            m.action_plan,
        ]
        if not implemented:
            values = values + [
                m.prevention_plan,
                m.requirements,
                m.responsible,
                m.budget and str(m.budget) or '',
                m.planning_start and formatDate(
                    self.request, m.planning_start) or '',
                m.planning_end and formatDate(
                    self.request, m.planning_end) or '',
            ]
        for heading, value in zip(headings, values):
            doc.add_paragraph(heading, style="MeasureField")
            doc = HtmlToWord(value, doc, style="MeasureText")

    def compile(self, data):
        '''
        '''
        self.set_session_title_row(data)
        self.set_body(data)


class IdentificationReportCompiler(DocxCompiler):

    def set_session_title_row(self, data):

        request = self.request
        survey = request.survey

        # Remove existing paragraphs
        for paragraph in self.template.paragraphs:
            delete_paragraph(paragraph)

        header = self.template.sections[0].header
        header_table = header.tables[0]
        header_table.cell(0, 0).paragraphs[0].text = data['title']
        header_table.cell(0, 1).paragraphs[0].text = formatDate(
            request, date.today())

        footer_txt = self.t(
            _("report_identification_revision",
                default=u"This document was based on the OiRA Tool '${title}' "
                        u"of revision date ${date}.",
                mapping={"title": survey.published[1],
                         "date": formatDate(request, survey.published[2])}))

        footer = self.template.sections[0].footer
        paragraph = footer.tables[0].cell(0, 0).paragraphs[0]
        paragraph.style = "Footer"
        paragraph.text = footer_txt

    def compile(self, data):
        '''
        '''
        self.set_session_title_row(data)
        self.set_body(
            data,
            show_priority=False,
            always_print_description=True,
            skip_legal_references=False,
            skip_existing_measures=True,
            skip_planned_measures=True,
        )
