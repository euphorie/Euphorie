# coding=utf-8
from collections import OrderedDict
from copy import deepcopy
from datetime import date
from docx.api import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from euphorie.client import MessageFactory as _
from euphorie.client import model
from euphorie.client.docx.html import HtmlToWord
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
from plone import api
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
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def title_custom_risks(self):
        return translate(_(
            'title_other_risks', default=u'Added risks (by you)'),
            target_language=self.lang)

    @property
    def session(self):
        return self.webhelpers.traversed_session.session

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
        self.italy_special = self.webhelpers.country == "it"

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

        survey = self.context.aq_parent

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

        survey = self.context.aq_parent
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
                elif (
                    (node.postponed or not node.identification) and
                    not node.risk_type == "top5"
                ):
                    msg = _(
                        "risk_unanswered",
                        default=u"This risk still needs to be inventorised.")
                if node.risk_type == "top5":
                    if node.postponed or not node.identification:
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

            if (
                node.priority and
                extra.get('show_priority', True) and
                not self.italy_special
            ):
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
            if self.italy_special:
                print_description = False
            if not getattr(node, 'identification', None) == 'no':
                if not extra.get('always_print_description', None) is True:
                    print_description = False

            if print_description:
                if zodb_node is None:
                    if 'custom-risks' in node.zodb_path:
                        description = (
                            getattr(node, 'custom_description', node.title)
                            or node.title
                        )
                    else:
                        description = node.title
                else:
                    description = zodb_node.description

                doc = HtmlToWord(_sanitize_html(description or ""), doc)

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
                if self.italy_special:
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
                    saved_measures = loads(node.existing_measures)
                    # Backwards compat. We used to save dicts in JSON before we
                    # switched to list of tuples.
                    if isinstance(saved_measures, dict):
                        saved_measures = [
                            (k, v) for (k, v) in saved_measures.items()]

                    saved_measure_texts = OrderedDict()
                    for text, on in saved_measures:
                        saved_measure_texts.update({text: on})

                    existing_measures = []
                    # Pick the pre-defined measures first
                    for text in defined_measures:
                        active = saved_measure_texts.get(text)
                        if active is not None:
                            # Only add the measures that are active
                            if active:
                                existing_measures.append((text, 1))
                            saved_measure_texts.pop(text)

                    # Finally, add the user-defined measures as well
                    for text, on in saved_measure_texts.items():
                        existing_measures.append((text, on))

                    measures = [item[0] for item in existing_measures if item[1]]
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

    def set_consultation_box(self):
        doc = self.template
        doc.add_paragraph()
        doc.add_paragraph()
        table = doc.add_table(rows=4, cols=1)
        color = '000000'

        row = table.rows[0]
        cell = row.cells[0]
        self.set_row_borders(row, settings=ALL_BORDERS, color=color)
        paragraph = cell.paragraphs[0]
        paragraph.style = "Heading 3"
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.text = self.t(_(
            "header_oira_report_consultation",
            default="Consultation of workers"))

        paragraph = cell.add_paragraph()
        paragraph.text = self.t(_(
                "paragraph_oira_consultation_of_workers",
                default="The undersigned hereby declare that the workers "
                        "have been consulted on the content of this "
                        "document."))

        paragraph = cell.add_paragraph()
        employer = self.t(_(
            "oira_consultation_employer",
            default="On behalf of the employer:"))
        workers = self.t(_(
            "oira_consultation_workers",
            default="On behalf of the workers:"))
        paragraph.text = u"{0}\t\t\t{1}".format(employer, workers)
        cell.add_paragraph()
        cell.add_paragraph()

        paragraph = cell.add_paragraph()
        paragraph.text = self.t(_("oira_survey_date", default="Date:"))
        cell.add_paragraph()
        cell.add_paragraph()

    def compile(self, data):
        '''
        '''
        self.set_session_title_row(data)
        self.set_body(data)
        self.set_consultation_box()


class DocxCompilerItalyOriginal(DocxCompiler):

    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira_it.docx',
    )
    paragraphs_offset = 29
    sections_offset = 1

    def compile(self, data):
        '''
        '''
        self.set_session_title_row(data)
        self.set_body(data)


class DocxCompilerFullTable(DocxCompiler):
    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira_fr.docx',
    )

    show_risk_descriptions = True
    only_anwered_risks = False
    use_measures_subheading = True
    risk_description_col = 1
    risk_answer_col = 2
    risk_measures_col = 3

    justifiable_map = {
        'yes': 'Oui',
        'no': 'Non',
    }

    title_extra = u""

    def __init__(self, context, request=None):
        super(DocxCompilerFullTable, self).__init__(context, request)

    def remove_row(self, row):
        tbl = row._parent._parent
        tr = row._tr
        tbl._element.remove(tr)

    @memoize
    def get_modules_table(self):
        ''' Returns the first table of the template,
        which contains the modules
        '''
        return self.template.tables[-1]

    @property
    def session_title_lookup(self):
        lookup = {
            0: {
                0: {"fname": "title", "title": _(u"label_title", default=u"Title")},
                2: {"title": _(u"label_report_staff", default=u"Staff who participated in the risk assessment")},
                4: {"fname": "today", "title": _(u"label_report_date", default=u"Date of editing")},
            }
        }
        return lookup

    def set_session_title_row(self, data):
        ''' This fills the workspace activity run with some text

        The run is empirically determined by studying the template.
        This is in a paragraph structure before the first table.
        Tou may want to change this if you change the template.
        Be aware that the paragraph is the 2nd only
        after this class is initialized.
        We have 2 fields to fill, all following the same principle
        '''

        data['today'] = formatDate(self.request, date.today())

        for row, values in self.session_title_lookup.items():
            for num, settings in values.items():
                self.template.paragraphs[self.paragraphs_offset + row].runs[num].text = api.portal.translate(
                    settings["title"])
                _r = self.template.paragraphs[self.paragraphs_offset + row + 1].runs[num]
                # This run should be set in two paragraphs (which appear clones)
                # One is inside a mc:Choice and the other is inside a mc:Fallback
                for subpar in _r._element.findall('.//%s' % qn('w:p')):
                    subpar.clear_content()
                    subrun = subpar.add_r()
                    subrun.text = data.get(settings.get("fname", ""), '') or ''
                    subrpr = subrun.get_or_add_rPr()
                    subrpr.get_or_add_rFonts()
                    subrpr.get_or_add_rFonts().set(qn('w:ascii'), 'CorpoS')
                    subrpr.get_or_add_rFonts().set(qn('w:hAnsi'), 'CorpoS')
                    subrpr.get_or_add_sz().set(qn('w:val'), '28')
                    szCs = OxmlElement('w:szCs')
                    szCs.attrib[qn('w:val')] = '14'
                    subrpr.append(szCs)

        if data["comment"]:
            self.template.paragraphs[
                self.paragraphs_offset + row + 2
            ].insert_paragraph_before(data["comment"])

        header = self.template.sections[self.sections_offset].header
        header.paragraphs[1].text = (
            u"{title}{extra}".format(
                title=data['survey_title'], extra=self.title_extra)
        )

        # And now we handle the document footer
        footer = self.template.sections[self.sections_offset].footer
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
        if self.show_risk_descriptions:
            HtmlToWord(risk['description'], cell)
        if risk['measures']:
            if self.show_risk_descriptions:
                cell.add_paragraph()
            if self.use_measures_subheading:
                cell.add_paragraph(
                    api.portal.translate(
                        _(u"report_measures_in_place", default=u"Measures already in place:")
                    ),
                    style="Risk Italics")
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
            paragraph.text = _simple_breaks(action['text'])
            if action.get('prevention_plan', None):
                paragraph = cell.add_paragraph(style="Measure Indent")
                run = paragraph.add_run()
                run.text = api.portal.translate(
                    _(u"report_actions", default=u"Actions:")
                )
                run.underline = True
                run = paragraph.add_run()
                run.text = u" "
                run = paragraph.add_run()
                run.text = _simple_breaks(action['prevention_plan'])
            if action.get('requirements', None):
                paragraph = cell.add_paragraph(style="Measure Indent")
                run = paragraph.add_run()
                run.text = api.portal.translate(
                    _(u"report_competences", default=u"Required expertise:")
                )
                run.underline = True
                run = paragraph.add_run()
                run.text = u" "
                run = paragraph.add_run()
                run.text = _simple_breaks(action['requirements']),

            if action.get('responsible', None):
                paragraph = cell.add_paragraph(
                    api.portal.translate(
                        _(
                            u"report_responsible",
                            default=u"Responsible: ${responsible_name}",
                            mapping={"responsible_name": action['responsible']}
                        )
                    ),
                    style="Measure Indent"
                )
                paragraph.runs[0].italic = True
            if action.get('planning_end', None):
                paragraph = cell.add_paragraph(
                    api.portal.translate(
                        _(
                            u"report_end_date",
                            default=u"To be done by: ${date}",
                            mapping={"date": action['planning_end']}
                        )
                    ),
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

        unanswered_risks = []
        not_applicable_risks = []

        for module in modules:
            risks = module['risks']
            if not risks:
                continue
            row_module = table.add_row()
            cell = row_module.cells[0]
            cell.paragraphs[0].text = module.get('title', '')
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            self.set_row_borders(row_module)
            count = 0
            for risk in risks:
                answer = risk.get('justifiable', '')
                # In case our report type defines this: Omit risk if the user has not anwered it
                if self.only_anwered_risks:
                    if not answer:
                        unanswered_risks.append(risk)
                        continue
                # Not applicable risks are never shown in the regular table
                if answer == "n/a":
                    not_applicable_risks.append(risk)
                    continue
                if count:
                    row_risk = table.add_row()
                else:
                    row_risk = row_module
                count += 1
                self.set_cell_risk(row_risk.cells[self.risk_description_col], risk)
                if self.risk_answer_col is not None:
                    row_risk.cells[self.risk_answer_col].text = (
                        self.justifiable_map.get(answer) or ""
                    )
                self.set_cell_actions(row_risk.cells[self.risk_measures_col], risk)

                if count:
                    self.merge_module_rows(row_module, row_risk)

            if count:
                # set borders on last risk row, but not the top
                settings = deepcopy(ALL_BORDERS)
                settings['top'] = False
                self.set_row_borders(row_risk, settings=settings)

        def _merge_cells(cells):
            """
            Merge all given cells into one
            """
            if len(cells) < 2:
                return cells
            cell1, rest = cells[0], cells[1:]
            cell1_new = cell1
            for cell in rest:
                cell1_new = cell1_new.merge(cell)
            return cell1_new

        # Finally, an empty row at the end
        row = table.add_row()
        self.set_row_borders(row)
        # The first cell stays as it is, the second cell will be merged with all following cells
        _merge_cells(row.cells[1:])

        return unanswered_risks, not_applicable_risks

    def add_extra(self, unanswered_risks, not_applicable_risks):
        pass

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
        unanswered_risks, not_applicable_risks = self.set_modules_rows(data)

        # Finally clean up the modules table
        modules_table = self.get_modules_table()
        self.remove_row(modules_table.rows[1])

        # Add extra, where required
        self.add_extra(unanswered_risks, not_applicable_risks)


class DocxCompilerFrance(DocxCompilerFullTable):
    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira_fr.docx',
    )

    title_extra = u"- Evaluation des risques professionnels"


class DocxCompilerItaly(DocxCompilerFullTable):
    """ WIP: Copy of the French report"""

    sections_offset = 1
    paragraphs_offset = 32

    _template_filename = resource_filename(
        'euphorie.client.docx',
        'templates/oira_it_table.docx',
    )

    show_risk_descriptions = False
    use_measures_subheading = False
    only_anwered_risks = True
    risk_answer_col = None
    risk_measures_col = 2

    @property
    def session_title_lookup(self):
        lookup = {
            0: {
                0: {"fname": "title", "title": _(u"label_title", default=u"Title")},
            }
        }
        return lookup

    def add_extra(self, unanswered_risks, not_applicable_risks):
        doc = self.template

        def print_risk(risk):
            p = doc.add_paragraph(style="List Bullet")
            run = p.add_run()
            run.font.bold = True
            run.text = risk["number"]
            run = p.add_run()
            run.text = u" %s" % risk["title"]

        if not_applicable_risks:
            doc.add_paragraph()
            doc.add_paragraph(
                u"Adempimenti e rischi non applicabili",
                style="Heading 2")
            for risk in not_applicable_risks:
                print_risk(risk)

        if unanswered_risks:
            doc.add_paragraph()
            doc.add_paragraph(
                u"I seguenti rischi non sono stati ancora valutati",
                style="Heading 2")
            doc.add_paragraph()
            for risk in unanswered_risks:
                print_risk(risk)


class IdentificationReportCompiler(DocxCompiler):

    def set_session_title_row(self, data):

        request = self.request
        survey = self.context.aq_parent

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
