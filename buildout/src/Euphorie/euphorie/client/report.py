from cStringIO import StringIO
import htmllaundry
from rtfng.Elements import Document
from rtfng.Elements import StyleSheet
from rtfng.document.paragraph import Paragraph
from rtfng.document.paragraph import Cell
from rtfng.document.paragraph import Table
from rtfng.document.section import Section
from rtfng.PropertySets import TabPropertySet
from rtfng.Renderer import Renderer
from sqlalchemy import sql
from five import grok
from zope.i18n import translate
from z3c.saconfig import Session
from plonetheme.nuplone.utils import formatDate
from euphorie.client.survey import PathGhost
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client import MessageFactory as _
from euphorie.client.session import SessionManager
from euphorie.client import model


class ActionPlanReportDownload(grok.View):
    """Generate and download action report.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.name("download")

    def update(self):
        self.session=SessionManager.session



    def getNodes(self):
        """Return an orderer list of all tree items for the current survey."""
        query=Session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session==self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                                model.RISK_PRESENT_OR_TOP5_FILTER))\
                .order_by(model.SurveyTreeItem.path)
        return query.all()


    def addIntroduction(self, document):
        t=lambda txt: translate(txt, context=self.request)
        normal_style=document.StyleSheet.ParagraphStyles.Normal
        section=self.createSection(document)

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(_("plan_report_intro_header", default=u"Introduction"))))

        intro=t(_("plan_report_intro_1", default=
            u"By filling in the list of questions, you have completed a risk "
            u"assessment. This assessment is used to draw up an action plan. "
            u"The progress of this action plan must be discussed annually and "
            u"a small report must be written on the progress. Certain "
            u"subjects might have been completed and perhaps new subjects "
            u"need to be added."))
        section.append(Paragraph(normal_style, intro))

        if self.session.report_comment:
            section.append(Paragraph(normal_style, self.session.report_comment))


    def addCompanyInformation(self, document):
        company=self.session.company
        t=lambda txt: translate(txt, context=self.request)
        section=self.createSection(document)
        normal_style=document.StyleSheet.ParagraphStyles.Normal
        missing=t(_("missing_data", default=u"Not provided"))

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(_("plan_report_company_header", default=u"Company details"))))

        table=Table(TabPropertySet.DEFAULT_WIDTH*5, TabPropertySet.DEFAULT_WIDTH*15)
        country=self.request.locale.displayNames.territories.get(company.country.upper(), company.country) \
                    if company.country else missing
        table.append(
                Cell(Paragraph(normal_style, t(_("label_company_country", default=u"Country")))),
                Cell(Paragraph(normal_style, country)))
        table.append(
                Cell(Paragraph(normal_style, t(_("label_employee_numbers", default=u"Number of employees")))),
                Cell(Paragraph(normal_style, company.employees if company.employees else missing)))
        table.append(
                Cell(Paragraph(normal_style, t(_("label_referer", default=u"Through which channel did you learn about this tool?")))),
                Cell(Paragraph(normal_style, company.referer if company.referer else missing)))
        section.append(table)


    def addActionPlan(self, document):
        survey=self.request.survey
        t=lambda txt: translate(txt, context=self.request)
        section=self.createSection(document)

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(_("plan_report_plan_header", default=u"Action plan"))))

        normal_style=document.StyleSheet.ParagraphStyles.Normal
        warning_style=document.StyleSheet.ParagraphStyles.Warning
        measure_heading_style=document.StyleSheet.ParagraphStyles.MeasureHeading
        header_styles={
                0: document.StyleSheet.ParagraphStyles.Heading2,
                1:  document.StyleSheet.ParagraphStyles.Heading3,
                2:  document.StyleSheet.ParagraphStyles.Heading4,
                3:  document.StyleSheet.ParagraphStyles.Heading5,
                }

        for node in self.getNodes():
            section.append(Paragraph(header_styles[node.depth], u"%s %s" % (node.number, node.title)))

            if node.type!="risk":
                continue

            zodb_node=survey.restrictedTraverse(node.zodb_path.split("/"))
            if node.identification=="no" and not (
                    zodb_node.problem_description and zodb_node.problem_description.strip()):
                section.append(Paragraph(warning_style,
                    t(_("warn_risk_present", default=u"You responded negative to the above statement."))))
            elif node.postponed or not node.identification:
                section.append(Paragraph(warning_style,
                    t(_("risk_unanswered", default=u"This risk still needs to be inventorised."))))

            if node.priority:
                if node.priority=="low":
                    level=_("report_priority_low", default=u"low priority risk")
                elif node.priority=="medium":
                    level=_("report_priority_medium", default=u"medium priority risk")
                elif node.priority=="high":
                    level=_("report_priority_high", default=u"high priority risk")
                section.append(Paragraph(normal_style, 
                    t(_("report_priority", default=u"This is a ")), t(level)))

            section.append(Paragraph(normal_style, htmllaundry.StripMarkup(zodb_node.description)))

            for (idx, measure) in enumerate(node.action_plans):
                if len(node.action_plans)==1:
                    section.append(Paragraph(measure_heading_style,
                        t(_("header_measure_single", default=u"Measure"))))
                else:
                    section.append(Paragraph(measure_heading_style,
                        t(_("header_measure_multiple", default=u"Measure ${index}", mapping={"index": idx+1}))))
                self.addMeasure(document, section, measure)


    def addMeasure(self, document, section, measure):
        normal_style=document.StyleSheet.ParagraphStyles.Normal

        t=lambda txt: translate(txt, context=self.request)

        table=Table(TabPropertySet.DEFAULT_WIDTH*5, TabPropertySet.DEFAULT_WIDTH*15)
        if measure.action_plan:
            table.append(
                    Cell(Paragraph(normal_style, t(_("report_measure_actionplan", default=u"Action plan:")))),
                    Cell(Paragraph(normal_style, measure.action_plan)))
        if measure.prevention_plan:
            table.append(
                    Cell(Paragraph(normal_style, t(_("report_measure_preventionplan", default=u"Prevention plan:")))),
                    Cell(Paragraph(normal_style, measure.prevention_plan)))
        if measure.requirements:
            table.append(
                    Cell(Paragraph(normal_style, t(_("report_measure_requirements", default=u"Requirements:")))),
                    Cell(Paragraph(normal_style, measure.requirements)))
        if table.Rows:
            section.append(table)

        if measure.responsible and not (measure.planning_start or measure.planning_end):
            section.append(Paragraph(normal_style, 
                t(_(u"${responsible} is responsible for this task.", mapping={"responsible": measure.responsible}))))
        elif measure.responsible and measure.planning_start and not measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_(u"${responsible} is responsible for this task which starts on ${start}.",
                    mapping={"responsible": measure.responsible,
                             "start": formatDate(self.request, measure.planning_start)}))))
        elif measure.responsible and not measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_(u"${responsible} is responsible for this task which ends on ${end}.",
                    mapping={"responsible": measure.responsible,
                             "end": formatDate(self.request, measure.planning_end)}))))
        elif measure.responsible and measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_(u"${responsible} is responsible for this task which starts on ${start} and ends on ${end}.",
                    mapping={"responsible": measure.responsible,
                             "start": formatDate(self.request, measure.planning_start),
                             "end": formatDate(self.request, measure.planning_end)}))))
        elif not measure.responsible and measure.planning_start and not measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_(u"This task starts at ${start}.",
                    mapping={"start": formatDate(self.request, measure.planning_start)}))))
        elif not measure.responsible and not measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_(u"This task ends at ${end}.", mapping={"end": formatDate(self.request, measure.planning_end)}))))
        elif not measure.responsible and measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_(u"This task starts at ${start} and ends at ${end}.",
                    mapping={"start": formatDate(self.request, measure.planning_start),
                             "end": formatDate(self.request, measure.planning_end)}))))


    def createSection(self, document):
        t=lambda txt: translate(txt, context=self.request)
        footer=t(_("report_survey_revision",
            default=u"This report was based on the survey '${title}' of revision date ${date}.",
            mapping={"title": self.context.published[1],
                     "date": formatDate(self.request, self.context.published[2])}))
        # rtfng does not like unicode footers
        footer=Paragraph(document.StyleSheet.ParagraphStyles.Footer,
                "".join(["\u%s?" % str(ord(e)) for e in footer]))
        section=Section()
        section.Header.append(Paragraph(document.StyleSheet.ParagraphStyles.Normal, self.session.title))
        section.Footer.append(footer)
        section.SetBreakType(section.PAGE)
        document.Sections.append(section)
        return section


    def createDocument(self):
        from rtfng.Styles import TextStyle
        from rtfng.Styles import ParagraphStyle
        from rtfng.PropertySets import TextPropertySet
        from rtfng.PropertySets import ParagraphPropertySet
        stylesheet=StyleSheet()

        style=TextStyle(TextPropertySet(stylesheet.Fonts.Arial, 22))

        stylesheet.ParagraphStyles.append(ParagraphStyle("Normal",
            style.Copy(), ParagraphPropertySet(space_before=60, space_after=60)))

        style.textProps.italic=True
        stylesheet.ParagraphStyles.append(ParagraphStyle("Warning",
            style.Copy(), ParagraphPropertySet(space_before=50, space_after=50)))

        style.textProps.size=10
        stylesheet.ParagraphStyles.append(ParagraphStyle("Footer",
            style.Copy(), ParagraphPropertySet()))

        style.textProps.italic=False
        style.textProps.bold=True
        style.textProps.size=36
        style.textProps.underline=True
        stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 1",
            style.Copy(), ParagraphPropertySet(space_before=480, space_after=60)))
        style.textProps.underline=False
        style.textProps.size=34
        stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 2",
            style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
        style.textProps.size=32
        stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 3",
            style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
        style.textProps.size=30
        stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 4",
            style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
        style.textProps.size=28
        stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 5",
            style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))

        stylesheet.ParagraphStyles.append(ParagraphStyle("Measure Heading",
            style.Copy(), ParagraphPropertySet(space_before=60, space_after=20)))

        document=Document(stylesheet)
        document.SetTitle(self.session.title)
        return document


    def render(self):
        document=self.createDocument()
        self.addIntroduction(document)
        self.addCompanyInformation(document)
        self.addActionPlan(document)

        renderer=Renderer()
        output=StringIO()
        renderer.Write(document, output)

        filename=_("filename_report_actionplan",
                   default=u"Action plan ${title}",
                   mapping=dict(title=self.session.title))
        filename=translate(filename, context=self.request)
        self.request.response.setHeader("Content-Disposition",
                            "attachment; filename=\"%s.rtf\"" % filename.encode("utf-8"))
        self.request.response.setHeader("Content-Type", "application/rtf")
        return output.getvalue()
