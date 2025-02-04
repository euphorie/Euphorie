from copy import deepcopy
from datetime import date
from docx.api import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor
from euphorie.client import MessageFactory as _
from euphorie.client.docx.html import HtmlToWord
from euphorie.content.solution import ISolution
from euphorie.content.survey import get_tool_type
from euphorie.content.utils import IToolTypesInfo
from euphorie.content.utils import UNWANTED
from lxml import etree
from pkg_resources import resource_filename
from plone import api
from plone.memoize.view import memoize
from plonetheme.nuplone.utils import formatDate
from zope.component import getUtility
from zope.i18n import translate

import re


all_breaks = re.compile("(\n|\r)+")
multi_spaces = re.compile("( )+")

BORDER_COLOR = "9E9E9E"
ALL_BORDERS = dict(top=True, right=True, bottom=True, left=True)
LEFT_RIGHT_BORDERS = dict(top=False, right=True, bottom=False, left=True)


def _sanitize_html(txt):
    txt = all_breaks.sub(" ", txt)
    txt = UNWANTED.sub("", txt)
    txt = multi_spaces.sub(" ", txt)
    return txt


def _simple_breaks(txt):
    txt = all_breaks.sub("\n", txt)
    return txt


def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


def node_title(node, zodbnode):
    # 2885: Non-present risks and unanswered risks are shown affirmatively,
    # i.e 'title'
    if node.type != "risk" or node.identification in ["n/a", "yes", None]:
        return node.title
    # The other two groups of risks are shown negatively, i.e
    # 'problem_description'
    if zodbnode.problem_description and zodbnode.problem_description.strip():
        return zodbnode.problem_description
    return node.title


class BaseOfficeCompiler:
    justifiable_map = {"yes": "Yes", "no": "No"}

    def xmlprint(self, obj):
        """Utility method that pretty prints the xml serialization of obj.

        Useful in tests and in depug
        """
        obj = getattr(obj, "_element", obj)
        return etree.tostring(obj, pretty_print=True)

    def t(self, txt):
        return translate(txt, context=self.request)

    @property
    @memoize
    def lang(self):
        lang = getattr(self.request, "LANGUAGE", "en")
        if "-" in lang:
            elems = lang.split("-")
            lang = f"{elems[0]}_{elems[1].upper()}"
        return lang

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def template_by_sector_mapping(self):
        return api.portal.get_registry_record(
            "euphorie.client.docx.template_by_sector_mapping", default={}
        )

    @property
    @memoize
    def title_extra_by_sector_mapping(self):
        return api.portal.get_registry_record(
            "euphorie.client.docx.title_extra_by_sector_mapping", default={}
        )

    @property
    def title_custom_risks(self):
        return translate(
            _("label_custom_risks", default="Custom risks"),
            target_language=self.lang,
        )

    @property
    def session(self):
        return self.webhelpers.traversed_session.session

    def set_cell_border(self, cell, settings=ALL_BORDERS, color=BORDER_COLOR):
        tcPr = cell._element.tcPr
        tcBorders = OxmlElement("w:tcBorders")

        bottom = OxmlElement("w:bottom")
        if settings.get("bottom", False):
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "4")
            bottom.set(qn("w:space"), "0")
            bottom.set(qn("w:color"), color)
        else:
            bottom.set(qn("w:val"), "nil")

        top = OxmlElement("w:top")
        if settings.get("top", False):
            top.set(qn("w:val"), "single")
            top.set(qn("w:sz"), "4")
            top.set(qn("w:space"), "0")
            top.set(qn("w:color"), color)
        else:
            top.set(qn("w:val"), "nil")

        left = OxmlElement("w:left")
        if settings.get("left", False):
            left.set(qn("w:val"), "single")
            left.set(qn("w:sz"), "4")
            left.set(qn("w:space"), "0")
            left.set(qn("w:color"), color)
        else:
            left.set(qn("w:val"), "nil")

        right = OxmlElement("w:right")
        if settings.get("right", False):
            right.set(qn("w:val"), "single")
            right.set(qn("w:sz"), "4")
            right.set(qn("w:space"), "0")
            right.set(qn("w:color"), color)
        else:
            right.set(qn("w:val"), "nil")

        tcBorders.append(top)
        tcBorders.append(left)
        tcBorders.append(bottom)
        tcBorders.append(right)
        tcPr.append(tcBorders)

    def set_row_borders(self, row, settings=ALL_BORDERS, color=BORDER_COLOR):
        for idx, cell in enumerate(row.cells):
            self.set_cell_border(cell, settings, color)


class DocxCompiler(BaseOfficeCompiler):
    _base_filename = "oira.docx"

    use_solution_description = True

    @property
    def _template_filename(self):
        return resource_filename(
            "euphorie.client.docx", f"templates/{self._base_filename}"
        )

    # In case of templates that contain additional content before the actual
    # first page, this can be defined by providing offsets to the first
    # paragraph for content and the first section for the header / footer.
    paragraphs_offset = 0
    sections_offset = 0

    def __init__(self, context, request=None):
        """Read the docx template and initialize some instance attributes that
        will be used to compile the template."""
        self.context = context
        self.request = request
        self.template = Document(self._template_filename)

        self.compiler = HtmlToWord()

        self.use_existing_measures = api.portal.get_registry_record(
            "euphorie.use_existing_measures", default=False
        )
        self.tool_type = get_tool_type(self.webhelpers._survey)
        self.tti = getUtility(IToolTypesInfo)
        self.italy_special = self.webhelpers.country == "it"

    @property
    @memoize
    def survey(self):
        return self.context.aq_parent

    def set_session_title_row(self, data):
        """This fills the workspace activity run with some text."""
        request = self.request
        self.template.paragraphs[self.paragraphs_offset].text = data["heading"]
        txt = self.t(_("toc_header", default="Contents"))
        par_contents = self.template.paragraphs[self.paragraphs_offset + 1]
        par_contents.text = txt
        par_toc = self.template.paragraphs[self.paragraphs_offset + 2]
        for nodes, heading in zip(data["nodes"], data["section_headings"]):
            if not nodes:
                continue
            par_toc.insert_paragraph_before(heading, style="TOC Heading 1")

        if data.get("comment"):
            par_toc.insert_paragraph_before("")
            par_toc.insert_paragraph_before(data["comment"])

        survey = self.context.aq_parent

        header = self.template.sections[self.sections_offset].header
        header_table = header.tables[0]
        header_table.cell(0, 0).paragraphs[0].text = data["title"]
        header_table.cell(0, 1).paragraphs[0].text = formatDate(request, date.today())

        footer_txt = self.t(
            _(
                "report_survey_revision",
                default="This document was based on the OiRA Tool '${title}' "
                "of revision date ${date}.",
                mapping={
                    "title": survey.published[1],
                    "date": formatDate(request, survey.published[2]),
                },
            )
        )
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
            if node.zodb_path == "custom-risks":
                title = self.title_custom_risks
            elif getattr(node, "is_custom_risk", None):
                title = node.title
            else:
                zodb_node = survey.restrictedTraverse(node.zodb_path.split("/"))
                title = node_title(node, zodb_node)

            number = node.number
            if "custom-risks" in node.zodb_path:
                num_elems = number.split(".")
                number = ".".join(["Ω"] + num_elems[1:])

            doc.add_paragraph(
                f"{number} {title}", style="Heading %d" % (node.depth + 1)
            )

            if node.type != "risk":
                continue

            if extra.get("show_risk_state", False):
                msg = ""
                if node.identification == "no":
                    msg = _("risk_present", default="Risk is present.")
                elif (
                    node.postponed or not node.identification
                ) and not node.risk_type == "top5":
                    msg = _(
                        "risk_unanswered",
                        default="This risk still needs to be inventorised.",
                    )
                if node.risk_type == "top5":
                    if node.postponed or not node.identification:
                        msg = _(
                            "top5_risk_not_present",
                            default="This risk is not present in your "
                            "organisation, but since the sector organisation "
                            "considers this one of the priority risks it must "
                            "be included in this report.",
                        )
                    elif node.identification == "yes":
                        # we need this distinction for Dutch RIE
                        msg = _(
                            "top5_risk_not_present_answer_yes",
                            default="This risk is not present in your "
                            "organisation, but since the sector organisation "
                            "considers this one of the priority risks it must "
                            "be included in this report.",
                        )
                if msg:
                    doc.add_paragraph(self.t(msg), style="RiskPriority")

            if (
                node.priority
                and extra.get("show_priority", True)
                and not self.italy_special
            ):
                if node.priority == "low":
                    level = _("risk_priority_low", default="low")
                elif node.priority == "medium":
                    level = _("risk_priority_medium", default="medium")
                elif node.priority == "high":
                    level = _("risk_priority_high", default="high")

                msg = _(
                    "risk_priority",
                    default="This is a ${priority_value} priority risk.",
                    mapping={"priority_value": level},
                )

                doc.add_paragraph(self.t(msg), style="RiskPriority")

            print_description = True
            # In the report for Italy, don't print the description
            if self.italy_special:
                print_description = False
            if not getattr(node, "identification", None) == "no":
                if not extra.get("always_print_description", None) is True:
                    print_description = False

            if print_description:
                if zodb_node is None:
                    if "custom-risks" in node.zodb_path:
                        description = (
                            getattr(node, "custom_description", node.title)
                            or node.title
                        )
                    else:
                        description = node.title
                else:
                    description = zodb_node.description

                self.compiler(_sanitize_html(description or ""), doc)

            if node.comment and node.comment.strip():
                msg = translate(
                    _("heading_comments", default="Comments"), target_language=self.lang
                )
                doc.add_paragraph(msg, style="Measure Heading")
                self.compiler(_sanitize_html(node.comment or ""), doc)

            if not extra.get("skip_legal_references", True):
                legal_reference = getattr(zodb_node, "legal_reference", None)
                if legal_reference and legal_reference.strip():
                    doc.add_paragraph()
                    legal_heading = translate(
                        _(
                            "header_legal_references",
                            default="Legal and policy references",
                        ),
                        target_language=self.lang,
                    )
                    doc.add_paragraph(legal_heading, style="Legal Heading")
                    self.compiler(_sanitize_html(legal_reference), doc)

            if not extra.get("use_solutions", False):
                skip_planned_measures = extra.get("skip_planned_measures", False)
                skip_existing_measures = extra.get("skip_existing_measures", False)
                self.add_measures(
                    skip_planned_measures, skip_existing_measures, node, doc
                )
            elif zodb_node is not None:
                self.add_solutions(zodb_node, doc)

    def add_measures(self, skip_planned_measures, skip_existing_measures, node, doc):
        if (
            self.use_existing_measures
            and self.tool_type in self.tti.types_existing_measures
            and not skip_existing_measures
        ):
            if self.italy_special:
                skip_planned_measures = True

            for idx, action_plan in enumerate(
                node.in_place_standard_measures + node.in_place_custom_measures
            ):
                heading = (
                    self.t(
                        _(
                            "label_existing_measure",
                            default="Measure already implemented",
                        )
                    )
                    + " "
                    + str(idx + 1)
                )
                self.add_measure(doc, heading, action_plan, implemented=True)

        if not skip_planned_measures:
            action_plans = node.standard_measures + node.custom_measures
            for idx, measure in enumerate(action_plans):
                if not measure.action:
                    continue

                if len(action_plans) == 1:
                    heading = self.t(_("header_measure_single", default="Measure"))
                else:
                    heading = self.t(
                        _(
                            "header_measure",
                            default="Measure ${index}",
                            mapping={"index": idx + 1},
                        )
                    )
                self.add_measure(doc, heading, measure)

    def add_solutions(self, zodb_node, doc):
        for solution in zodb_node.values():
            if not ISolution.providedBy(solution):
                continue
            self.add_measure(doc, solution.description, solution, implemented=True)

    def add_measure(self, doc, heading, measure, implemented=False):
        doc.add_paragraph(heading, style="Measure Heading")
        headings = [
            self.t(
                _(
                    "label_measure_action_plan",
                    default="General approach (to " "eliminate or reduce the risk)",
                )
            )
        ]
        if not implemented:
            headings = headings + [
                self.t(
                    _(
                        "label_measure_requirements",
                        default="Level of expertise and/or requirements needed",
                    )
                ),
                self.t(
                    _("label_action_plan_responsible", default="Who is responsible?")
                ),
                self.t(_("label_action_plan_budget", default="Budget")),
                self.t(_("label_action_plan_start", default="Planning start")),
                self.t(_("label_action_plan_end", default="Planning end")),
            ]

        m = measure
        action = m.action
        if (
            self.use_solution_description
            and hasattr(measure, "plan_type")
            and measure.plan_type
            in [
                "in_place_standard",
                "measure_standard",
            ]
        ):
            action = "\n".join(
                (
                    self.survey.restrictedTraverse(
                        "/".join((measure.risk.zodb_path, measure.solution_id))
                    ).description,
                    action,
                )
            )
        values = [_simple_breaks(action or "")]
        if not implemented:
            values = values + [
                _simple_breaks(m.requirements or ""),
                m.responsible,
                m.budget and str(m.budget) or "",
                m.planning_start and formatDate(self.request, m.planning_start) or "",
                m.planning_end and formatDate(self.request, m.planning_end) or "",
            ]
        for heading, value in zip(headings, values):
            doc.add_paragraph(heading, style="MeasureField")
            self.compiler(value, doc, style="MeasureText")

    def set_consultation_box(self):
        doc = self.template
        doc.add_paragraph()
        doc.add_paragraph()
        table = doc.add_table(rows=4, cols=1)
        color = "000000"

        row = table.rows[0]
        cell = row.cells[0]
        self.set_row_borders(row, settings=ALL_BORDERS, color=color)
        paragraph = cell.paragraphs[0]
        paragraph.style = "Heading 3"
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.text = self.t(
            _("header_oira_report_consultation", default="Consultation of workers")
        )

        paragraph = cell.add_paragraph()
        paragraph.text = self.t(
            _(
                "paragraph_oira_consultation_of_workers",
                default="The undersigned hereby declare that the workers "
                "have been consulted on the content of this "
                "document.",
            )
        )

        paragraph = cell.add_paragraph()
        employer = self.t(
            _("oira_consultation_employer", default="On behalf of the employer:")
        )
        workers = self.t(
            _("oira_consultation_workers", default="On behalf of the workers:")
        )
        paragraph.text = f"{employer}\t\t\t{workers}"
        cell.add_paragraph()
        cell.add_paragraph()

        paragraph = cell.add_paragraph()
        paragraph.text = self.t(_("oira_survey_date", default="Date:"))
        cell.add_paragraph()
        cell.add_paragraph()

    def compile(self, data):
        """"""
        self.set_session_title_row(data)
        self.set_body(data)
        self.set_consultation_box()


class DocxCompilerItalyOriginal(DocxCompiler):
    _base_filename = "oira_it.docx"

    paragraphs_offset = 29
    sections_offset = 1

    def compile(self, data):
        """"""
        self.set_session_title_row(data)
        self.set_body(data)


class DocxCompilerFullTable(DocxCompiler):
    _base_filename = "oira_fr.docx"

    show_risk_descriptions = True
    only_anwered_risks = False
    use_measures_subheading = True
    show_priority = True
    risk_description_col = 1
    risk_answer_col = 2
    risk_measures_col = 3

    justifiable_map = {"yes": "Oui", "no": "Non"}

    title_extra = ""

    def __init__(self, context, request=None):
        super().__init__(context, request)

    def remove_row(self, row):
        tbl = row._parent._parent
        tr = row._tr
        tbl._element.remove(tr)

    @memoize
    def get_modules_table(self):
        """Returns the first table of the template, which contains the
        modules."""
        return self.template.tables[-1]

    @property
    def session_title_lookup(self):
        lookup = {
            0: {
                0: {"fname": "title", "title": _("label_title", default="Title")},
                2: {
                    "title": _(
                        "label_report_staff",
                        default="Staff who participated in the risk assessment",
                    )
                },
                4: {
                    "fname": "today",
                    "title": _("label_report_date", default="Date of editing"),
                },
            }
        }
        return lookup

    def set_session_title_row(self, data):
        """This fills the workspace activity run with some text.

        The run is empirically determined by studying the template. This
        is in a paragraph structure before the first table. Tou may want
        to change this if you change the template. Be aware that the
        paragraph is the 2nd only after this class is initialized. We
        have 2 fields to fill, all following the same principle
        """

        data["today"] = formatDate(self.request, date.today())

        for row, values in self.session_title_lookup.items():
            for num, settings in values.items():
                self.template.paragraphs[self.paragraphs_offset + row].runs[
                    num
                ].text = api.portal.translate(settings["title"])
                _r = self.template.paragraphs[self.paragraphs_offset + row + 1].runs[
                    num
                ]
                # This run should be set in two paragraphs (which appear clones)
                # One is inside a mc:Choice and the other is inside a mc:Fallback
                for subpar in _r._element.findall(".//%s" % qn("w:p")):
                    subpar.clear_content()
                    subrun = subpar.add_r()
                    subrun.text = data.get(settings.get("fname", ""), "") or ""
                    subrpr = subrun.get_or_add_rPr()
                    subrpr.get_or_add_rFonts()
                    subrpr.get_or_add_rFonts().set(qn("w:ascii"), "CorpoS")
                    subrpr.get_or_add_rFonts().set(qn("w:hAnsi"), "CorpoS")
                    subrpr.get_or_add_sz().set(qn("w:val"), "28")
                    szCs = OxmlElement("w:szCs")
                    szCs.attrib[qn("w:val")] = "14"
                    subrpr.append(szCs)

        if data["comment"]:
            self.template.paragraphs[
                self.paragraphs_offset + row + 2
            ].insert_paragraph_before(data["comment"])

        header = self.template.sections[self.sections_offset].header
        header.paragraphs[1].text = "{title}{extra}".format(
            title=data["survey_title"], extra=self.title_extra.strip()
        )

        # And now we handle the document footer
        footer = self.template.sections[self.sections_offset].footer
        # The footer contains a table with 3 columns:
        # left we have a logo, center for text, right for the page numbers
        cell1, cell2, cell3 = footer.tables[0].row_cells(0)
        cell2.paragraphs[0].text = "{}".format(date.today().strftime("%d.%m.%Y"))
        # Translate page number label
        # except template for Italy which has a different structure
        if cell3.tables:
            inner = cell3.tables[0].cell(0, 1)
            inner.paragraphs[0].runs[6].text = api.portal.translate(
                _(
                    "label_page_of",
                    default="of",
                ),
            )

    def set_table_header(self):
        # To be overridden in subclass
        pass

    def set_cell_risk(self, cell, risk):
        """Take the risk and add the appropriate text:

        title, descripton, comment, measures in place
        """
        self.set_cell_risk_title(cell, risk)
        self.set_cell_risk_comment(cell, risk)
        self.set_cell_risk_description(cell, risk)
        self.set_cell_risk_measures(cell, risk)

        cell.add_paragraph(style="Risk Normal")

    def set_cell_risk_priority(self, cell, risk):
        priority = risk.get("priority", "high")
        if priority:
            if priority == "low":
                level = _("risk_priority_low", default="low")
            elif priority == "medium":
                level = _("risk_priority_medium", default="medium")
            elif priority == "high":
                level = _("risk_priority_high", default="high")
            paragraph = cell.add_paragraph(
                "{}: {}".format(
                    api.portal.translate(
                        _("report_timeline_priority", default="Priority")
                    ),
                    api.portal.translate(level),
                ),
                style="Measure Indent",
            )
            paragraph.runs[0].italic = True

    def set_cell_risk_title(self, cell, risk):
        paragraph = cell.paragraphs[0]
        paragraph.style = "Risk Bold List"
        paragraph.text = risk["title"]
        if self.show_priority:
            self.set_cell_risk_priority(cell, risk)

    def set_cell_risk_comment(self, cell, risk):
        if risk["comment"] and risk["comment"].strip():
            self.compiler(risk["comment"], cell, style="Risk Normal")

    def set_cell_risk_description(self, cell, risk):
        if self.show_risk_descriptions:
            self.compiler(risk["description"], cell)

    def set_cell_risk_measures(self, cell, risk):
        if risk["measures"]:
            if self.show_risk_descriptions:
                cell.add_paragraph()
            if self.use_measures_subheading:
                cell.add_paragraph(
                    api.portal.translate(
                        _(
                            "report_measures_in_place",
                            default="Measures already in place:",
                        )
                    ),
                    style="Risk Italics",
                )
            for measure in risk["measures"]:
                self.compiler(_simple_breaks(measure), cell, style="Risk Italics List")

    def set_cell_actions(self, cell, risk):
        """Take the risk and add the appropriate text:

        planned measures
        """
        for idx, action in enumerate(risk["actions"]):
            if idx != 0:
                cell.add_paragraph()
            self.set_cell_action_text(cell, action)
            self.set_cell_action_responsible(cell, action)
            self.set_cell_action_date(cell, action)

    def set_cell_action_text(self, cell, action):
        action_text = action["text"]
        if self.use_solution_description and "solution_description" in action:
            action_text = "\n".join((action["solution_description"], action_text))
        self.compiler(_simple_breaks(action_text), cell, style="Measure List")

    def set_cell_action_requirements(self, cell, action):
        if action.get("requirements", None):
            paragraph = cell.add_paragraph(style="Measure Indent")
            run = paragraph.add_run()
            run.text = api.portal.translate(
                _("report_competences", default="Required expertise:")
            )
            run.underline = True
            run = paragraph.add_run()
            run.text = " "
            run = paragraph.add_run()
            run.text = (_simple_breaks(action["requirements"]),)

    def set_cell_action_responsible(self, cell, action):
        if action.get("responsible", None):
            paragraph = cell.add_paragraph(
                api.portal.translate(
                    _(
                        "report_responsible",
                        default="Responsible: ${responsible_name}",
                        mapping={"responsible_name": action["responsible"]},
                    )
                ),
                style="Measure Indent",
            )
            paragraph.runs[0].italic = True

    def set_cell_action_date(self, cell, action):
        if action.get("planning_end", None):
            paragraph = cell.add_paragraph(
                api.portal.translate(
                    _(
                        "report_end_date",
                        default="To be done by: ${date}",
                        mapping={"date": action["planning_end"]},
                    )
                ),
                style="Measure Indent",
            )

            paragraph.runs[0].italic = True

    def merge_module_rows(self, row_module, row_risk):
        """This merges the the first cell of the given rows, the one containing
        the module title.

        Also remove the horizontal borders between the not merged cells.
        """
        idx = 0
        first_cell = row_module.cells[idx]
        last_cell = row_risk.cells[idx]
        self.set_cell_border(last_cell)
        first_cell.merge(last_cell)
        for idx, cell in enumerate(row_risk.cells[1:]):
            self.set_cell_border(cell, settings=LEFT_RIGHT_BORDERS)

    def set_answer_font(self, answer, cell):
        """Overridden in subclasses"""

    def set_modules_rows(self, data):
        """This takes a list of modules and creates the rows for them."""
        modules = data.get("modules", [])
        table = self.get_modules_table()

        unanswered_risks = []
        not_applicable_risks = []

        for module in modules:
            risks = module["risks"]
            if not risks:
                continue
            row_module = table.add_row()
            cell = row_module.cells[0]
            cell.paragraphs[0].text = module.get("title", "")
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            self.set_row_borders(row_module)
            count = 0
            for risk in risks:
                answer = risk.get("justifiable", "")
                if not answer and risk.get("postponed", False):
                    answer = "postponed"
                # In case our report type defines this:
                # Omit risk if the user has not answered it
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
                    cell = row_risk.cells[self.risk_answer_col]
                    cell.text = self.justifiable_map.get(answer) or ""
                    self.set_answer_font(answer, cell)
                self.set_cell_actions(row_risk.cells[self.risk_measures_col], risk)

                if count:
                    self.merge_module_rows(row_module, row_risk)

            if count:
                # set borders on last risk row, but not the top
                settings = deepcopy(ALL_BORDERS)
                settings["top"] = False
                self.set_row_borders(row_risk, settings=settings)

        def _merge_cells(cells):
            """Merge all given cells into one."""
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
        # The first cell stays as it is,
        # the second cell will be merged with all following cells
        _merge_cells(row.cells[1:])

        return unanswered_risks, not_applicable_risks

    def add_extra(self, unanswered_risks, not_applicable_risks):
        pass

    def compile(self, data):
        """Compile the template using data.

        We need to compile two areas of the template:

        - the paragraph above the first table (containing the session title)
        - the first table (containing all the modules)

        data is a dict like object.
        Check the file .../daimler/oira/tests/mocked_data.py
        to understand its format
        """
        self.set_session_title_row(data)
        self.set_table_header()
        unanswered_risks, not_applicable_risks = self.set_modules_rows(data)

        # Finally clean up the modules table
        modules_table = self.get_modules_table()
        self.remove_row(modules_table.rows[1])

        # Add extra, where required
        self.add_extra(unanswered_risks, not_applicable_risks)


class DocxCompilerFrance(DocxCompilerFullTable):
    use_solution_description = False

    @property
    @memoize
    def registry_key(self):
        return "{country}.{sector}".format(
            country=self.webhelpers.country, sector=self.webhelpers.sector.id
        )

    @property
    def _base_filename(self):
        return self.template_by_sector_mapping.get(self.registry_key, "oira_fr.docx")

    @property
    def title_extra(self):
        return self.title_extra_by_sector_mapping.get(
            self.registry_key, "- Evaluation des risques professionnels"
        )


class DocxCompilerItaly(DocxCompilerFullTable):
    """WIP: Copy of the French report"""

    sections_offset = 1
    paragraphs_offset = 32

    _base_filename = "oira_it_table.docx"

    show_risk_descriptions = False
    use_measures_subheading = False
    show_priority = False
    only_anwered_risks = True
    risk_answer_col = None
    risk_measures_col = 2
    use_solution_description = False

    @property
    def session_title_lookup(self):
        lookup = {
            0: {0: {"fname": "title", "title": _("label_title", default="Title")}}
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
            run.text = " %s" % risk["title"]

        if not_applicable_risks:
            doc.add_paragraph()
            doc.add_paragraph("Adempimenti e rischi non applicabili", style="Heading 2")
            for risk in not_applicable_risks:
                print_risk(risk)

        if unanswered_risks:
            doc.add_paragraph()
            doc.add_paragraph(
                "I seguenti rischi non sono stati ancora valutati", style="Heading 2"
            )
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
        header_table.cell(0, 0).paragraphs[0].text = data["title"]
        header_table.cell(0, 1).paragraphs[0].text = formatDate(request, date.today())

        footer_txt = self.t(
            _(
                "report_identification_revision",
                default="This document was based on the OiRA Tool '${title}' "
                "of revision date ${date}.",
                mapping={
                    "title": survey.published[1],
                    "date": formatDate(request, survey.published[2]),
                },
            )
        )

        footer = self.template.sections[0].footer
        paragraph = footer.tables[0].cell(0, 0).paragraphs[0]
        paragraph.style = "Footer"
        paragraph.text = footer_txt

    def compile(self, data):
        """"""
        self.set_session_title_row(data)
        self.set_body(
            data,
            show_priority=False,
            always_print_description=True,
            skip_legal_references=False,
            skip_existing_measures=False,
            skip_planned_measures=False,
            use_solutions=True,
        )


class DocxCompilerShort(DocxCompilerFullTable):
    _base_filename = "oira_short.docx"

    justifiable_map = {"yes": "✅", "no": "❌", "postponed": "?"}
    justifiable_font = {"postponed": {"color": RGBColor(0xCC, 0xCC, 0x0), "bold": True}}

    @property
    @memoize
    def options(self):
        country = self.webhelpers.content_country_obj
        return country.compact_report_options

    @property
    def is_show_description_of_risks(self):
        return "description_of_risks" in self.options

    @property
    def is_show_comments(self):
        return "comments" in self.options

    @property
    def use_solution_description(self):
        return "description_of_measures" in self.options

    @property
    def is_show_measure_responsible_date(self):
        return "measure_responsible_date" in self.options

    @property
    def is_show_resources_legal_references(self):
        return "resources_legal_references" in self.options

    def set_table_header(self):
        table = self.get_modules_table()
        header = table.rows[0]
        header.cells[0].paragraphs[0].runs[0].text = api.portal.translate(
            _(
                "report_heading_activity",
                default="Activity",
            )
        )
        header.cells[1].paragraphs[0].runs[0].text = api.portal.translate(
            _(
                "report_heading_risk_description",
                default="Risk Description",
            )
        )
        if self.tool_type in self.tti.types_existing_measures:
            header.cells[1].paragraphs[1].runs[0].text = api.portal.translate(
                _(
                    "report_heading_measures_in_place",
                    default="Measures in Place",
                )
            )
        else:
            # workaround for paragraph deletion
            # https://github.com/python-openxml/python-docx/issues/33#issuecomment-77661907
            p = header.cells[1].paragraphs[1]._element
            p.getparent().remove(p)
            p._p = p._element = None

        header.cells[2].paragraphs[0].runs[0].text = api.portal.translate(
            _(
                "report_heading_situation",
                default="Situation",
            )
        )
        header.cells[3].paragraphs[0].runs[0].text = api.portal.translate(
            _(
                "report_heading_planned_measures",
                default="Planned Measures",
            )
        )

    def set_answer_font(self, answer, cell):
        font = self.justifiable_font.get(answer)
        if font:
            cell.paragraphs[0].runs[0].font.color.rgb = font.get("color")
            cell.paragraphs[0].runs[0].font.bold = font.get("bold", False)

    def set_cell_risk_title(self, cell, risk):
        paragraph = cell.paragraphs[0]
        paragraph.style = "Risk Bold List"
        paragraph.text = " ".join((risk["number"], risk["title"]))
        paragraph.paragraph_format.left_indent = 0
        if self.show_priority:
            self.set_cell_risk_priority(cell, risk)

    def set_cell_risk(self, cell, risk):
        """Take the risk and add the appropriate text:

        title, description, comment, measures in place, resources
        """
        self.set_cell_risk_title(cell, risk)
        if self.is_show_description_of_risks:
            self.set_cell_risk_description(cell, risk)
        self.set_cell_risk_measures(cell, risk)
        if self.is_show_comments:
            self.set_cell_risk_comment(cell, risk)
        if self.is_show_resources_legal_references:
            self.set_resources_legal_references(cell, risk)

        cell.add_paragraph(style="Risk Normal")

    def set_cell_risk_comment(self, cell, risk):
        if risk["comment"] and risk["comment"].strip():
            cell.add_paragraph()
            cell.add_paragraph(
                api.portal.translate(
                    _(
                        "report_heading_comments",
                        default="Comments:",
                    )
                ),
                style="Risk Italics",
            )
            self.compiler(risk["comment"], cell, style="Risk Italics")

    def set_resources_legal_references(self, cell, risk):
        if risk["resources"] and risk["resources"].strip():
            cell.add_paragraph()
            cell.add_paragraph(
                api.portal.translate(
                    _(
                        "report_heading_resources",
                        default="Legal and policy references:",
                    )
                ),
            )
            self.compiler(risk["resources"], cell)

    def set_cell_actions(self, cell, risk):
        """Take the risk and add the appropriate text:

        planned measures
        """
        cell.paragraphs[0]
        for idx, action in enumerate(risk["actions"]):
            if idx != 0:
                cell.add_paragraph()
            self.set_cell_action_text(cell, action)
            if self.is_show_measure_responsible_date:
                self.set_cell_action_responsible(cell, action)

    def set_cell_action_responsible(self, cell, action):
        text_responsible = ""
        if action.get("responsible", None):
            text_responsible = action["responsible"]

        if action.get("planning_end", None):
            text_date = api.portal.translate(
                _(
                    "report_end_date_short",
                    default="by ${date}",
                    mapping={"date": action["planning_end"]},
                )
            )
            text_responsible = " – ".join((text_responsible, text_date))
        if text_responsible:
            cell.add_paragraph(
                "",
                style="Measure Indent",
            )
            paragraph = cell.add_paragraph(
                text_responsible,
                style="Measure Indent",
            )
            paragraph.runs[0].italic = True

    def merge_module_rows(self, row_module, row_risk):
        """Override to not remove the horizontal borders between the unmerged cells."""
        idx = 0
        first_cell = row_module.cells[idx]
        last_cell = row_risk.cells[idx]
        self.set_cell_border(last_cell)
        first_cell.merge(last_cell)
