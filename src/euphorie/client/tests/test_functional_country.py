# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser
from euphorie.client.tests.utils import addSurvey


class CountryTests(EuphorieFunctionalTestCase):
    def View(self, *a, **kw):
        from ..country import View
        return View(*a, **kw)

    def test_sessions_ordering(self):
        import datetime
        from euphorie.content.tests.utils import BASIC_SURVEY
        from z3c.saconfig import Session
        from AccessControl.SecurityManagement import newSecurityManager
        from ..model import Account
        from ..model import SurveySession
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        session = Session()
        account = Account(loginname='johny',
                sessions=[
                    SurveySession(zodb_path='nl/ict/software-development',
                        title=u'One',
                        modified=datetime.datetime(2012, 12, 10)),
                    SurveySession(zodb_path='nl/ict/software-development',
                        title=u'Three',
                        modified=datetime.datetime(2012, 12, 12)),
                    SurveySession(zodb_path='nl/ict/software-development',
                        title=u'Two',
                        modified=datetime.datetime(2012, 12, 11))])
        session.add(account)
        newSecurityManager(None, account)
        view = self.View(self.portal.client['nl'], None)
        self.assertEqual(
                [s['title'] for s in view.sessions()],
                [u'Three', u'Two', 'One'])

    def test_surveys_filtered_by_language(self):
        from euphorie.client.tests.utils import registerUserInClient
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector</title>
                      <survey>
                        <title>Survey</title>
                        <language>en</language>
                      </survey>
                    </sector>"""
        survey_nl = \
                """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                    <title>Branche</title>
                    <survey>
                      <title>Vragenlijst</title>
                      <language>nl</language>
                    </survey>
                  </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        addSurvey(self.portal, survey_nl)
        browser = Browser()
        browser.open(self.portal.client.absolute_url())
        browser.getLink("Nederlands").click()
        registerUserInClient(browser, link="Registreer")
        # Note, this used to test that the URL was that of the client,
        # in the correct country (nl), with `?language=nl-NL` appended.
        # I don't see where in the code this language URL parameter would
        # come from, so I remove it in this test as well.
        self.assertEqual(
                browser.url,
                "http://nohost/plone/client/nl")
        browser.getLink(id='button-new-session').click()
        self.assertEqual(browser.getControl(name="survey").options,
                ["branche/vragenlijst"])
        browser.open("%s?language=en" % self.portal.client["nl"].absolute_url())
        browser.getLink(id='button-new-session').click()
        self.assertEqual(browser.getControl(name="survey").options,
                ["sector/survey"])

    def test_must_select_valid_survey(self):
        import urllib
        from euphorie.client.tests.utils import registerUserInClient
        from euphorie.content.tests.utils import BASIC_SURVEY
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        browser = Browser()
        browser.open(self.portal.client['nl'].absolute_url())
        registerUserInClient(browser)
        data = urllib.urlencode({'action': 'new',
                                 'survey': '',
                                 'title:utf8:ustring': 'Foo'})
        browser.handleErrors = False
        browser.open(browser.url, data)
        self.assertEqual(browser.url, 'http://nohost/plone/client/nl')
