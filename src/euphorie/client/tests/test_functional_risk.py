# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient


class RiskTests(EuphorieFunctionalTestCase):
    def testShowFrenchEvaluation(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = Browser()
        survey = self.portal.client.nl["ict"]["software-development"]
        survey.evaluation_algorithm = u"french"
        survey["1"]["2"].type = "risk"
        browser.open(survey.absolute_url())
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = \
                u"Sessiøn".encode("utf-8")
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the risk
        browser.getControl("next").click()
        browser.getControl(name="answer").value = ["no"]
        # Verify number of options
        self.assertEqual(
                len(browser.getControl(name="frequency:int").controls), 4)
        self.assertEqual(
                len(browser.getControl(name="severity:int").controls), 4)
        # Enter some digits
        browser.getControl(name="frequency:int").value = ["7"]
        browser.getControl(name="severity:int").value = ["10"]
        browser.getControl("next").click()
        # Verify the result
        browser.open(
                "http://nohost/plone/client/nl/ict/"
                "software-development/actionplan/1/1")
        self.assertEqual(browser.getControl(name="priority").value, ["high"])

    def XtestPreventEarlyDate(self):
        """
        Deactivated until we decide what to do about this kind of validation
        error check
        """
        from euphorie.content.tests.utils import BASIC_SURVEY
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = Browser()
        survey_url = self.portal.client.nl["ict"]["software-development"]\
                .absolute_url()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = \
                u"Sessiøn".encode("utf-8")
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the risk
        browser.getControl("next").click()
        browser.getControl(name="answer").value = ["no"]
        browser.getControl("next").click()
        # Move on to the risk's action plan form
        browser.getLink("Create action plan").click()
        browser.getLink("Next").click()
        # Try an early year
        browser.getControl(name="measure.action_plan:utf8:ustring:records", index=0)\
                .value = "Do something awesome"
        browser.getControl(name="measure.planning_start_day:records", index=0)\
                .value = "1"
        browser.getControl(name="measure.planning_start_month:records", index=0)\
                .value = ["2"]
        browser.getControl(name="measure.planning_start_year:records", index=0)\
                .value = "3"
        browser.getControl("next").click()
        self.assertEqual(browser.url,
                "http://nohost/plone/client/nl/ict/"
                "software-development/actionplan/1/1")
        self.assertTrue(
                "Please enter a year between 2000 and 2100"
                in browser.contents)

    def Xtest_do_not_abort_on_far_future(self):
        """
        Deactivated, since such a far-future date can not be entered any more
        in modern browsers
        """
        from euphorie.content.tests.utils import BASIC_SURVEY
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = Browser()
        survey_url = (self.portal.client.nl["ict"]
                ["software-development"].absolute_url())
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = \
                u"Sessiøn".encode("utf-8")
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the risk
        browser.getControl("next").click()
        browser.getControl(name="answer").value = ["no"]
        browser.getControl("next").click()
        # Move on to the risk's action plan form
        browser.getLink("Create action plan").click()
        browser.getLink("Next").click()
        # Try an early year
        browser.getControl(name="measure.action_plan:utf8:ustring:records", index=0)\
                .value = "Do something awesome"
        browser.getControl(name="measure.planning_start:records", index=0)\
                .value = "12345/02/01"
        browser.handleErrors = False
        browser.getControl("next").click()
        self.assertEqual(browser.url,
                "http://nohost/plone/client/nl/ict/"
                "software-development/actionplan/1/1")
        self.assertTrue(
                "Please enter a year between 2000 and 2100"
                in browser.contents)

    def test_set_unknown_answer_if_skipped(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        # Register in the client
        browser = Browser()
        survey_url = self.portal.client.nl['ict']['software-development']\
                .absolute_url()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name='title:utf8:ustring').value = u'Session'
        browser.getControl(name='next').click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink('Start Risk Identification').click()
        browser.getControl('next').click()
        # No answer should be set on initial view
        self.assertEqual(browser.getControl(name='answer').value, [])
        # Do not give an identification answer
        risk_url = browser.url
        browser.getControl('next').click()
        # Go back and check the new answer
        browser.open(risk_url)
        self.assertTrue(
            'class="current postponed'
            in browser.contents)
