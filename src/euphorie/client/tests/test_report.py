# coding=utf-8
# from cStringIO import StringIO
# from euphorie.client.report import HtmlToRtf
# from euphorie.client.report import IdentificationReport
# from euphorie.content.risk import Risk
from euphorie.client import model
from euphorie.client.adapters.session_traversal import TraversedSurveySession
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import SurveySession
from euphorie.client.tests.utils import addAccount
from euphorie.testing import EuphorieIntegrationTestCase
from ExtensionClass import Base
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from six.moves.urllib.parse import quote
from z3c.saconfig import Session
from zope.interface import alsoProvides

import datetime


try:
    from unittest import mock
except ImportError:
    import mock


# import unittest


class ReportIntegrationTests(EuphorieIntegrationTestCase):
    def create_session(self):
        with api.env.adopt_user(SITE_OWNER_NAME):
            api.content.create(
                container=self.portal.sectors, type="euphorie.country", id="eu"
            )
            client_country = api.content.create(
                container=self.portal.client, type="euphorie.clientcountry", id="eu"
            )
            client_sector = api.content.create(
                container=client_country, type="euphorie.clientsector", id="sector"
            )
            api.content.create(
                container=client_sector, type="euphorie.survey", id="survey"
            )

        sqlsession = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        sqlsession.add(account)
        session = model.SurveySession(
            title=u"Session", zodb_path="eu/sector/survey", account=account
        )
        sqlsession.add(session)
        sqlsession.flush()

        return session

    def test_default_reports(self):
        self.create_session()
        traversed_session = self.portal.client.eu.sector.survey.restrictedTraverse(
            "++session++1"
        )

        with self._get_view("report_view", traversed_session) as view:
            # default default sections
            self.assertEqual(
                view.default_reports,
                ["report_full", "report_action_plan", "report_overview_risks"],
            )

        # customized default sections
        view.webhelpers.content_country_obj.default_reports = [
            "report_overview_measures",
        ]
        with self._get_view("report_view", traversed_session) as view:
            self.assertEqual(
                view.default_reports,
                ["report_overview_measures"],
            )


# XXX Change these tests to test client.docx.views.IdentificationReportDocxView instead

# class IdentificationReportTests(unittest.TestCase):

#     def IdentificationReport(self, *a, **kw):
#         return IdentificationReport(*a, **kw)

#     def test_title_not_a_risk(self):
#         node = mock.Mock()
#         node.type = 'module'
#         node.title = u'My title'
#         view = self.IdentificationReport(None, None)
#         self.assertEqual(view.title(node, None), u'My title')

#     def test_title_unanswered_risk(self):
#         node = mock.Mock()
#         node.type = 'risk'
#         node.identification = None
#         node.title = u'My title'
#         view = self.IdentificationReport(None, None)
#         self.assertEqual(view.title(node, None), u'My title')

#     def test_title_empty_problem_description(self):
#         node = mock.Mock()
#         node.type = 'risk'
#         node.identification = u'no'
#         node.title = u'My title'
#         zodb_node = mock.Mock()
#         zodb_node.problem_description = u'   '
#         view = self.IdentificationReport(None, None)
#         self.assertEqual(view.title(node, zodb_node), u'My title')

#     def test_title_risk_present_and_with_problem_description(self):
#         node = mock.Mock()
#         node.type = 'risk'
#         node.identification = u'no'
#         node.title = u'My title'
#         zodb_node = mock.Mock()
#         zodb_node.problem_description = u'Bad situation'
#         view = self.IdentificationReport(None, None)
#         self.assertEqual(view.title(node, zodb_node), u'Bad situation')


# class ShowNegateWarningTests(unittest.TestCase):

#     def _call(self, node, zodbnode):
#         report = IdentificationReport(None, None)
#         return report.show_negate_warning(node, zodbnode)

#     def test_show_Unanswered(self):
#         # https//code.simplon.biz/tracker/tno-euphorie/ticket/75
#         zodbnode = Risk()
#         zodbnode.problem_description = None
#         node = model.Risk(type="risk")
#         self.assertEqual(self._call(node, zodbnode), False)

#     def test_RiskNotPresent(self):
#         zodbnode = Risk()
#         zodbnode.problem_description = None
#         node = model.Risk(type="risk", identification="yes")
#         self.assertEqual(self._call(node, zodbnode), False)

#     def test_RiskNotApplicable(self):
#         zodbnode = Risk()
#         zodbnode.problem_description = None
#         node = model.Risk(type="risk", identification="n/a")
#         self.assertEqual(self._call(node, zodbnode), False)

#     def test_Present(self):
#         zodbnode = Risk()
#         zodbnode.problem_description = None
#         node = model.Risk(type="risk", identification="no")
#         self.assertEqual(self._call(node, zodbnode), True)

#     def test_HasProblemDescription(self):
#         zodbnode = Risk()
#         zodbnode.problem_description = u"Negative"
#         node = model.Risk(type="risk", identification="no")
#         self.assertEqual(self._call(node, zodbnode), False)

#     def test_HasEmptyProblemDescription(self):
#         zodbnode = Risk()
#         zodbnode.problem_description = u"   "
#         node = model.Risk(type="risk", identification="no")
#         self.assertEqual(self._call(node, zodbnode), True)


# XXX Change these test to check client.docx.html._HtmlToWord instead

# class HtmlToRtfTests(unittest.TestCase):

#     def HtmlToRtf(self, *a, **kw):
#         return HtmlToRtf(*a, **kw)

#     def render(self, output):
#         document = Document()
#         section = Section()
#         for o in output:
#             section.append(o)
#         document.Sections.append(section)
#         renderer = Renderer()
#         renderer.Write(document, StringIO())  # Setup instance variables
#         renderer._doc = document
#         renderer._fout = StringIO()
#         renderer._CurrentStyle = ""
#         renderer._WriteSection(section, True, False)
#         return renderer._fout.getvalue()

#     def testEmptyInput(self):
#         self.assertEqual(self.HtmlToRtf(u"", u"<stylesheet>"), [])

#     def testInvalidHtmlFallback(self):
#         self.assertTrue(
#             "text\\par" in
#             self.render(self.HtmlToRtf(u"<p>text</p>", u"<stylesheet>"))
#         )

#     def testBasicParagraph(self):
#         self.assertTrue(
#             "Simple text\\par" in self.render(
#                 self.HtmlToRtf(u"<p>Simple text</p>", u"<stylesheet>")
#             ), []
#         )

#     def testItalicInText(self):
#         self.assertTrue(
#             "Simple {\\i text}\\par" in self.render(
#                 self.
#                 HtmlToRtf(u"<p>Simple <em>text</em></p>", u"<stylesheet>")
#             )
#         )

#     def testBoldAndItalicText(self):
#         self.assertTrue(
#             "Very {\\i very }{\\b\\i bold}\\par" in self.render(
#                 self.HtmlToRtf(
#                     u"<p>Very <em>very <strong>bold</strong></em></p>",
#                     u"<stylesheet>"
#                 )
#             )
#         )

#     def testEmphasisInText(self):
#         self.assertTrue(
#             "{\\i text}" in
#             self.render(self.HtmlToRtf(u"<em>text</em>", u"<stylesheet>"))
#         )

#     def testInlineEntity(self):
#         self.assertTrue(
#             "Simple & clean\\par" in self.render(
#                 self.HtmlToRtf(u"<p>Simple &amp; clean</p>", u"<stylesheet>")
#             )
#         )

#     def testInlineEntityDigit(self):
#         self.assertTrue(
#             "Simple \r clean\\par" in self.render(
#                 self.HtmlToRtf(u"<p>Simple &#13; clean</p>", u"<stylesheet>")
#             )
#         )

#     def test_link_in_text(self):
#         # This demonstrates TNO Euphorie ticket 186
#         html = '<p>Check the <a rel="nofollow">manual</a> for more info.</p>'
#         rendering = self.render(self.HtmlToRtf(html, '<stylesheet>'))
#         self.assertTrue('Check the manual for more info.' in rendering)
#         self.assertEqual(rendering.count('more info'), 1)


class ActionPlanTimelineTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super(ActionPlanTimelineTests, self).setUp()
        self.account = addAccount(password="secret")

    def _get_timeline(self, context=None, request=None):
        """Return the timeline view"""

        class DummySurvey(mock.Mock, Base):

            __new__ = object.__new__

            def getPhysicalPath(self):
                return ("test", "dummy-survey")

        if request is None:
            request = self.request.clone()
            alsoProvides(request, IClientSkinLayer)
        if context is None:
            survey = DummySurvey()
            session = self._create_session()
            context = TraversedSurveySession(
                survey,
                session.id,
            ).__of__(survey)
        return api.content.get_view("timeline", context, request)

    def _create_session(self, dbsession=None):
        if dbsession is None:
            dbsession = Session()
        session = SurveySession(account=self.account, zodb_path="survey")
        dbsession.add(session)
        dbsession.flush()
        return session

    def test_get_measures_with_correct_module(self):
        view = self._get_timeline()
        session = view.context.session

        # This first module should be ignored, it doesn't contain any risks
        session.addChild(
            model.Module(
                zodb_path="1",
                module_id="1",
            )
        )
        # Between the next two modules, the first one (root-level) must be
        # returned.
        module = session.addChild(
            model.Module(
                zodb_path="2",
                module_id="2",
            )
        )
        module = module.addChild(
            model.Module(
                zodb_path="2/3",
                module_id="3",
            )
        )
        module.addChild(model.Risk(zodb_path="2/3/4", risk_id="1", identification="no"))
        survey = view.context.aq_parent
        survey.restrictedTraverse = lambda x: object
        survey.ProfileQuestions = lambda: []

        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][0].module_id, u"2")

    def test_get_measures_return_risks_without_measures(self):
        view = self._get_timeline()
        session = view.context.session

        module = session.addChild(
            model.Module(
                session=session,
                zodb_path="1",
                module_id="1",
            )
        )
        module.addChild(
            model.Risk(
                session=session, zodb_path="1/2", risk_id="1", identification="no"
            )
        )
        survey = view.context.aq_parent
        survey.restrictedTraverse = lambda x: object
        survey.ProfileQuestions = lambda: []

        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][2], None)

    def test_get_measures_filter_on_session(self):
        view = self._get_timeline()
        sessions = [
            view.context.session,
            self._create_session(),
        ]
        for session in sessions:
            module = session.addChild(
                model.Module(
                    session=session,
                    zodb_path="1",
                    module_id="1",
                )
            )
            module.addChild(
                model.Risk(
                    session=session,
                    zodb_path="1/2",
                    risk_id="1",
                    identification="no",
                    action_plans=[
                        model.ActionPlan(
                            action=u"Measure 1 for %s" % session.account.loginname
                        )
                    ],
                )
            )

        survey = view.context.aq_parent
        survey.restrictedTraverse = lambda x: object
        survey.ProfileQuestions = lambda: []

        measures = view.get_measures()
        self.assertEqual(len(measures), 1)
        self.assertEqual(measures[0][2].action, "Measure 1 for jane@example.com")

    def test_get_measures_order_by_start_date(self):
        view = self._get_timeline()
        session = view.context.session
        module = session.addChild(
            model.Module(
                session=session,
                zodb_path="1",
                module_id="1",
            )
        )
        module.addChild(
            model.Risk(
                session=session,
                zodb_path="1/2",
                risk_id="1",
                identification="no",
                action_plans=[
                    model.ActionPlan(
                        action=u"Plan 2", planning_start=datetime.date(2011, 12, 15)
                    ),
                    model.ActionPlan(
                        action=u"Plan 1", planning_start=datetime.date(2011, 11, 15)
                    ),
                ],
            )
        )

        survey = view.context.aq_parent
        survey.restrictedTraverse = lambda x: object
        survey.ProfileQuestions = lambda: []

        measures = view.get_measures()
        self.assertEqual(len(measures), 2)
        self.assertEqual([row[2].action for row in measures], [u"Plan 1", u"Plan 2"])

    def test_priority_name_known_priority(self):
        view = self._get_timeline()
        self.assertEqual(view.priority_name("high"), u"High")

    def test_priority_name_known_unpriority(self):
        view = self._get_timeline()
        self.assertEqual(view.priority_name("dummy"), "dummy")

    def test_create_workbook_empty_session(self):
        # If there are no risks only the header row should be generated.
        view = self._get_timeline()
        view.getModulePaths = lambda: []
        book = view.create_workbook()
        self.assertEqual(len(book.worksheets), 1)
        sheet = book.worksheets[0]
        self.assertEqual(len(tuple(sheet.rows)), 1)

    def test_create_workbook_plan_information(self):
        view = self._get_timeline()
        module = model.Module(
            zodb_path="1",
            title=u"Top-level Module title",
        )
        risk = model.Risk(
            zodb_path="1/2/3",
            risk_id="1",
            title=u"Risk title",
            priority="high",
            identification="no",
            path="001002003",
            comment=u"Risk comment",
        )
        plan = model.ActionPlan(
            action=u"Plan 2", planning_start=datetime.date(2011, 12, 15), budget=500
        )
        survey = view.context.aq_parent
        zodb_node = mock.Mock()
        zodb_node.problem_description = u"This is wrong."
        survey.restrictedTraverse.return_value = zodb_node

        view.get_measures = lambda: [(module, risk, plan)]
        wb = view.create_workbook()
        sheet = wb.worksheets[0]
        # planning start
        self.assertEqual(sheet["A2"].value, datetime.date(2011, 12, 15))
        # planning end
        self.assertEqual(sheet["B2"].value, None)
        # action plan
        self.assertEqual(sheet["C2"].value, u"Plan 2")
        # requirements
        self.assertEqual(sheet["D2"].value, None)
        # responsible
        self.assertEqual(sheet["E2"].value, None)
        # budget
        self.assertEqual(sheet["F2"].value, 500)
        # module title
        self.assertEqual(sheet["G2"].value, u"Top-level Module title")
        # risk number
        self.assertEqual(sheet["H2"].value, u"1.2.3")
        # risk title
        self.assertEqual(sheet["I2"].value, u"This is wrong.")
        # risk priority
        self.assertEqual(sheet["J2"].value, u"High")
        # risk comment
        self.assertEqual(sheet["K2"].value, u"Risk comment")

    def test_create_workbook_no_problem_description(self):
        view = self._get_timeline()
        module = model.Module(
            zodb_path="1",
            path="001",
            title=u"Top-level Module title",
        )
        risk = model.Risk(
            zodb_path="1/2/3",
            risk_id="1",
            title=u"Risk title",
            priority="high",
            identification="no",
            path="001002003",
            comment=u"Risk comment",
        )
        survey = view.context.aq_parent
        survey.ProfileQuestions = lambda: []
        zodb_node = mock.Mock()
        zodb_node.title = u"Risk title."
        zodb_node.problem_description = u"  "
        survey.restrictedTraverse.return_value = zodb_node
        view.getRisks = lambda x: [(module, risk)]
        sheet = view.create_workbook().worksheets[0]
        self.assertEqual(sheet["I2"].value, u"Risk title")

    def test_render_value(self):
        with api.env.adopt_user(user=self.account):
            view = self._get_timeline()
            view.context.session.title = u"Acmè"
            survey = view.context.aq_parent
            survey.ProfileQuestions = lambda: []
            view.__call__()
            response = view.request.response
            self.assertEqual(
                response.headers["content-type"],
                "application/vnd.openxmlformats-" "officedocument.spreadsheetml.sheet",
            )
            quoted_filename = quote(u"Timeline for Acmè.xlsx".encode("utf-8"))
            self.assertEqual(quoted_filename, "Timeline%20for%20Acm%C3%A8.xlsx")
            self.assertEqual(
                response.headers["content-disposition"],
                "attachment; filename*=UTF-8''{}".format(quoted_filename),
            )
