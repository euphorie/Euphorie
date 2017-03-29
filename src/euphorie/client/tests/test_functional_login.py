# coding=utf-8
from Products.Five.testbrowser import Browser
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from euphorie.deployment.tests.functional import EuphorieTestCase
from z3c.appconfig.interfaces import IAppConfig
from zope.interface import alsoProvides
from zope import component
import re


class GuestAccountTests(EuphorieFunctionalTestCase):

    def test_guest_login_no_valid_survey(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.logout()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)
        browser = Browser()
        appconfig = component.getUtility(IAppConfig)
        allow_guest_accounts = appconfig['euphorie'].get('allow_guest_accounts', False)
        appconfig['euphorie']['allow_guest_accounts'] = True
        browser.open(self.portal.client.nl.absolute_url())
        self.assertTrue(
            re.search('run a test session', browser.contents)
            is not None)
        # No valid survey path is passed in came_from
        browser.open("%s/@@tryout?came_from=%s" % (
            self.portal.client.nl.absolute_url(),
            self.portal.client.nl.absolute_url()
        ))
        # Therefore we land on the "start new session" page
        self.assertTrue("This is a test session" in browser.contents)
        self.assertTrue("start a new session" in browser.contents)
        appconfig['euphorie']['allow_guest_accounts'] = allow_guest_accounts

    def test_guest_login_with_valid_survey(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.logout()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)
        browser = Browser()
        appconfig = component.getUtility(IAppConfig)
        allow_guest_accounts = appconfig['euphorie'].get('allow_guest_accounts', False)
        appconfig['euphorie']['allow_guest_accounts'] = True
        browser.open(self.portal.client.nl.absolute_url())
        self.assertTrue(
            re.search('run a test session', browser.contents)
            is not None)
        url = "{}/ict/software-development".format(
            self.portal.client.nl.absolute_url())
        # We pass in a valid survey path in came_from
        browser.open("{url}/@@tryout?came_from={url}".format(url=url))
        # Therefore we land on the start page of the survey
        self.assertTrue("This is a test session" in browser.contents)
        self.assertTrue("<h1>Software development</h1>" in browser.contents)
        appconfig['euphorie']['allow_guest_accounts'] = allow_guest_accounts


class LoginTests(EuphorieFunctionalTestCase):

    def test_login_not_case_sensitive(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'JANE@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name="next").click()
        self.assertTrue('@@login' not in browser.url)

    def test_use_session_cookie_by_default(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'jane@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name="next").click()
        auth_cookie = browser.cookies.getinfo('__ac')
        self.assertEqual(auth_cookie['expires'], None)

    def test_remember_user_sets_cookie_expiration(self):
        import datetime
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'jane@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name='remember').value = ['True']
        browser.getControl(name="next").click()
        auth_cookie = browser.cookies.getinfo('__ac')
        self.assertNotEqual(auth_cookie['expires'], None)
        delta = auth_cookie['expires'] - datetime.datetime.now(
                                            auth_cookie['expires'].tzinfo)
        self.assertTrue(delta.days > 100)

    def test_extra_ga_pageview_post_login(self):
        from euphorie.content.tests.utils import BASIC_SURVEY
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import addAccount
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'JANE@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name="next").click()
        self.assertTrue(re.search('trackPageview.*login_form/success', browser.contents) is not None)


class RegisterTests(EuphorieTestCase):
    def afterSetUp(self):
        super(RegisterTests, self).afterSetUp()
        self.loginAsPortalOwner()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)

    def test_lowercase_email(self):
        view = self.portal.client.restrictedTraverse("register")
        view.errors = {}
        view.request.form['email'] = 'JANE@example.com'
        view.request.form['password1'] = 'secret'
        view.request.form['password2'] = 'secret'
        account = view._tryRegistration()
        self.assertEqual(account.loginname, 'jane@example.com')

    def testConflictWithPloneAccount(self):
        view = self.portal.client.restrictedTraverse("register")
        view.errors = {}
        view.request.form["email"] = self.portal._owner[1]
        view.request.form["password1"] = "secret"
        view.request.form["password2"] = "secret"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)

    def testBasicEmailVerification(self):
        view = self.portal.client.restrictedTraverse("register")
        view.errors = {}
        view.request.form["email"] = "wichert"
        view.request.form["password1"] = "secret"
        view.request.form["password2"] = "secret"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)

        view.errors.clear()
        view.request.form["email"] = "wichert@wiggy net"
        self.assertEqual(view._tryRegistration(), False)
        self.failUnless("email" in view.errors)

        view.errors.clear()
        view.request.form["email"] = "wichert@wiggy.net"
        self.assertNotEqual(view._tryRegistration(), False)


class ReminderTests(EuphorieFunctionalTestCase):
    def addDummySurvey(self):
        from euphorie.client.tests.utils import addSurvey
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                      </survey>
                    </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)

    def testUnknownAccount(self):
        self.addDummySurvey()
        browser = Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getLink("I forgot my password").click()
        browser.getControl(name="loginname").value = "jane@example.com"
        browser.getControl(name="next").click()
        self.failUnless("Unknown email address" in browser.contents)

    def testEmail(self):
        from euphorie.client.tests.utils import MockMailFixture
        from euphorie.client.tests.utils import addAccount
        self.addDummySurvey()
        addAccount()
        mail_fixture = MockMailFixture()
        self.portal.email_from_address = "discard@simplon.biz"
        self.portal.email_from_name = "Euphorie website"
        browser = Browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getLink("I forgot my password").click()
        browser.getControl(name="loginname").value = "jane@example.com"
        browser.getControl(name="next").click()
        self.assertEqual(len(mail_fixture.storage), 1)
        (args, kw) = mail_fixture.storage[0]
        (mail, mto, mfrom) = args[:3]
        self.assertEqual(mfrom, "discard@simplon.biz")
        self.assertEqual(mto, "jane@example.com")
        self.assertEqual(
                unicode(mail["Subject"]),
                u"OiRA registration reminder")
        body = mail.get_payload(0).get_payload(decode=True)\
                .decode(mail.get_content_charset("utf-8"))
        self.failUnless(u"Øle" in body)
