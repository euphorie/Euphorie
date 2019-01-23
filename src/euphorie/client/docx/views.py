# coding=utf-8
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.docx.compiler import DocxCompiler
from euphorie.client.docx.compiler import DocxCompilerFrance
from euphorie.client.docx.compiler import DocxCompilerItaly
from euphorie.client.docx.compiler import IdentificationReportCompiler
from euphorie.client.interfaces import IFranceReportPhaseSkinLayer
from euphorie.client.interfaces import IItalyReportPhaseSkinLayer
from euphorie.client.session import SessionManager
from euphorie.content import MessageFactory as _
from euphorie.content.survey import get_tool_type
from plone.memoize.view import memoize
from Products.Five import BrowserView
from sqlalchemy import sql
from StringIO import StringIO
from urllib import quote
from z3c.saconfig import Session
from zope.i18n import translate


class OfficeDocumentView(BrowserView):
    ''' Base view that generates an office document and returns it
    '''
    _compiler = None
    _content_type = ''

    @property
    @memoize
    def session(self):
        ''' Return the session for this context/request
        '''
        return SessionManager.session

    def get_data(self, for_download=False):
        ''' Return the data for the compiler
        '''
        return {}

    def get_payload(self):
        ''' Compile the template and return the file as a string
        '''
        output = StringIO()
        compiler = self._compiler(self.context, self.request)
        compiler.compile(self.get_data(for_download=True))
        compiler.template.save(output)
        output.seek(0)
        return output.read()

    def t(self, txt):
        return translate(txt, context=self.request)

    def get_session_nodes(self):
        """ Return an ordered list of all relevant tree items for the current
            survey.
        """
        query = Session.query(model.SurveyTreeItem).filter(
            model.SurveyTreeItem.session == self.session).filter(
            sql.not_(model.SKIPPED_PARENTS)).filter(
                sql.or_(
                    model.MODULE_WITH_RISK_OR_TOP5_FILTER,
                    model.RISK_PRESENT_OR_TOP5_FILTER
                )
        ).order_by(model.SurveyTreeItem.path)

        return query.all()

    def __call__(self):
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename*=UTF-8\'\'{}'.format(
                quote(self._filename)
            ),
        )
        self.request.response.setHeader(
            "Content-Type",
            self._content_type,
        )
        return self.get_payload()


def _escape_text(txt):
    return txt and txt.replace('<', '&lt;') or ''


def _get_action_plan(action):
    action_plan = {}
    action_plan['text'] = _escape_text(action.action_plan)
    if action.responsible:
        action_plan['responsible'] = _escape_text(action.responsible)
    if action.planning_start:
        action_plan['planning_start'] = action.planning_start.strftime(
            "%d.%m.%Y")
    return action_plan


class ActionPlanDocxView(OfficeDocumentView):
    ''' Generate a report based on a basic docx template
    '''

    _compiler = DocxCompiler
    _content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # noqa: E 501

    def __init__(self, context, request):
        super(ActionPlanDocxView, self).__init__(context, request)
        if IItalyReportPhaseSkinLayer.providedBy(request):
            self._compiler = DocxCompilerItaly
        elif IFranceReportPhaseSkinLayer.providedBy(request):
            if get_tool_type(context) == 'existing_measures':
                self._compiler = DocxCompilerFrance

    def get_heading(self, title):
        heading = self.t(
            _(
                "header_oira_report_download",
                default=u"OiRA Report: “${title}”",
                mapping=dict(title=title)
            ),
        )
        return heading

    def get_section_headings(self):
        headings = [
            self.t(_(
                "header_present_risks",
                default=u"Risks that have been identified, "
                u"evaluated and have an Action Plan")),
            self.t(_(
                "header_unevaluated_risks",
                default=u"Risks that have been identified but "
                u"do NOT have an Action Plan")),
            self.t(_(
                "header_unanswered_risks",
                default=u'Hazards/problems that have been "parked" '
                u'and are still to be dealt with')),
            self.t(_(
                "header_risks_not_present",
                default=u"Hazards/problems that have been managed "
                u"or are not present in your organisation"))
        ]
        return headings

    def get_sorted_nodes(self):
        nodes = self.get_session_nodes()
        session = SessionManager.session

        actioned_nodes = utils.get_actioned_nodes(nodes)
        unactioned_nodes = utils.get_unactioned_nodes(nodes)
        unanswered_nodes = utils.get_unanswered_nodes(session)
        risk_not_present_nodes = utils.get_risk_not_present_nodes(session)
        # From the non-present risks, filter out risks from the (un-)/actioned
        # categories. A "priority" risk will always appear in the action plan,
        # even if it has been answered with "Yes"
        risk_not_present_nodes = [
            n for n in risk_not_present_nodes if
            n not in actioned_nodes and n not in unactioned_nodes
        ]
        nodes = [
            actioned_nodes,
            unactioned_nodes,
            unanswered_nodes,
            risk_not_present_nodes,
        ]
        return nodes

    def get_data(self, for_download=False):
        ''' Gets the data structure in a format suitable for `DocxCompiler`
        '''

        data = {
            'title': self.session.title,
            'heading': self.get_heading(self.session.title),
            'section_headings': self.get_section_headings(),
            'nodes': self.get_sorted_nodes(),
            'survey_title': self.request.survey.title,
        }

        return data

    @property
    def _filename(self):
        ''' Return the document filename
        '''
        filename = _(
            "filename_report_actionplan",
            default=u"Action plan ${title}",
            mapping={'title': self.session.title}
        )
        filename = translate(filename, context=self.request)
        return filename.encode('utf8') + '.docx'


class IdentificationReportDocxView(OfficeDocumentView):
    ''' Generate a report based on a basic docx template
    '''

    _compiler = IdentificationReportCompiler
    _content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # noqa: E 501

    def get_session_nodes(self):
        """ Return an ordered list of all relevant tree items for the current
            survey.
        """
        query = Session.query(model.SurveyTreeItem).filter(
            model.SurveyTreeItem.session == self.session).filter(
                sql.not_(model.SKIPPED_PARENTS)
            ).order_by(model.SurveyTreeItem.path)

        return query.all()

    def get_data(self, for_download=False):
        ''' Gets the data structure in a format suitable for `DocxCompiler`
        '''

        data = {
            'title': self.session.title,
            'heading': '',
            'section_headings': [self.session.title],
            'nodes': [self.get_session_nodes()],
        }
        return data

    @property
    def _filename(self):
        ''' Return the document filename
        '''
        filename = _(
            "filename_report_identification",
            default=u"Identification report ${title}",
            mapping=dict(title=self.session.title))
        filename = translate(filename, context=self.request)
        return filename.encode('utf8') + '.docx'
