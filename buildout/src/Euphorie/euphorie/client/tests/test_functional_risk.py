# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient


class RiskTests(EuphorieFunctionalTestCase):
    def testPreventEarlyDate(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/150
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser=Browser()
        survey_url=self.portal.client.nl["ict"]["software-development"].absolute_url()
        browser.open(survey_url)
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value=u"Sessiøn".encode("utf-8")
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the risk
        browser.getControl("next").click()
        browser.getControl(name="answer").value=["no"]
        browser.getControl("next").click()
        # Move on to the risk's action plan form
        browser.getLink("Go to action plan").click()
        browser.getLink("Create action plan").click()
        browser.getLink("Next").click()
        # Try an early year
        browser.getControl(name="measure.action_plan:utf8:ustring:records").value="Do something awesome"
        browser.getControl(name="measure.planning_start_day:records").value="1"
        browser.getControl(name="measure.planning_start_month:records").value=["2"]
        browser.getControl(name="measure.planning_start_year:records").value="3"
        browser.getControl("next").click()
        self.assertEqual(browser.url,
                "http://nohost/plone/client/nl/ict/software-development/actionplan/1/1")
        self.assertTrue("Please enter a valid year after 1900" in browser.contents)

