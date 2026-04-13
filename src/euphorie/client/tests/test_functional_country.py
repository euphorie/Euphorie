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
        # We want the NL version.
        browser = self.get_browser(language="nl")
        browser.open(self.portal.client.absolute_url())
        registerUserInClient(browser)
        # By default, all surveys within this country are shown.
        country_url = self.portal.client["nl"].absolute_url()
        browser.open(f"{country_url}/surveys")
        self.assertTrue(
            browser.getForm(action=f"{country_url}/sector/survey/@@new-session.html")
        )
        self.assertTrue(
            browser.getForm(
                action=f"{country_url}/branche/vragenlijst/@@new-session.html"
            )
        )

        # There is a filter where you can query a specific language.
        # Get English only
        browser.open(f"{country_url}/surveys?Language=en")
        self.assertTrue(
            browser.getForm(action=f"{country_url}/sector/survey/@@new-session.html")
        )
        with self.assertRaises(LookupError):
            browser.getForm(
                action=f"{country_url}/branche/vragenlijst/@@new-session.html"
            )

        # Get Dutch only
        browser.open(f"{country_url}/surveys?Language=nl")
        with self.assertRaises(LookupError):
            browser.getForm(action=f"{country_url}/sector/survey/@@new-session.html")
        self.assertTrue(
            browser.getForm(
                action=f"{country_url}/branche/vragenlijst/@@new-session.html"
            )
        )

    def test_available_tools_portlet_not_filtered_by_language(self):
        # We used to filter on language, but no longer:
        # plone.use_request_negotiation is set to True.
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
        # We want the NL version.
        browser = self.get_browser(language="nl")
        browser.open(self.portal.client.absolute_url())
        registerUserInClient(browser)
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        self.assertEqual(
            browser.getControl(name="survey").options,
            ["sector/survey", "branche/vragenlijst"],
        )

        # Now, switch to English.
        # This no longer should have an effect.
        browser.open("%s?set_language=en" % self.portal.client["nl"].absolute_url())
        # We need to manually open the portlet view as the test browser
        # does not handle JavaScript.
        browser.open(
            self.portal.client["nl"].absolute_url() + "/@@portlet-available-tools"
        )
        self.assertEqual(
            browser.getControl(name="survey").options,
            ["sector/survey", "branche/vragenlijst"],
        )

    def test_must_select_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        browser.open(self.portal.client.absolute_url())
        # By default 'registerUserInClient' looks for the Dutch 'Registreer'
        # link, but we need to link for the English version.
        registerUserInClient(browser, link="Register")
        data = urlencode({"action": "new", "survey": "", "title:utf8:ustring": "Foo"})
        browser.handleErrors = False
        browser.open(browser.url, data)
        self.assertEqual(browser.url, "http://nohost/plone/client/nl")
