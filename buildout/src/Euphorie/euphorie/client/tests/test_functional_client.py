# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey


class SurveyTests(EuphorieFunctionalTestCase):
    def register(self, browser):
        browser.getLink("register").click()
        browser.getControl(name="email").value="guest"
        browser.getControl(name="password1:utf8:ustring").value="guest"
        browser.getControl(name="password2:utf8:ustring").value="guest"
        browser.getControl(name="next", index=1).click()

    def testMultiProfiles(self):
        # Tests http://code.simplon.biz/tracker/euphorie/ticket/96
        survey="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Sector title</title>
                    <survey>
                      <title>Survey title</title>
                      <profile-question type="repeat">
                        <title>Multiple profile question</title>
                        <question>Profile titles</question>
                        <description>&lt;p&gt;Profile description.&lt;/p&gt;</description>
                        <risk type="policy">
                          <title>Profile risk</title>
                          <description>&lt;p&gt;Risk description.&lt;/p&gt;</description>
                          <evaluation-method>direct</evaluation-method>
                        </risk>
                      </profile-question>
                      <module optional="no">
                        <title>Module title</title>
                        <description>&lt;p&gt;Module description.&lt;/p&gt;</description>
                        <risk type="policy">
                          <title>Module risk</title>
                          <description>&lt;p&gt;Module description.&lt;/p&gt;</description>
                          <evaluation-method>direct</evaluation-method>
                        </risk>
                      </module>
                    </survey>
                  </sector>"""

        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser=Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"].absolute_url())
        self.register(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value="Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        # Enter the profile information
        browser.getControl(name="1:utext:list", index=0).value="Profile 1"
        browser.getControl(name="1:utext:list", index=1).value="Profile 2"
        browser.getForm().submit()


    def testUpdateShowsRepeatableProfileItems(self):
        # Tests http://code.simplon.biz/tracker/tno-euphorie/ticket/85
        survey="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Sector title</title>
                    <survey>
                      <title>Survey title</title>
                      <profile-question type="repeat">
                        <title>Multiple profile question</title>
                        <question>Profile titles</question>
                        <description>&lt;p&gt;Profile description.&lt;/p&gt;</description>
                        <risk type="policy">
                          <title>Profile risk</title>
                          <description>&lt;p&gt;Risk description.&lt;/p&gt;</description>
                          <evaluation-method>direct</evaluation-method>
                        </risk>
                      </profile-question>
                    </survey>
                  </sector>"""

        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser=Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"].absolute_url())
        self.register(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value="Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        # Enter the profile information
        browser.getControl(name="1:utext:list", index=0).value="Profile 1"
        browser.getControl(name="1:utext:list", index=1).value="Profile 2"
        browser.getForm().submit()
        # Change the survey and publish again
        from euphorie.client import publish
        survey=self.portal.sectors["nl"]["sector-title"]["survey-title"]["test-import"]
        survey.invokeFactory("euphorie.module", "test module")
        publisher=publish.PublishSurvey(survey, self.portal.REQUEST)
        publisher.publish()
        # We should get an update notification now
        browser.getLink("Start Risk Identification").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/sector-title/survey-title/update")
        # And out current profile should be listed
        self.assertEqual(browser.getControl(name="1:utext:list", index=0).value, "Profile 1")
        self.assertEqual(browser.getControl(name="1:utext:list", index=1).value, "Profile 2")


    def testUpdateShowsOptionalProfileItems(self):
        survey="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Sector title</title>
                    <survey>
                      <title>Survey title</title>
                      <profile-question type="optional">
                        <title>Optional profile question one</title>
                        <question>Yes or no</question>
                        <description>&lt;p&gt;Profile description.&lt;/p&gt;</description>
                      </profile-question>
                      <profile-question type="optional">
                        <title>Optional profile question two</title>
                        <question>Yay or nay</question>
                        <description>&lt;p&gt;Profile description.&lt;/p&gt;</description>
                      </profile-question>
                    </survey>
                  </sector>"""

        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser=Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"].absolute_url())
        self.register(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value="Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        # Enter the profile information
        browser.getControl(name="1:boolean").value=False
        browser.getControl(name="2:boolean").value=True
        browser.getForm().submit()
        # Change the survey and publish again
        from euphorie.client import publish
        survey=self.portal.sectors["nl"]["sector-title"]["survey-title"]["test-import"]
        survey.invokeFactory("euphorie.module", "test module")
        publisher=publish.PublishSurvey(survey, self.portal.REQUEST)
        publisher.publish()
        # We should get an update notification now
        browser.getLink("Start Risk Identification").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/sector-title/survey-title/update")
        # And out current profile should be listed
        self.assertEqual(browser.getControl(name="1:boolean").value, False)
        self.assertEqual(browser.getControl(name="2:boolean").value, True)

    def testTop5SkippedInEvaluation(self):
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/105
        survey="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Sector title</title>
                    <survey>
                      <title>Survey title</title>
                      <evaluation-optional>false</evaluation-optional>
                      <module optional="false">
                        <title>Top5 parent</title>
                        <description>&lt;p&gt;Een module met een top-5 risico.&lt;/p&gt;</description>
                        <risk type="risk">
                          <title>Top-5 probleem!</title>
                          <problem-description>Er is een top-5 probleem.</problem-description>
                          <description>&lt;p&gt;Zomaar wat tekst.&lt;/p&gt;</description>
                          <show-not-applicable>false</show-not-applicable>
                          <evaluation-method>calculated</evaluation-method>
                        </risk>
                      </module>
                    </survey>
                  </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser=Browser()
        browser.open(self.portal.client.nl["sector-title"]["survey-title"].absolute_url())
        self.register(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value="Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        browser.getLink("Start Risk Identification").click()
        # Identify the top-5 risk
        browser.open("http://nohost/plone/client/nl/sector-title/survey-title/identification/1/1")
        browser.getControl(name="answer").value=["no"]
        browser.getControl(name="next", index=1).click()
        # Check what the evaluation found
        browser.open("http://nohost/plone/client/nl/sector-title/survey-title/evaluation")
        self.assertTrue("There are no risks that need to be evaluated" in browser.contents)

