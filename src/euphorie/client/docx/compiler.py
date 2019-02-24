# coding=utf-8
from collections import OrderedDict
from copy import deepcopy
from datetime import date
from docx.api import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
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
from plone.memoize.view import memoize
from plonetheme.nuplone.utils import formatDate
from z3c.appconfig.interfaces import IAppConfig
from zope.component import getUtility
from zope.i18n import translate
import htmllaundry
import re

all_breaks = re.compile('(\n|\r)+')
multi_spaces = re.compile('( )+')

BORDER_COLOR = '9E9E9E'
ALL_BORDERS = dict(top=True, right=True, bottom=True, left=True)
LEFT_RIGHT_BORDERS = dict(top=False, right=True, bottom=False, left=True)


def _sanitize_html(txt):
    txt = all_breaks.sub(" ", txt)
    txt = UNWANTED.sub("", txt)
    txt = multi_spaces.sub(" ", txt)
    return txt


def _simple_breaks(txt):
    txt = all_breaks.sub('\n', txt)
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

    justifiable_map = {
        'yes': 'Yes',
        'no': 'No',
    }

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


    def set_cell_border(self, cell, settings=ALL_BORDERS, color=BORDER_COLOR):
        tcPr = cell._element.tcPr
        tcBorders = OxmlElement('w:tcBorders')

        bottom = OxmlElement('w:bottom')
        if settings.get('bottom', False):
            bottom.set(qn('w:val'), 'single')
            bottom.set(qn('w:sz'), '4')
            bottom.set(qn('w:space'), '0')
            bottom.set(qn('w:color'), color)
        else:
            bottom.set(qn('w:val'), 'nil')

        top = OxmlElement('w:top')
        if settings.get('top', False):
            top.set(qn('w:val'), 'single')
            top.set(qn('w:sz'), '4')
            top.set(qn('w:space'), '0')
            top.set(qn('w:color'), color)
        else:
            top.set(qn('w:val'), 'nil')

        left = OxmlElement('w:left')
        if settings.get('left', False):
            left.set(qn('w:val'), 'single')
            left.set(qn('w:sz'), '4')
            left.set(qn('w:space'), '0')
            left.set(qn('w:color'), color)
        else:
            left.set(qn('w:val'), 'nil')

        right = OxmlElement('w:right')
        if settings.get('right', False):
            right.set(qn('w:val'), 'single')
            right.set(qn('w:sz'), '4')
            right.set(qn('w:space'), '0')
            right.set(qn('w:color'), color)
        else:
            right.set(qn('w:val'), 'nil')

        tcBorders.append(top)
        tcBorders.append(left)
        tcBorders.append(bottom)
        tcBorders.append(right)
        tcPr.append(tcBorders)

    def set_row_borders(self, row, settings=ALL_BORDERS, color=BORDER_COLOR):
        for idx, cell in enumerate(row.cells):
            self.set_cell_border(cell, settings, color)


class DocxCompiler(BaseOfficeCompiler):

    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira.docx',
    )
    # In case of templates that contain additional content before the actual
    # first page, this can be defined by providing offsets to the first
    # paragraph for content and the first section for the header / footer.
    paragraphs_offset = 0
    sections_offset = 0

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
        self.template.paragraphs[self.paragraphs_offset].text = data['heading']
        txt = self.t(_("toc_header", default=u"Contents"))
        par_contents = self.template.paragraphs[self.paragraphs_offset + 1]
        par_contents.text = txt
        par_toc = self.template.paragraphs[self.paragraphs_offset + 2]
        for nodes, heading in zip(data["nodes"], data["section_headings"]):
            if not nodes:
                continue
            par_toc.insert_paragraph_before(heading, style="TOC Heading 1")
        survey = request.survey

        header = self.template.sections[self.sections_offset].header
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
        footer = self.template.sections[self.sections_offset].footer
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
                if node.risk_type == "top5":
                    if node.postponed:
                        msg = _(
                            "top5_risk_not_present",
                            default=u"This risk is not present in your "
                            u"organisation, but since the sector organisation "
                            u"considers this one of the priority risks it must "
                            u"be included in this report.")
                    elif node.identification == "yes":
                        # we need this distinction for Dutch RIE
                        msg = _(
                            "top5_risk_not_present_answer_yes",
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
            _simple_breaks(m.action_plan or ""),
        ]
        if not implemented:
            values = values + [
                _simple_breaks(m.prevention_plan or ""),
                _simple_breaks(m.requirements or ""),
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


class DocxCompilerItaly(DocxCompiler):

    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira_it.docx',
    )
    paragraphs_offset = 29
    sections_offset = 1


class DocxCompilerFrance(DocxCompiler):
    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira_fr.docx',
    )

    justifiable_map = {
        'yes': 'Oui',
        'no': 'Non',
    }

    def __init__(self, context, request=None):
        super(DocxCompilerFrance, self).__init__(context, request)

    def remove_row(self, row):
        tbl = row._parent._parent
        tr = row._tr
        tbl._element.remove(tr)

    @memoize
    def get_modules_table(self):
        ''' Returns the first table of the template,
        which contains the modules
        '''
        return self.template.tables[0]

    def set_session_title_row(self, data):
        ''' This fills the workspace activity run with some text

        The run is empirically determined by studying the template.
        This is in a paragraph structure before the first table.
        Tou may want to change this if you change the template.
        Be aware that the paragraph is the 2nd only
        after this class is initialized.
        We have 2 fields to fill, all following the same principle
        '''
        lookup = {
            0: "title",
            4: "today",
        }
        data['today'] = formatDate(self.request, date.today())

        for num, fname in lookup.items():
            _r = self.template.paragraphs[1].runs[num]
            # This run should be set in two paragraphs (which appear clones)
            # One is inside a mc:Choice and the other is inside a mc:Fallback
            for subpar in _r._element.findall('.//%s' % qn('w:p')):
                subpar.clear_content()
                subrun = subpar.add_r()
                subrun.text = data.get(fname, '') or ''
                subrpr = subrun.get_or_add_rPr()
                subrpr.get_or_add_rFonts()
                subrpr.get_or_add_rFonts().set(qn('w:ascii'), 'CorpoS')
                subrpr.get_or_add_rFonts().set(qn('w:hAnsi'), 'CorpoS')
                subrpr.get_or_add_sz().set(qn('w:val'), '32')
                szCs = OxmlElement('w:szCs')
                szCs.attrib[qn('w:val')] = '16'
                subrpr.append(szCs)

        header = self.template.sections[0].header
        header.paragraphs[1].text = (
            u"{} - Evaluation des risques professionnels".format(
                data['survey_title'])
        )

        # And now we handle the document footer
        footer = self.template.sections[0].footer
        # The footer contains a table with 3 columns:
        # left we have a logo, center for text, right for the page numbers
        cell1, cell2, cell3 = footer.tables[0].row_cells(0)
        cell2.paragraphs[0].text = u"{}".format(
            date.today().strftime("%d.%m.%Y"))

    def set_cell_risk(self, cell, risk):
        """ Take the risk and add the appropriate text:
            title, descripton, comment, measures in place
        """
        paragraph = cell.paragraphs[0]
        paragraph.style = "Risk Bold List"
        paragraph.text = risk['title']
        if risk['comment']:
            cell.add_paragraph(risk['comment'], style="Risk Normal")
        HtmlToWord(risk['description'], cell)
        if risk['measures']:
            cell.add_paragraph()
            cell.add_paragraph(u"Mesures déjà en place :", style="Risk Italics")
            for measure in risk['measures']:
                HtmlToWord(measure, cell, style="Risk Italics List")
        paragraph = cell.add_paragraph(style="Risk Normal")

    def set_cell_actions(self, cell, risk):
        """ Take the risk and add the appropriate text:
            planned measures
        """
        paragraph = cell.paragraphs[0]
        for idx, action in enumerate(risk['actions']):
            if idx != 0:
                paragraph = cell.add_paragraph()
            paragraph.style = "Measure List"
            paragraph.text = action['text']
            if action.get('prevention_plan', None):
                paragraph = cell.add_paragraph(
                    action['prevention_plan'],
                    style="Measure Indent")
            if action.get('requirements', None):
                paragraph = cell.add_paragraph(
                    action['requirements'],
                    style="Measure Indent")
            if action.get('responsible', None):
                paragraph = cell.add_paragraph(
                    u"Responsable: {}".format(action['responsible']),
                    style="Measure Indent"
                )
                paragraph.runs[0].italic = True
            if action.get('planning_start', None):
                paragraph = cell.add_paragraph(
                    u"Date de fin: {}".format(action['planning_start']),
                    style="Measure Indent"
                )
                paragraph.runs[0].italic = True

    def merge_module_rows(self, row_module, row_risk):
        ''' This merges the the first cell of the given rows,
        the one containing the module title.
        Also remove the horizontal borders between the not merged cells.
        '''
        for idx in range(1):
            first_cell = row_module.cells[idx]
            last_cell = row_risk.cells[idx]
            self.set_cell_border(last_cell)
            first_cell.merge(last_cell)
        for idx, cell in enumerate(row_risk.cells[1:]):
            self.set_cell_border(cell, settings=LEFT_RIGHT_BORDERS)

    def set_modules_rows(self, data):
        ''' This takes a list of modules and creates the rows for them
        '''
        modules = data.get('modules', [])
        table = self.get_modules_table()

        for module in modules:
            risks = module['risks']
            if not risks:
                continue
            row_module = table.add_row()
            for r_idx, risk in enumerate(risks):
                if r_idx:
                    row_risk = table.add_row()
                else:
                    cell = row_module.cells[0]
                    cell.paragraphs[0].text = module.get('title', '')
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                    row_risk = row_module
                self.set_cell_risk(row_risk.cells[1], risk)
                row_risk.cells[2].text = self.justifiable_map.get(
                    risk.get('justifiable', '')
                ) or ""
                self.set_cell_actions(row_risk.cells[3], risk)

                if len(risks) > 1:
                    self.merge_module_rows(row_module, row_risk)

            # set borders on last risk row, but not the top
            settings = deepcopy(ALL_BORDERS)
            settings['top'] = False
            self.set_row_borders(row_risk, settings=settings)

        # # Set the footer row of the table
        # row = table.add_row()
        # self.set_row_borders(row)

        def _merge_cells(row):
            cell1, cell2, cell3, cell4 = row.cells
            cell2_new = cell2.merge(cell3)
            cell2_new = cell2_new.merge(cell4)
            return (cell1, cell2_new)

        # cell1_new, cell2_new = _merge_cells(row)
        # cell1_new.paragraphs[0].text = u"Freigegeben:"
        # txt = (
        #     data.get('publisher', None) and
        #     data['publisher'].loginname or u""
        # )
        # if data.get('published', None):
        #     if txt:
        #         txt = u"{} – ".format(txt)
        #     txt = u"{}{}".format(
        #         txt, data['published'].strftime('%d.%m.%Y'))
        # cell2_new.paragraphs[0].text = txt

        # Finally, an empty row at the end
        row = table.add_row()
        self.set_row_borders(row)
        _merge_cells(row)

    def compile(self, data):
        ''' Compile the template using data

        We need to compile two areas of the template:

        - the paragraph above the first table (containing the session title)
        - the first table (containing all the modules)

        data is a dict like object.
        Check the file .../daimler/oira/tests/mocked_data.py
        to understand its format
        '''
        self.set_session_title_row(data)
        self.set_modules_rows(data)

        # Finally clean up the modules table
        modules_table = self.get_modules_table()
        self.remove_row(modules_table.rows[1])


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
