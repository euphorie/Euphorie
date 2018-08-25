# coding=utf-8
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import MockMailFixture
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from z3c.appconfig.interfaces import IAppConfig
from zope import component
from zope.interface import alsoProvides

import datetime
import re
import six


class GuestAccountTests(EuphorieFunctionalTestCase):

    def test_guest_login_no_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.logout()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)
        browser = self.get_browser()
        appconfig = component.getUtility(IAppConfig)
        allow_guest_accounts = appconfig['euphorie'].get(
            'allow_guest_accounts', False
        )
        appconfig['euphorie']['allow_guest_accounts'] = True
        browser.open(self.portal.client.nl.absolute_url())
        self.assertTrue(
            re.search('run a test session', browser.contents) is not None
        )
        # No valid survey path is passed in came_from
        browser.open(
            "%s/@@tryout?came_from=%s" % (
                self.portal.client.nl.absolute_url(),
                self.portal.client.nl.absolute_url()
            )
        )
        # Therefore we land on the "start new session" page
        self.assertTrue("This is a test session" in browser.contents)
        self.assertTrue("Start a new session" in browser.contents)
        appconfig['euphorie']['allow_guest_accounts'] = allow_guest_accounts

    def test_guest_login_with_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.logout()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)
        browser = self.get_browser()
        appconfig = component.getUtility(IAppConfig)
        allow_guest_accounts = appconfig['euphorie'].get(
            'allow_guest_accounts', False
        )
        appconfig['euphorie']['allow_guest_accounts'] = True
        browser.open(self.portal.client.nl.absolute_url())
        self.assertTrue(
            re.search('run a test session', browser.contents) is not None
        )
        url = "{}/ict/software-development".format(
            self.portal.client.nl.absolute_url()
        )
        # We pass in a valid survey path in came_from
        browser.open("{url}/@@tryout?came_from={url}".format(url=url))
        # Therefore we land on the start page of the survey
        self.assertTrue("This is a test session" in browser.contents)
        self.assertTrue("<h1>Software development</h1>" in browser.contents)
        appconfig['euphorie']['allow_guest_accounts'] = allow_guest_accounts


class LoginTests(EuphorieFunctionalTestCase):

    def test_login_not_case_sensitive(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'JANE@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name="next").click()
        self.assertTrue('@@login' not in browser.url)

    def test_use_session_cookie_by_default(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'jane@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name="next").click()
        auth_cookie = browser.cookies.getinfo('__ac')
        self.assertEqual(auth_cookie['expires'], None)

    def test_remember_user_sets_cookie_expiration(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'jane@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name='remember').value = ['True']
        browser.getControl(name="next").click()
        auth_cookie = browser.cookies.getinfo('__ac')
        self.assertNotEqual(auth_cookie['expires'], None)
        delta = auth_cookie['expires'] - datetime.datetime.now(
            auth_cookie['expires'].tzinfo
        )
        self.assertTrue(delta.days > 100)

    def test_extra_ga_pageview_post_login(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password='secret')
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getControl(name='__ac_name').value = 'JANE@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name="next").click()
        self.assertTrue(
            re.search('trackPageview.*login_form/success', browser.contents) is
            not None
        )


class RegisterTests(EuphorieIntegrationTestCase):

    def test_lowercase_email(self):
        with self._get_view('register', self.portal.client) as view:
            view.errors = {}
            view.request.form['email'] = 'JANE@example.com'
            view.request.form['password1'] = 'secret'
            view.request.form['password2'] = 'secret'
            account = view._tryRegistration()
            self.assertEqual(account.loginname, 'jane@example.com')

    def testConflictWithPloneAccount(self):
        with self._get_view('register', self.portal.client) as view:
            view.errors = {}
            view.request.form["email"] = self.portal._owner[1]
            view.request.form["password1"] = "secret"
            view.request.form["password2"] = "secret"
            self.assertEqual(view._tryRegistration(), False)
            self.failUnless("email" in view.errors)

    def testBasicEmailVerification(self):
        with self._get_view('register', self.portal.client) as view:
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


class ResetPasswordTests(EuphorieFunctionalTestCase):

    def addDummySurvey(self):
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                      </survey>
                    </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        self.logout()

    def testUnknownAccount(self):
        self.addDummySurvey()
        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url)
        browser.getLink('Login').click()
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"  # noqa: E501
        browser.getControl(name="form.buttons.save").click()

        # We do not have any account here
        self.assertListEqual(model.Session.query(model.Account).all(), [])
        # Even if the user does not exist, the form submission
        # will be successfully sent
        self.assertTrue(
            browser.url.startswith('http://nohost/plone/client/nl/@@login?came_from')  # noqa: E501
        )

    def testInvalidEmail(self):
        self.addDummySurvey()
        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url)
        browser.getLink('Login').click()
        browser.getLink("I forgot my password").click()
        # Test an invalid email address
        browser.getControl(name="form.widgets.email").value = "jane @ joe.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertIn('The specified email is not valid.', browser.contents)
        self.assertEqual(
            browser.url,
            'http://nohost/plone/client/nl/@@reset_password_request',
        )

    def testEmail(self):
        self.addDummySurvey()
        addAccount()
        mail_fixture = MockMailFixture()
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url())
        browser.getLink('Login').click()
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"  # noqa: E501
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(len(mail_fixture.storage), 1)
        (args, kw) = mail_fixture.storage[0]
        (mail, mto, mfrom) = args[:3]
        self.assertEqual(mfrom, "discard@simplon.biz")
        self.assertEqual(mto, "jane@example.com")
        self.assertEqual(
            six.text_type(mail["Subject"]),
            u"OiRA password reset instructions",
        )
        body = mail.get_payload(0).get_payload(decode=True).decode(
            mail.get_content_charset("utf-8")
        )
        self.failUnless(u"/passwordreset/" in body)

    def testInvalidResetKey(self):
        ''' When the request key is invalid the user is invited
        to request a new key
        '''
        self.addDummySurvey()
        browser = self.get_browser()
        for url in (
            self.portal.client.nl.absolute_url() + '/passwordreset',
            self.portal.client.nl.absolute_url() + '/passwordreset/foo',
        ):
            browser.open(url)
            browser.getControl(name="form.widgets.new_password").value = "secret"  # noqa: E501
            browser.getControl(name="form.widgets.new_password.confirm").value = "secret"  # noqa: E501
            browser.getControl(label="Save changes").click()
            self.assertEqual(
                browser.url,
                'http://nohost/plone/client/nl/@@reset_password_request',
            )
