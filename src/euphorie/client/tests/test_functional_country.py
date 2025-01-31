from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from urllib.parse import urlencode


class CountryFunctionalTests(EuphorieFunctionalTestCase):
    def test_surveys_filtered_by_language(self):
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector</title>
                      <survey>
                        <title>Survey</title>
                        <language>en</language>
                      </survey>
                    </sector>"""
        survey_nl = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Branche</title>
                    <survey>
                      <title>Vragenlijst</title>
                      <language>nl</language>
                    </survey>
                  </sector>"""  # noqa
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        addSurvey(self.portal, survey_nl)
        browser = self.get_browser()
        # Pass the language as URL parameter to ensure that we get the NL
        # version
        browser.open("%s?language=nl" % self.portal.client.absolute_url())
        registerUserInClient(browser, link="Registreer")
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        self.assertEqual(
            browser.getControl(name="survey").options, ["branche/vragenlijst"]
        )

        # Still Dutch
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        self.assertEqual(
            browser.getControl(name="survey").options, ["branche/vragenlijst"]
        )

        # Now, switch to English
        browser.open("%s?language=en" % self.portal.client["nl"].absolute_url())
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        self.assertEqual(browser.getControl(name="survey").options, ["sector/survey"])

    def test_must_select_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        browser.open(self.portal.client["nl"].absolute_url())
        registerUserInClient(browser, link="Register")
        data = urlencode({"action": "new", "survey": "", "title:utf8:ustring": "Foo"})
        browser.handleErrors = False
        browser.open(browser.url, data)
        self.assertEqual(browser.url, "http://nohost/plone/client/nl")
