# coding=utf-8
from cStringIO import StringIO
from euphorie.client import model
from euphorie.client.model import Account
from euphorie.client.model import SurveySession
from euphorie.client.report import ActionPlanTimeline
from euphorie.client.report import HtmlToRtf
from euphorie.client.report import IdentificationReport
from euphorie.client.tests.utils import testRequest
from euphorie.client.utils import setRequest
from euphorie.content.risk import Risk
from euphorie.testing import EuphorieIntegrationTestCase
from rtfng.document.section import Section
from rtfng.Elements import Document
from rtfng.Renderer import Renderer
from z3c.saconfig import Session

import datetime
import mock
import unittest


class IdentificationReportTests(unittest.TestCase):

    def IdentificationReport(self, *a, **kw):
        return IdentificationReport(*a, **kw)

    def test_title_not_a_risk(self):
        node = mock.Mock()
        node.type = 'module'
        node.title = u'My title'
        view = self.IdentificationReport(None, None)
        self.assertEqual(view.title(node, None), u'My title')

    def test_title_unanswered_risk(self):
        node = mock.Mock()
        node.type = 'risk'
        node.identification = None
        node.title = u'My title'
        view = self.IdentificationReport(None, None)
        self.assertEqual(view.title(node, None), u'My title')

    def test_title_empty_problem_description(self):
        node = mock.Mock()
        node.type = 'risk'
        node.identification = u'no'
        node.title = u'My title'
        zodb_node = mock.Mock()
        zodb_node.problem_description = u'   '
        view = self.IdentificationReport(None, None)
        self.assertEqual(view.title(node, zodb_node), u'My title')

    def test_title_risk_present_and_with_problem_description(self):
        node = mock.Mock()
        node.type = 'risk'
        node.identification = u'no'
        node.title = u'My title'
        zodb_node = mock.Mock()
        zodb_node.problem_description = u'Bad situation'
        view = self.IdentificationReport(None, None)
        self.assertEqual(view.title(node, zodb_node), u'Bad situation')


class ShowNegateWarningTests(unittest.TestCase):

    def _call(self, node, zodbnode):
        report = IdentificationReport(None, None)
        return report.show_negate_warning(node, zodbnode)

    def test_show_Unanswered(self):
        # https//code.simplon.biz/tracker/tno-euphorie/ticket/75
        zodbnode = Risk()
        zodbnode.problem_description = None
        node = model.Risk(type="risk")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_RiskNotPresent(self):
        zodbnode = Risk()
        zodbnode.problem_description = None
        node = model.Risk(type="risk", identification="yes")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_RiskNotApplicable(self):
        zodbnode = Risk()
        zodbnode.problem_description = None
        node = model.Risk(type="risk", identification="n/a")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_Present(self):
        zodbnode = Risk()
        zodbnode.problem_description = None
        node = model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), True)

    def test_HasProblemDescription(self):
        zodbnode = Risk()
        zodbnode.problem_description = u"Negative"
        node = model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_HasEmptyProblemDescription(self):
        zodbnode = Risk()
        zodbnode.problem_description = u"   "
        node = model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), True)


class HtmlToRtfTests(unittest.TestCase):

    def HtmlToRtf(self, *a, **kw):
        return HtmlToRtf(*a, **kw)

    def render(self, output):
        document = Document()
        section = Section()
        for o in output:
            section.append(o)
        document.Sections.append(section)
        renderer = Renderer()
        renderer.Write(document, StringIO())  # Setup instance variables
        renderer._doc = document
        renderer._fout = StringIO()
        renderer._CurrentStyle = ""
        renderer._WriteSection(section, True, False)
        return renderer._fout.getvalue()

    def testEmptyInput(self):
        self.assertEqual(self.HtmlToRtf(u"", u"<stylesheet>"), [])

    def testInvalidHtmlFallback(self):
        self.assertTrue(
            "text\\par" in
            self.render(self.HtmlToRtf(u"<p>text</p>", u"<stylesheet>"))
        )

    def testBasicParagraph(self):
        self.assertTrue(
            "Simple text\\par" in self.render(
                self.HtmlToRtf(u"<p>Simple text</p>", u"<stylesheet>")
            ), []
        )

    def testItalicInText(self):
        self.assertTrue(
            "Simple {\\i text}\\par" in self.render(
                self.
                HtmlToRtf(u"<p>Simple <em>text</em></p>", u"<stylesheet>")
            )
        )

    def testBoldAndItalicText(self):
        self.assertTrue(
            "Very {\\i very }{\\b\\i bold}\\par" in self.render(
                self.HtmlToRtf(
                    u"<p>Very <em>very <strong>bold</strong></em></p>",
                    u"<stylesheet>"
                )
            )
        )

    def testEmphasisInText(self):
        self.assertTrue(
            "{\\i text}" in
            self.render(self.HtmlToRtf(u"<em>text</em>", u"<stylesheet>"))
        )

    def testInlineEntity(self):
        self.assertTrue(
            "Simple & clean\\par" in self.render(
                self.HtmlToRtf(u"<p>Simple &amp; clean</p>", u"<stylesheet>")
            )
        )

    def testInlineEntityDigit(self):
        self.assertTrue(
            "Simple \r clean\\par" in self.render(
                self.HtmlToRtf(u"<p>Simple &#13; clean</p>", u"<stylesheet>")
            )
        )

    def test_link_in_text(self):
        # This demonstrates TNO Euphorie ticket 186
        html = '<p>Check the <a rel="nofollow">manual</a> for more info.</p>'
        rendering = self.render(self.HtmlToRtf(html, '<stylesheet>'))
        self.assertTrue('Check the manual for more info.' in rendering)
        self.assertEqual(rendering.count('more info'), 1)


class ActionPlanTimelineTests(EuphorieIntegrationTestCase):

    def ActionPlanTimeline(self, *a, **kw):
        return ActionPlanTimeline(*a, **kw)

    def _create_session(self, dbsession, loginname='jane'):
        session = SurveySession(
            account=Account(loginname=loginname, password=u'john'),
            zodb_path='survey'
        )
        dbsession.add(session)
        return session

    def test_get_measures_with_correct_module(self):
        dbsession = Session()
        session = self._create_session(dbsession)
        # This first module should be ignored, it doesn't contain any risks
        session.addChild(model.Module(
            zodb_path='1',
            module_id='1',
        ))
        # Between the next two modules, the first one (root-level) must be
        # returned.
        module = session.addChild(
            model.Module(
                zodb_path='2',
                module_id='2',
            )
        )
        module = module.addChild(
            model.Module(
                zodb_path='2/3',
                module_id='3',
            )
        )
        module.addChild(
            model.Risk(
                zodb_path='2/3/4',
                risk_id='1',
                identification='no'
            )
        )
        request = testRequest()
        request.survey = mock.Mock()
        request.survey.restrictedTraverse = lambda x: object
        request.survey.ProfileQuestions = lambda: []
        view = self.ActionPlanTimeline(None, request)
        view.session = session
        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][0].module_id, u'2')

    def test_get_measures_return_risks_without_measures(self):
        dbsession = Session()
        session = self._create_session(dbsession)
        module = session.addChild(
            model.Module(
                session=session,
                zodb_path='1',
                module_id='1',
            )
        )
        module.addChild(
            model.Risk(
                session=session,
                zodb_path='1/2',
                risk_id='1',
                identification='no'
            )
        )
        request = testRequest()
        request.survey = mock.Mock()
        request.survey.restrictedTraverse = lambda x: object
        request.survey.ProfileQuestions = lambda: []
        setRequest(request)
        view = self.ActionPlanTimeline(None, request)
        view.session = session
        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][2], None)

    def test_get_measures_filter_on_session(self):
        dbsession = Session()
        sessions = []
        for login in ['jane', 'john']:
            session = self._create_session(dbsession, loginname=login)
            module = session.addChild(
                model.Module(
                    session=session,
                    zodb_path='1',
                    module_id='1',
                )
            )
            module.addChild(
                model.Risk(
                    session=session,
                    zodb_path='1/2',
                    risk_id='1',
                    identification='no',
                    action_plans=[
                        model.ActionPlan(
                            action_plan=u'Measure 1 for %s' % login)
                    ]))
            sessions.append(session)

        request = testRequest()
        request.survey = mock.Mock()
        request.survey.restrictedTraverse = lambda x: object
        request.survey.ProfileQuestions = lambda: []
        setRequest(request)
        view = self.ActionPlanTimeline(None, request)
        view.session = sessions[0]
        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][2].action_plan, 'Measure 1 for jane')

    def test_get_measures_order_by_start_date(self):
        dbsession = Session()
        session = self._create_session(dbsession)
        module = session.addChild(
            model.Module(
                session=session,
                zodb_path='1',
                module_id='1',
            )
        )
        module.addChild(
            model.Risk(
                session=session,
                zodb_path='1/2',
                risk_id='1',
                identification='no',
                action_plans=[
                    model.ActionPlan(
                        action_plan=u'Plan 2',
                        planning_start=datetime.date(2011, 12, 15)
                    ),
                    model.ActionPlan(
                        action_plan=u'Plan 1',
                        planning_start=datetime.date(2011, 11, 15)
                    )
                ]
            )
        )

        request = testRequest()
        request.survey = mock.Mock()
        request.survey.restrictedTraverse = lambda x: object
        request.survey.ProfileQuestions = lambda: []
        setRequest(request)
        view = self.ActionPlanTimeline(None, request)
        view.session = session
        measures = view.get_measures()
        self.assertEqual(len(measures), 2)
        self.assertEqual([row[2].action_plan for row in measures],
                         [u'Plan 1', u'Plan 2'])

    def test_priority_name_known_priority(self):
        view = self.ActionPlanTimeline(None, None)
        self.assertEqual(view.priority_name('high'), u'High')

    def test_priority_name_known_unpriority(self):
        view = self.ActionPlanTimeline(None, None)
        self.assertEqual(view.priority_name('dummy'), 'dummy')

    def test_create_workbook_empty_session(self):
        # If there are no risks only the header row should be generated.
        request = testRequest()
        request.survey = None
        setRequest(request)
        view = self.ActionPlanTimeline(None, request)
        view.getModulePaths = lambda: []
        book = view.create_workbook()
        self.assertEqual(len(book.worksheets), 1)
        sheet = book.worksheets[0]
        self.assertEqual(len(sheet.rows), 1)

    def test_create_workbook_plan_information(self):
        dbsession = Session()
        session = self._create_session(dbsession)
        module = model.Module(
            zodb_path='1',
            title=u'Top-level Module title',
        )
        risk = model.Risk(
            zodb_path='1/2/3',
            risk_id='1',
            title=u'Risk title',
            priority='high',
            identification='no',
            path='001002003',
            comment=u'Risk comment'
        )
        plan = model.ActionPlan(
            action_plan=u'Plan 2',
            planning_start=datetime.date(2011, 12, 15),
            budget=500
        )
        request = testRequest()
        request.survey = mock.Mock()
        zodb_node = mock.Mock()
        zodb_node.problem_description = u'This is wrong.'
        request.survey.restrictedTraverse.return_value = zodb_node
        view = self.ActionPlanTimeline(None, request)
        view.session = session
        view.get_measures = lambda: [(module, risk, plan)]
        wb = view.create_workbook()
        sheet = wb.worksheets[0]
        # planning start
        self.assertEqual(
            sheet.cell('A2').value.date(), datetime.date(2011, 12, 15)
        )
        # planning end
        self.assertEqual(sheet.cell('B2').value, None)
        # action plan
        self.assertEqual(sheet.cell('C2').value, u'Plan 2')
        # prevention plan
        self.assertEqual(sheet.cell('D2').value, None)
        # requirements
        self.assertEqual(sheet.cell('E2').value, None)
        # responsible
        self.assertEqual(sheet.cell('F2').value, None)
        # budget
        self.assertEqual(sheet.cell('G2').value, 500)
        # module title
        self.assertEqual(sheet.cell('H2').value, u'Top-level Module title')
        # risk number
        self.assertEqual(sheet.cell('I2').value, u'1.2.3')
        # risk title
        self.assertEqual(sheet.cell('J2').value, u'This is wrong.')
        # risk priority
        self.assertEqual(sheet.cell('K2').value, u'High')
        # risk comment
        self.assertEqual(sheet.cell('L2').value, u'Risk comment')

    def test_create_workbook_no_problem_description(self):
        dbsession = Session()
        session = self._create_session(dbsession)
        module = model.Module(
            zodb_path='1',
            path='001',
            title=u'Top-level Module title',
        )
        risk = model.Risk(
            zodb_path='1/2/3',
            risk_id='1',
            title=u'Risk title',
            priority='high',
            identification='no',
            path='001002003',
            comment=u'Risk comment')
        request = testRequest()
        request.survey = mock.Mock()
        request.survey.ProfileQuestions = lambda: []
        zodb_node = mock.Mock()
        zodb_node.title = u'Risk title.'
        zodb_node.problem_description = u'  '
        request.survey.restrictedTraverse.return_value = zodb_node
        setRequest(request)
        view = self.ActionPlanTimeline(None, request)
        view.session = session
        view.getRisks = lambda x: [(module, risk)]
        sheet = view.create_workbook().worksheets[0]
        self.assertEqual(sheet.cell('J2').value, u'Risk title')

    def test_render_value(self):
        request = testRequest()
        request.survey = None
        view = self.ActionPlanTimeline(None, request)
        view.session = SurveySession(title=u'Acme')
        view.render()
        response = request.response
        self.assertEqual(
            response.headers['content-type'], 'application/vnd.openxmlformats-'
            'officedocument.spreadsheetml.sheet'
        )
        self.assertEqual(
            response.headers['content-disposition'],
            'attachment; filename="Timeline for Acme.xlsx"'
        )
