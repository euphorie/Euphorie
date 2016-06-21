# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient


class SurveyTests(EuphorieFunctionalTestCase):
    def test_policy_gets_high_priority(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/93
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <evaluation-optional>false</evaluation-optional>
                        <module optional="false">
                          <title>Policy parent</title>
                          <description>&lt;p&gt;Een module met een beleidsrisico.&lt;/p&gt;</description>
                          <risk type="policy">
                            <title>Policy problem!</title>
                            <problem-description>There is a policy problem.</problem-description>
                            <description>&lt;p&gt;Random text.&lt;/p&gt;</description>
                            <show-not-applicable>false</show-not-applicable>
                          </risk>
                        </module>
                      </survey>
                    </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser = Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"]
                        .absolute_url())
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = "Test session"
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the risk
        browser.open("http://nohost/plone/client/nl/sector-title/"
                     "survey-title/identification/1/1")
        browser.getControl(name="answer").value = ["no"]
        browser.getControl(name="next", index=1).click()
        # Check priority in action plan
        browser.open("http://nohost/plone/client/nl/sector-title/"
                     "survey-title/actionplan/1/1")
        self.assertEqual(browser.getControl(name="priority").value, ["high"])

    def test_top5_gets_high_priority(self):
        # Test for http://code.simplon.biz/tracker/tno-euphorie/ticket/93
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <evaluation-optional>false</evaluation-optional>
                        <module optional="false">
                          <title>Top5 parent</title>
                          <description>&lt;p&gt;Een module met een top-5 risico.&lt;/p&gt;</description>
                          <risk type="top5">
                            <title>Top-5 probleem!</title>
                            <problem-description>Er is een top-5 probleem.</problem-description>
                            <description>&lt;p&gt;Zomaar wat tekst.&lt;/p&gt;</description>
                            <show-not-applicable>false</show-not-applicable>
                          </risk>
                        </module>
                      </survey>
                    </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser = Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"]
                                .absolute_url())
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = "Test session"
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the top-5 risk
        browser.open("http://nohost/plone/client/nl/sector-title/"
                     "survey-title/identification/1/1")
        browser.getControl(name="answer").value = ["no"]
        browser.getControl(name="next", index=1).click()
        # Check priority in action plan
        browser.open("http://nohost/plone/client/nl/sector-title/"
                     "survey-title/actionplan/1/1")
        self.assertEqual(browser.getControl(name="priority").value, ["high"])

    def test_top5_skipped_in_evaluation(self):
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/105
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <evaluation-optional>false</evaluation-optional>
                        <module optional="false">
                          <title>Top5 parent</title>
                          <description>&lt;p&gt;Een module met een top-5 risico.&lt;/p&gt;</description>
                          <risk type="top5">
                            <title>Top-5 probleem!</title>
                            <problem-description>Er is een top-5 probleem.</problem-description>
                            <description>&lt;p&gt;Zomaar wat tekst.&lt;/p&gt;</description>
                            <show-not-applicable>false</show-not-applicable>
                          </risk>
                        </module>
                      </survey>
                    </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser = Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"]
                .absolute_url())
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = "Test session"
        browser.getControl(name="next").click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the top-5 risk
        browser.open("http://nohost/plone/client/nl/sector-title/"
                        "survey-title/identification/1/1")
        browser.getControl(name="answer").value = ["no"]
        # No evaluation is necessary
        self.assertTrue(
                "The risk evaluation has been automatically done by the tool"
                in browser.contents)
