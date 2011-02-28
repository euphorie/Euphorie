import logging
import random
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
from Acquisition import aq_inner
from five import grok
from zope.i18n import translate
from z3c.saconfig import Session
from zExceptions import NotFound
from plonetheme.nuplone.utils import formatDate
from euphorie.client.survey import PathGhost
from euphorie.client.interfaces import IIdentificationPhaseSkinLayer
from euphorie.client.interfaces import IReportPhaseSkinLayer
from euphorie.client import MessageFactory as _
from euphorie.client.session import SessionManager
from euphorie.client import model
from euphorie.client.company import CompanySchema
from euphorie.client.update import redirectOnSurveyUpdate

log = logging.getLogger(__name__)

grok.templatedir("templates")

def createDocument():
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

    stylesheet.ParagraphStyles.append(ParagraphStyle("Comment",
        style.Copy(), ParagraphPropertySet(space_before=100, space_after=100,
            left_indent=TabPropertySet.DEFAULT_WIDTH)))

    style.textProps.size=16
    stylesheet.ParagraphStyles.append(ParagraphStyle("Footer",
        style.Copy(), ParagraphPropertySet()))

    style.textProps.italic=False
    style.textProps.size=36
    style.textProps.underline=True
    stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 1",
        style.Copy(), ParagraphPropertySet(space_before=480, space_after=60)))
    style.textProps.underline=False
    style.textProps.size=34
    stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 2",
        style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
    style.textProps.size=30
    style.textProps.bold=True
    stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 3",
        style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
    style.textProps.size=28
    stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 4",
        style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
    style.textProps.size=26
    stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 5",
        style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))
    style.textProps.size=24
    stylesheet.ParagraphStyles.append(ParagraphStyle("Heading 6",
        style.Copy(), ParagraphPropertySet(space_before=240, space_after=60)))

    stylesheet.ParagraphStyles.append(ParagraphStyle("Measure Heading",
        style.Copy(), ParagraphPropertySet(space_before=60, space_after=20)))

    document=Document(stylesheet)
    document.SetTitle(SessionManager.session.title)
    return document


def HtmlToRtf(markup):
    text=htmllaundry.StripMarkup(markup)
    text=text.replace("&#13", "\n")
    return text


def createSection(document, survey, request):
    t=lambda txt: translate(txt, context=request)
    footer=t(_("report_survey_revision",
        default=u"This report was based on the survey '${title}' of revision date ${date}.",
        mapping={"title": survey.published[1],
                 "date": formatDate(request, survey.published[2])}))
    # rtfng does not like unicode footers
    footer=Paragraph(document.StyleSheet.ParagraphStyles.Footer,
            "".join(["\u%s?" % str(ord(e)) for e in footer]))
    section=Section()
    section.Header.append(Paragraph(
        document.StyleSheet.ParagraphStyles.Footer, SessionManager.session.title))
    section.Footer.append(footer)
    section.SetBreakType(section.PAGE)
    document.Sections.append(section)
    return section



class ReportView(grok.View):
    """Intro page for report phase.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *identifcation* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.template("report")
    grok.name("index_html")

    def update(self):
        self.session=SessionManager.session

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            self.session.report_comment=reply.get("comment")
            url="%s/report/company" % self.request.survey.absolute_url()
            self.request.response.redirect(url)
            return



class IdentificationReport(grok.View):
    """Generate identification report.

    The identification report lists all risks and modules along with their identification
    and evaluation results. It does not include action plan information.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *identifcation* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)
    grok.template("report_identification")
    grok.name("report")

    def random(self):
        return random.choice([True, False])


    def report_title(self):
        return SessionManager.session.title


    def title(self, node, zodbnode):
        if node.type!="risk" or node.identification in [u"n/a", u"yes"]:
            return node.title
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return zodbnode.problem_description
        return node.title


    def risk_status(self, node, zodbnode):
        if node.postponed or not node.identification:
            return "unanswered"
        elif node.identification in [u"n/a", u"yes"]:
            return "not-present"
        elif node.identification=="no":
            return "present"


    def show_negate_warning(self, node, zodbnode):
        """Check if the risk is present but does not have a problem description.
        In that case the user interface must show a special warning."""
        if node.type!="risk" or node.identification in [u"n/a", u"yes", None]:
            return False
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return False
        return True


    def imageUrl(self, node):
        if getattr(node, "image", None):
            return "%s/@@download/image/%s" % \
                    (node.absolute_url(), node.image.filename)


    def getZodbNode(self, treenode):
        try:
            return self.request.survey.restrictedTraverse(
                    treenode.zodb_path.split("/"))
        except KeyError:
            log.error("Caught reference in session for %s to missing node %s",
                    "/".join(self.request.survey.getPhysicalPath()),
                    treenode.zodb_path)
            return None


    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        session=Session()
        dbsession=SessionManager.session
        query=session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session==dbsession)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .order_by(model.SurveyTreeItem.path)
        self.nodes=query.all()


    def publishTraverse(self, request, name):
        """Check if the user wants to download this report by checking for a
        ``download`` URL entry. This uses a little trick: browser views
        implement `IPublishTraverse`, which allows us to catch traversal steps.
        """

        if name=="download":
            return IdentificationReportDownload(aq_inner(self.context), request)
        else:
            raise NotFound(self, name, request)



class IdentificationReportDownload(grok.View):
    """Generate identification report in RTF form.

    The identification report lists all risks and modules along with their identification
    and evaluation results. It does not include action plan information.

    This view is registered for :py:class:`PathGhost` instead of
    :py:obj:`euphorie.content.survey.ISurvey` since the
    :py:class:`SurveyPublishTraverser` generates a :py:class:`PathGhost` object for the
    *identifcation* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IIdentificationPhaseSkinLayer)

    def update(self):
        self.session=SessionManager.session


    def getNodes(self):
        """Return an orderer list of all relevant tree items for the current
        survey.
        """
        query=Session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session==self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .order_by(model.SurveyTreeItem.path)
        return query.all()


    def addIdentificationResults(self, document):
        survey=self.request.survey
        t=lambda txt: translate(txt, context=self.request)
        section=createSection(document, self.context, self.request)

        normal_style=document.StyleSheet.ParagraphStyles.Normal
        warning_style=document.StyleSheet.ParagraphStyles.Warning
        comment_style=document.StyleSheet.ParagraphStyles.Comment
        header_styles={
                0: document.StyleSheet.ParagraphStyles.Heading2,
                1:  document.StyleSheet.ParagraphStyles.Heading3,
                2:  document.StyleSheet.ParagraphStyles.Heading4,
                3:  document.StyleSheet.ParagraphStyles.Heading5,
                4:  document.StyleSheet.ParagraphStyles.Heading6,
                }

        for node in self.getNodes():
            section.append(Paragraph(header_styles[node.depth], u"%s %s" % (node.number, node.title)))

            if node.type!="risk":
                continue

            zodb_node=survey.restrictedTraverse(node.zodb_path.split("/"))
            if node.identification=="no" and not (
                    zodb_node.problem_description and zodb_node.problem_description.strip()):
                section.append(Paragraph(warning_style,
                    t(_("warn_risk_present", default=u"You responded negatively to the above statement."))))
            elif node.postponed or not node.identification:
                section.append(Paragraph(warning_style,
                    t(_("risk_unanswered", default=u"This risk still needs to be inventorised."))))

            section.append(Paragraph(normal_style, HtmlToRtf(zodb_node.description)))

            if node.comment and node.comment.strip():
                section.append(Paragraph(comment_style, node.comment))



    def render(self):
        document=createDocument()
        self.addIdentificationResults(document)

        renderer=Renderer()
        output=StringIO()
        renderer.Write(document, output)

        filename=_("filename_report_identification",
                   default=u"Identification report ${title}",
                   mapping=dict(title=self.session.title))
        filename=translate(filename, context=self.request)
        self.request.response.setHeader("Content-Disposition",
                            "attachment; filename=\"%s.rtf\"" % filename.encode("utf-8"))
        self.request.response.setHeader("Content-Type", "application/rtf")
        return output.getvalue()



class ActionPlanReportView(grok.View):
    """Generate action report.

    The action plan report lists all present risks, including their action plan
    information.

    This view is registered for :obj:`PathGhost` instead of :obj:`ISurvey`
    since the :py:class:`SurveyPublishTraverser` generates a `PathGhost` object for
    the *inventory* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.template("report_actionplan")
    grok.name("view")

    def random(self):
        return random.choice([True, False])


    def report_title(self):
        return SessionManager.session.title


    def title(self, node, zodbnode):
        if node.type!="risk" or node.identification in [u"n/a", u"yes"]:
            return node.title
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return zodbnode.problem_description
        return node.title


    def risk_status(self, node, zodbnode):
        if node.postponed or not node.identification:
            return "unanswered"
        elif node.identification in [u"n/a", u"yes"]:
            return "not-present"
        elif node.identification=="no":
            return "present"


    def show_negate_warning(self, node, zodbnode):
        if node.type!="risk" or node.identification in [u"n/a", u"yes"]:
            return False
        if zodbnode.problem_description and zodbnode.problem_description.strip():
            return False
        return True


    def imageUrl(self, node):
        if getattr(node, "image", None):
            return "%s/@@download/image/%s" % \
                    (node.absolute_url(), node.image.filename)


    def getZodbNode(self, treenode):
        return self.request.survey.restrictedTraverse(
                treenode.zodb_path.split("/"))

    def update(self):
        if redirectOnSurveyUpdate(self.request):
            return

        session=Session()
        self.session=SessionManager.session
        if self.session.company is None:
            self.session.company=model.Company()
        query=session.query(model.SurveyTreeItem)\
                .filter(model.SurveyTreeItem.session==self.session)\
                .filter(sql.not_(model.SKIPPED_PARENTS))\
                .filter(sql.or_(model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                                model.RISK_PRESENT_OR_TOP5_FILTER))\
                .order_by(model.SurveyTreeItem.path)
        self.nodes=query.all()



class ActionPlanReportDownload(grok.View):
    """Generate and download action report as a RTF file.

    The action plan report lists all present risks, including their action plan
    information.

    This view is registered for :obj:`PathGhost` instead of :obj:`ISurvey`
    since the :py:class:`SurveyPublishTraverser` generates a `PathGhost` object for
    the *inventory* component of the URL.
    """
    grok.context(PathGhost)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IReportPhaseSkinLayer)
    grok.name("download")

    def update(self):
        self.session=SessionManager.session
        if self.session.company is None:
            self.session.company=model.Company()


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
        section=createSection(document, self.context, self.request)

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
        section=createSection(document, self.context, self.request)
        normal_style=document.StyleSheet.ParagraphStyles.Normal
        missing=t(_("missing_data", default=u"Not provided"))

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(_("plan_report_company_header", default=u"Company details"))))

        table=Table(TabPropertySet.DEFAULT_WIDTH*3, TabPropertySet.DEFAULT_WIDTH*8)
        field=CompanySchema["country"]
        country=self.request.locale.displayNames.territories.get(company.country.upper(), company.country) \
                    if company.country else missing
        table.append(
                Cell(Paragraph(normal_style, t(field.title))),
                Cell(Paragraph(normal_style, country)))
        field=CompanySchema["employees"]
        table.append(
                Cell(Paragraph(normal_style, t(field.title))),
                Cell(Paragraph(normal_style, t(field.vocabulary.getTerm(company.employees).title) if company.employees else missing)))
        field=CompanySchema["conductor"]
        table.append(
                Cell(Paragraph(normal_style, t(field.title))),
                Cell(Paragraph(normal_style, t(field.vocabulary.getTerm(company.conductor).title) if company.conductor else missing)))
        field=CompanySchema["referer"]
        table.append(
                Cell(Paragraph(normal_style, t(field.title))),
                Cell(Paragraph(normal_style, t(field.vocabulary.getTerm(company.referer).title) if company.referer else missing)))
        section.append(table)


    def addActionPlan(self, document):
        survey=self.request.survey
        t=lambda txt: translate(txt, context=self.request)
        section=createSection(document, self.context, self.request)

        section.append(Paragraph(
            document.StyleSheet.ParagraphStyles.Heading1,
            t(_("plan_report_plan_header", default=u"Action plan"))))

        normal_style=document.StyleSheet.ParagraphStyles.Normal
        comment_style=document.StyleSheet.ParagraphStyles.Comment
        warning_style=document.StyleSheet.ParagraphStyles.Warning
        measure_heading_style=document.StyleSheet.ParagraphStyles.MeasureHeading
        header_styles={
                0: document.StyleSheet.ParagraphStyles.Heading2,
                1:  document.StyleSheet.ParagraphStyles.Heading3,
                2:  document.StyleSheet.ParagraphStyles.Heading4,
                3:  document.StyleSheet.ParagraphStyles.Heading5,
                4:  document.StyleSheet.ParagraphStyles.Heading6,
                }

        for node in self.getNodes():
            section.append(Paragraph(header_styles[node.depth], u"%s %s" % (node.number, node.title)))

            if node.type!="risk":
                continue

            zodb_node=survey.restrictedTraverse(node.zodb_path.split("/"))
            if node.identification=="no" and not (
                    zodb_node.problem_description and zodb_node.problem_description.strip()):
                section.append(Paragraph(warning_style,
                    t(_("warn_risk_present", default=u"You responded negatively to the above statement."))))
            elif node.postponed or not node.identification:
                section.append(Paragraph(warning_style,
                    t(_("risk_unanswered", default=u"This risk still needs to be inventorised."))))
            elif node.identification in [u"n/a", u"yes"] and node.risk_type=="top5":
                section.append(Paragraph(warning_style,
                    t(_("top5_risk_not_present", 
                        default=u"This risk is not present in your "
                                u"organisation, but since the sector "
                                u"organisation considers this one of "
                                u"the top 5 most critical risks it "
                                u"must be included in this report."))))

            if node.priority:
                if node.priority=="low":
                    level=_("report_priority_low", default=u"low priority risk")
                elif node.priority=="medium":
                    level=_("report_priority_medium", default=u"medium priority risk")
                elif node.priority=="high":
                    level=_("report_priority_high", default=u"high priority risk")
                section.append(Paragraph(normal_style, 
                    t(_("report_priority", default=u"This is a ")), t(level)))

            section.append(Paragraph(normal_style, HtmlToRtf(zodb_node.description)))
            if node.comment and node.comment.strip():
                section.append(Paragraph(comment_style, node.comment))

            for (idx, measure) in enumerate(node.action_plans):
                if len(node.action_plans)==1:
                    section.append(Paragraph(measure_heading_style,
                        t(_("header_measure_single", default=u"Measure"))))
                else:
                    section.append(Paragraph(measure_heading_style,
                        t(_("header_measure", default=u"Measure ${index}", mapping={"index": idx+1}))))
                self.addMeasure(document, section, measure)


    def addMeasure(self, document, section, measure):
        normal_style=document.StyleSheet.ParagraphStyles.Normal

        t=lambda txt: translate(txt, context=self.request)

        table=Table(TabPropertySet.DEFAULT_WIDTH*5, TabPropertySet.DEFAULT_WIDTH*8)
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
                t(_("report_measure_responsible", default=u"${responsible} is responsible for this task.",
                    mapping={"responsible": measure.responsible}))))
        elif measure.responsible and measure.planning_start and not measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_("report_measure_responsible_and_start",
                    default=u"${responsible} is responsible for this task which starts on ${start}.",
                    mapping={"responsible": measure.responsible,
                             "start": formatDate(self.request, measure.planning_start)}))))
        elif measure.responsible and not measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_("report_measure_responsible_and_end",
                    default=u"${responsible} is responsible for this task which ends on ${end}.",
                    mapping={"responsible": measure.responsible,
                             "end": formatDate(self.request, measure.planning_end)}))))
        elif measure.responsible and measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_("report_measure_full",
                    default=u"${responsible} is responsible for this task which starts on ${start} and ends on ${end}.",
                    mapping={"responsible": measure.responsible,
                             "start": formatDate(self.request, measure.planning_start),
                             "end": formatDate(self.request, measure.planning_end)}))))
        elif not measure.responsible and measure.planning_start and not measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_("report_measure_start_only",
                    default=u"This task starts on ${start}.",
                    mapping={"start": formatDate(self.request, measure.planning_start)}))))
        elif not measure.responsible and not measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_("report_measure_end_only",
                    default=u"This task ends on ${end}.",
                    mapping={"end": formatDate(self.request, measure.planning_end)}))))
        elif not measure.responsible and measure.planning_start and measure.planning_end:
            section.append(Paragraph(normal_style, 
                t(_("report_measure_start_and_stop",
                    default=u"This task starts on ${start} and ends on ${end}.",
                    mapping={"start": formatDate(self.request, measure.planning_start),
                             "end": formatDate(self.request, measure.planning_end)}))))
        if measure.budget:
            section.append(Paragraph(normal_style,
                t(_("report_measure_budget",
                    default=u"There is a budget of ${amount} for this measure.",
                    mapping={"amount": measure.budget}))))


    def render(self):
        document=createDocument()
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

