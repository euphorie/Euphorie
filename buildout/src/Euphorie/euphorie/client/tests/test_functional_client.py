from euphorie.deployment.tests.functional import EuphorieDeploymentFunctionalTestCase
from Products.Five.testbrowser import Browser


class ClientTests(EuphorieDeploymentFunctionalTestCase):
    def addSurvey(self, survey):
        from euphorie.content import upload
        from euphorie.client import publish
        self.loginAsPortalOwner()
        importer=upload.SectorImporter(self.portal.sectors.nl)
        sector=importer(survey, None, None, u"test import")
        survey=sector.values()[0]["test-import"]
        publisher=publish.PublishSurvey(survey, self.portal.REQUEST)
        publisher()

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

        self.addSurvey(survey)
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


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

