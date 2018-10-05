# coding=utf-8
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.testing import EuphorieFunctionalTestCase


class ProfileTests(EuphorieFunctionalTestCase):

    def testMultiProfiles(self):
        # Tests http://code.simplon.biz/tracker/euphorie/ticket/96
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <profile-question>
                          <title>Multiple profile question</title>
                          <question>Profile titles</question>
                          <description>&lt;p&gt;Profile description.&lt;/p&gt;</description>
                          <risk type="policy">
                            <title>Profile risk</title>
                            <description>&lt;p&gt;Risk description.&lt;/p&gt;</description>
                            <evaluation-method>direct</evaluation-method>
                          </risk>
                        </profile-question>
                        <module optional="false">
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
        browser = self.get_browser()
        browser.open(
            self.portal.client.nl["sector-title"]["survey-title"]
            .absolute_url()
        )
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="survey").value = ["sector-title/survey-title"]
        browser.getForm().submit()
        browser.getControl(name="form.widgets.title").value = "Test session"
        # Start the survey
        browser.getControl(name="form.button.submit").click()
        # Enter the profile information
        browser.getControl(
            name="1:utf8:utext:list", index=0
        ).value = "Profile 1"
        browser.getControl(
            name="1:utf8:utext:list", index=1
        ).value = "Profile 2"
        browser.getForm().submit()


class UpdateTests(EuphorieFunctionalTestCase):
    # This test is disabled because the queries used in copySessionData
    # are not compatible with SQLite.
    def XtestUpdateShowsRepeatableProfileItems(self):
        # Tests http://code.simplon.biz/tracker/tno-euphorie/ticket/85
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                        <profile-question>
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
        browser = self.get_browser()
        browser.open(
            self.portal.client.nl["sector-title"]["survey-title"]
            .absolute_url()
        )
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = "Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        # Enter the profile information
        browser.getControl(name="1:utext:list", index=0).value = "Profile 1"
        browser.getControl(name="1:utext:list", index=1).value = "Profile 2"
        browser.getForm().submit()
        # Change the survey and publish again
        from euphorie.client import publish
        survey = (
            self.portal.sectors["nl"]["sector-title"]["survey-title"]
            ["test-import"]
        )
        survey.invokeFactory("euphorie.module", "test module")
        publisher = publish.PublishSurvey(survey, self.portal.REQUEST)
        publisher.publish()
        # We should get an update notification now
        browser.getLink("Start Risk Identification").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/sector-title/survey-title/update"
        )
        # And our current profile should be listed
        self.assertEqual(
            browser.getControl(name="1:utext:list", index=0).value, "Profile 1"
        )
        self.assertEqual(
            browser.getControl(name="1:utext:list", index=1).value, "Profile 2"
        )
        # Confirm the profile
        browser.getForm().submit()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/sector-title/"
            "survey-title/identification"
        )
        # Make sure the profile is correct
        browser.getLink("Start Risk Identification").click()
        self.assertTrue("Profile 1" in browser.contents)
        self.assertTrue("Profile 2" in browser.contents)

    # This test is disabled because the queries used in copySessionData
    # are not compatible with SQLite.
    def XtestSkipChildrenFalseForMandatoryModules(self):
        """ Mandatory modules must have skip_children=False. It's possible that
            the module was optional with skip_children=True and now after the
            update must be mandatory.
        """
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                          <title>Survey title</title>
                          <module optional="true">
                              <title>Module Title</title>
                              <description>&lt;p&gt;Testing ticket #3860&lt;/p&gt;</description>
                              <question>What is the sound of one hand clapping?</question>
                              <risk type="risk">
                                  <title>This risk exists</title>
                                  <problem-description>This risk doesn't exist</problem-description>
                                  <description>&lt;p&gt;asdg&lt;/p&gt;</description>
                                  <show-not-applicable>false</show-not-applicable>
                                  <evaluation-method>direct</evaluation-method>
                              </risk>
                          </module>
                      </survey>
                  </sector>"""

        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        browser = self.get_browser()
        client_survey = self.portal.client.nl["sector-title"]["survey-title"]
        browser.open(client_survey.absolute_url())
        registerUserInClient(browser)
        # Create a new survey session
        browser.getControl(name="title:utf8:ustring").value = "Test session"
        browser.getControl(name="next", index=1).click()
        # Start the survey
        browser.getForm().submit()
        # Enter the profile information
        browser.getLink("Start Risk Identification").click()
        # Set Skip-children to True
        module_identification_url = browser.url
        browser.handleErrors = False
        # XXX: The following breaks when testing with sqlite but not with
        # postgres.
        browser.getControl(name="skip_children:boolean").controls[1].click()
        browser.getControl(name="next", index=1).click()
        # Change the survey to make the module required and publish again
        from euphorie.client import publish
        survey = self.portal.sectors["nl"]["sector-title"]["survey-title"
                                                           ]["test-import"]
        module = survey['1']
        module.optional = False
        publisher = publish.PublishSurvey(survey, self.portal.REQUEST)
        publisher.publish()

        # We should get an update notification now
        browser.open(client_survey.absolute_url())
        browser.getLink("Start Risk Identification").click()
        # We should now be on the module
        self.assertEqual(browser.url, module_identification_url)
        # But this time, the module's "optional" question (i.e to skip the
        # children) should not be there
        self.assertRaises(
            LookupError, browser.getControl, name='skip_children:boolean'
        )
        browser.getControl(name="next", index=1).click()
        # Now we must see the risk, i.e skip_children=False so we *must* answer
        # the risk
        self.assertEqual(
            "<legend>This risk exists</legend>" in browser.contents, True
        )
        # There are 2 inputs (2 radio, 1 hidden), for yes, no and postponed.
        self.assertEqual(len(browser.getControl(name="answer").controls), 3)
        self.assertEqual(
            browser.getControl(name="answer:default").value, 'postponed'
        )
