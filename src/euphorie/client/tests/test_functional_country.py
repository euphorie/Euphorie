# coding=utf-8
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import registerUserInClient
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase

import urllib


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
        # Note, this used to test that the URL was that of the client,
        # in the correct country (nl), with `?language=nl-NL` appended.
        # I don't see where in the code this language URL parameter would
        # come from, so I remove it in this test as well.
        self.assertEqual(browser.url, "http://nohost/plone/client/nl")
        self.assertEqual(
            browser.getControl(name="survey").options, ["branche/vragenlijst"]
        )
        browser.open(
            "%s?language=en" % self.portal.client["nl"].absolute_url()
        )
        self.assertEqual(
            browser.getControl(name="survey").options, ["sector/survey"]
        )

    def test_must_select_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = self.get_browser()
        browser.open(self.portal.client['nl'].absolute_url())
        registerUserInClient(browser)
        data = urllib.urlencode({
            'action': 'new',
            'survey': '',
            'title:utf8:ustring': 'Foo'
        })
        browser.handleErrors = False
        browser.open(browser.url, data)
        self.assertEqual(browser.url, 'http://nohost/plone/client/nl')
