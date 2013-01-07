# coding=utf-8

from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


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
        browser.getControl(name='__ac_name').value = 'jane@example.com'
        browser.getControl(name='__ac_password:utf8:ustring').value = 'secret'
        browser.getControl(name='remember').value = ['True']
        browser.getControl(name="next").click()
        auth_cookie = browser.cookies.getinfo('__ac')
        self.assertNotEqual(auth_cookie['expires'], None)
        delta = auth_cookie['expires'] - datetime.datetime.now(
                                            auth_cookie['expires'].tzinfo)
        self.assertTrue(delta.days > 100)


class RegisterTests(EuphorieTestCase):
    def afterSetUp(self):
        from zope.interface import alsoProvides
        from euphorie.client.interfaces import IClientSkinLayer
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
