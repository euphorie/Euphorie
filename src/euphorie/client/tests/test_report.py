import unittest
from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.content.risk import Risk
from euphorie.client import model


class ShowNegateWarningTests(unittest.TestCase):
    def _call(self, node, zodbnode):
        from euphorie.client.report import IdentificationReport
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
        from euphorie.client.report import HtmlToRtf
        return HtmlToRtf(*a, **kw)

    def render(self, output):
        from cStringIO import StringIO
        from rtfng.Elements import Document
        from rtfng.document.section import Section
        from rtfng.Renderer import Renderer
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
                self.render(self.HtmlToRtf(u"<p>text</p>", u"<stylesheet>")))

    def testBasicParagraph(self):
        self.assertTrue(
                "Simple text\\par" in
                self.render(self.HtmlToRtf(u"<p>Simple text</p>",
                                           u"<stylesheet>")), [])

    def testItalicInText(self):
        self.assertTrue(
                "Simple {\\i text}\\par" in
                self.render(self.HtmlToRtf(u"<p>Simple <em>text</em></p>",
                                           u"<stylesheet>")))

    def testBoldAndItalicText(self):
        self.assertTrue(
                "Very {\\i very }{\\b\\i bold}\\par" in
                self.render(self.HtmlToRtf(
                    u"<p>Very <em>very <strong>bold</strong></em></p>",
                    u"<stylesheet>")))

    def testInlineEntity(self):
        self.assertTrue(
                "Simple & clean\\par" in
                self.render(self.HtmlToRtf(
                    u"<p>Simple &amp; clean</p>",
                    u"<stylesheet>")))

    def testInlineEntityDigit(self):
        self.assertTrue(
                "Simple \r clean\\par" in
                self.render(self.HtmlToRtf(u"<p>Simple &#13; clean</p>",
                                           u"<stylesheet>")))

    def test_link_in_text(self):
        # This demonstrates TNO Euphorie ticket 186
        html = '<p>Check the <a rel="nofollow">manual</a> for more info.</p>'
        rendering = self.render(self.HtmlToRtf(html, '<stylesheet>'))
        self.assertTrue('Check the manual for more info.' in rendering)
        self.assertEqual(rendering.count('more info'), 1)


class ActionPlanTimelineTests(EuphorieTestCase):
    def ActionPlanTimeline(self, *a, **kw):
        from euphorie.client.report import ActionPlanTimeline
        return ActionPlanTimeline(*a, **kw)

    def _create_session(self, dbsession, loginname='jane'):
        from euphorie.client.model import Account
        from euphorie.client.model import SurveySession
        session = SurveySession(
                account=Account(loginname=loginname, password=u'john'),
                zodb_path='survey')
        dbsession.add(session)
        return session

    def _convert_xls(self, book):
        from cStringIO import StringIO
        import xlrd
        output = StringIO()
        book.save(output)
        readable_book = xlrd.open_workbook(
                file_contents=output.getvalue(),
                on_demand=True)
        return readable_book

    def test_get_measures_return_risks_without_measures(self):
        from z3c.saconfig import Session
        from euphorie.client.model import Risk
        dbsession = Session()
        session = self._create_session(dbsession)
        session.addChild(Risk(session=session,
                              zodb_path='1',
                              risk_id='1', 
                              identification='no'))
        view = self.ActionPlanTimeline(None, None)
        view.session = session
        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][1], None)

    def test_get_measures_filter_on_session(self):
        from z3c.saconfig import Session
        from euphorie.client.model import Risk
        from euphorie.client.model import ActionPlan
        dbsession = Session()
        sessions = []
        for login in ['jane', 'john']:
            session = self._create_session(dbsession, loginname=login)
            session.addChild(Risk(session=session,
                                  zodb_path='1',
                                  risk_id='1', 
                                  identification='no',
                                  action_plans=[
                                      ActionPlan(action_plan=u'Measure 1')]))
            sessions.append(session)
        view = self.ActionPlanTimeline(None, None)
        view.session = sessions[0]
        measures = view.get_measures()
        self.assertEqual(len(measures), 1)

    def test_get_measures_order_by_start_date(self):
        import datetime
        from z3c.saconfig import Session
        from euphorie.client.model import Risk
        from euphorie.client.model import ActionPlan
        dbsession = Session()
        session = self._create_session(dbsession)
        session.addChild(Risk(
            session=session,
            zodb_path='1',
            risk_id='1', 
            identification='no',
            action_plans=[
                ActionPlan(action_plan=u'Plan 2',
                           planning_start=datetime.date(2011, 12, 15)),
                ActionPlan(action_plan=u'Plan 1',
                           planning_start=datetime.date(2011, 11, 15))]))
        view = self.ActionPlanTimeline(None, None)
        view.session = session
        measures = view.get_measures()
        self.assertEqual(len(measures), 2)
        self.assertEqual(
                [row[1].action_plan for row in measures],
                [u'Plan 1', u'Plan 2'])

    def test_create_workbook_empty_session(self):
        # If there are no risks only the header row should be generated.
        view = self.ActionPlanTimeline(None, None)
        view.get_measures = lambda: []
        book = view.create_workbook()
        self.assertRaises(IndexError, book.get_sheet, 1)
        sheet = book.get_sheet(0)
        self.assertEqual(len(sheet.rows), 1)

    def test_create_workbook_plan_information(self):
        import datetime
        import xlrd
        from euphorie.client.model import Risk
        from euphorie.client.model import ActionPlan
        risk = Risk(zodb_path='1', risk_id='1', identification='no')
        plan = ActionPlan(action_plan=u'Plan 2',
                           planning_start=datetime.date(2011, 12, 15),
                           budget=500)
        view = self.ActionPlanTimeline(None, None)
        view.get_measures = lambda: [(risk, plan)]
        book = view.create_workbook()
        book = self._convert_xls(book)
        row = book.get_sheet(0).row(1)
        # planning start
# XXX xlwt turns dates into numbers?
        #self.assertEqual(row[0].ctype, xlrd.XL_CELL_DATE)
        # planning end
        self.assertEqual(row[1].ctype, xlrd.XL_CELL_EMPTY)
        # action plan
        self.assertEqual(row[2].ctype, xlrd.XL_CELL_TEXT)
        self.assertEqual(row[2].value, u'Plan 2')
        # prevention plan
        self.assertEqual(row[3].ctype, xlrd.XL_CELL_EMPTY)
        # requirements
        self.assertEqual(row[4].ctype, xlrd.XL_CELL_EMPTY)
        # responsible
        self.assertEqual(row[4].ctype, xlrd.XL_CELL_EMPTY)
        # budget
        self.assertEqual(row[6].ctype, xlrd.XL_CELL_NUMBER)
        self.assertEqual(row[6].value, 500)

    def test_render_value(self):
        from euphorie.client.tests.utils import testRequest
        from euphorie.client.model import SurveySession
        request = testRequest()
        view = self.ActionPlanTimeline(None, request)
        view.session = SurveySession(title=u'Acme')
        view.get_measures = lambda: []
        view.render()
        response = request.response
        self.assertEqual(
                response.headers['content-type'],
                'application/vnd.ms-excel')
        self.assertEqual(
                response.headers['content-disposition'],
                'attachment; filename="Timeline for Acme.xls"')
