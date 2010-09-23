# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey

class CountryTests(EuphorieFunctionalTestCase):
    def register(self, browser):
        # If this getLink failed the translations may not be compiled yet. This
        # can happen if you run tests without ever having started Zope.
        browser.getLink("Registreer").click()
        browser.getControl(name="email").value="guest"
        browser.getControl(name="password1:utf8:ustring").value="guest"
        browser.getControl(name="password2:utf8:ustring").value="guest"
        browser.getControl(name="next", index=1).click()


    def testSessionFiltersByLanguage(self):
        survey="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Sector</title>
                    <survey>
                      <title>Survey</title>
                      <language>en</language>
                    </survey>
                  </sector>"""
        survey_nl="""<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Branche</title>
                    <survey>
                      <title>Vragenlijst</title>
                      <language>nl</language>
                    </survey>
                  </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        addSurvey(self.portal, survey_nl)
        browser=Browser()
        browser.open(self.portal.client.absolute_url())
        browser.getLink("Nederlands", index=1).click()
        self.register(browser)
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/?language=nl-NL")
        self.assertEqual(browser.getControl(name="survey").options,
                ["branche/vragenlijst"])
        browser.open("%s?language=en" % self.portal.client["nl"].absolute_url())
        self.assertEqual(browser.getControl(name="survey").options,
                ["sector/survey"])

