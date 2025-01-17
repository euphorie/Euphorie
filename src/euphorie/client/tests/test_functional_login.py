from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import MockMailFixture
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISecuritySchema
from transaction import commit
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope.component import getUtility
from zope.interface import alsoProvides

import datetime
import re
import transaction


class GuestAccountTests(EuphorieFunctionalTestCase):
    def test_guest_login_no_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.logout()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)
        browser = self.get_browser()
        api.portal.set_registry_record("euphorie.allow_guest_accounts", True)
        commit()
        browser.open(self.portal.client.nl.absolute_url())
        self.assertIn("Start a test session", browser.contents)
        # No valid survey path is passed in came_from
        browser.open(
            "%s/@@surveys?came_from=%s"
            % (
                self.portal.client.nl.absolute_url(),
                self.portal.client.nl.absolute_url(),
            )
        )
        # Therefore we land on the "start new session" page
        self.assertIn("Test session", browser.contents)

    def test_guest_login_with_valid_survey(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.logout()
        alsoProvides(self.portal.client.REQUEST, IClientSkinLayer)
        browser = self.get_browser()
        api.portal.set_registry_record("euphorie.allow_guest_accounts", True)
        commit()
        browser.open(self.portal.client.nl.absolute_url())
        self.assertIn("Start a test session", browser.contents)
        url = f"{self.portal.client.nl.absolute_url()}/ict/software-development"
        # We pass in a valid survey path in came_from
        browser.open("{url}/@@tryout?came_from={url}".format(url=url))
        # Therefore we land on the start page of the survey
        self.assertIn("Test session", browser.contents)
        self.assertIn("<h1>Software development</h1>", browser.contents)


class LoginTests(EuphorieFunctionalTestCase):
    def test_login_not_case_sensitive(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password="secret")
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url() + "/@@login")
        browser.getControl(name="__ac_name").value = "JANE@example.com"
        browser.getControl(name="__ac_password:utf8:ustring").value = "secret"
        browser.getControl(name="login").click()
        self.assertTrue("@@login" not in browser.url)

    def test_use_session_cookie_by_default(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password="secret")
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url() + "/@@login")
        browser.getControl(name="__ac_name").value = "jane@example.com"
        browser.getControl(name="__ac_password:utf8:ustring").value = "secret"
        browser.getControl(name="login").click()
        auth_cookie = browser.cookies.getinfo("__ac")
        self.assertEqual(auth_cookie["expires"], None)

    def test_remember_user_sets_cookie_expiration(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password="secret")
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url() + "/@@login")
        browser.getControl(name="__ac_name").value = "jane@example.com"
        browser.getControl(name="__ac_password:utf8:ustring").value = "secret"
        browser.getControl(name="remember").value = True
        browser.getControl(name="login").click()
        auth_cookie = browser.cookies.getinfo("__ac")
        self.assertNotEqual(auth_cookie["expires"], None)
        delta = auth_cookie["expires"] - datetime.datetime.now(
            auth_cookie["expires"].tzinfo
        )
        self.assertTrue(delta.days > 100)

    def test_extra_ga_pageview_post_login(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        addAccount(password="secret")
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url() + "/@@login")
        browser.getControl(name="__ac_name").value = "JANE@example.com"
        browser.getControl(name="__ac_password:utf8:ustring").value = "secret"
        browser.getControl(name="login").click()
        self.assertTrue(
            re.search("trackPageview.*login/success", browser.contents) is not None
        )

    def test_record_last_login_time(self):
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password="secret")
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url() + "/@@login")
        browser.getControl(name="__ac_name").value = "jane@example.com"
        browser.getControl(name="__ac_password:utf8:ustring").value = "secret"
        browser.getControl(name="login").click()
        last_login = Session().query(account.__class__).one().last_login
        delta = datetime.datetime.now(last_login.tzinfo) - last_login
        self.assertAlmostEqual(delta.seconds / 10, 0)


class RegisterTests(EuphorieIntegrationTestCase):
    def test_lowercase_email(self):
        with self._get_view("login", self.portal.client) as view:
            view.errors = {}
            view.request.form["email"] = "JANE@example.com"
            view.request.form["password1"] = "Secret123Secret"
            view.request.form["password2"] = "Secret123Secret"
            view.request.form["terms"] = "on"
            account = view._tryRegistration()
            self.assertEqual(account.loginname, "jane@example.com")

    def test_first_name_last_name(self):
        with self._get_view("login", self.portal.client) as view:
            view.errors = {}
            view.request.form["first_name"] = "Jane"
            view.request.form["last_name"] = "Doe"
            view.request.form["email"] = "JANE@example.com"
            view.request.form["password1"] = "Secret123Secret"
            view.request.form["password2"] = "Secret123Secret"
            view.request.form["terms"] = "on"
            account = view._tryRegistration()
            self.assertEqual(account.loginname, "jane@example.com")
            self.assertEqual(account.first_name, "Jane")
            self.assertEqual(account.last_name, "Doe")

    def test_conflict_with_plone_account(self):
        with self._get_view("login", self.portal.client) as view:
            view.errors = {}
            view.request.form["email"] = self.portal._owner[1]
            view.request.form["password1"] = "Secret123Secret"
            view.request.form["password2"] = "Secret123Secret"
            view.request.form["terms"] = "on"
            self.assertEqual(view._tryRegistration(), False)
            self.assertTrue("email" in view.errors)

    def test_basic_email_verification(self):
        with self._get_view("login", self.portal.client) as view:
            view.errors = {}
            view.request.form["email"] = "wichert"
            view.request.form["password1"] = "Secret123Secret"
            view.request.form["password2"] = "Secret123Secret"
            view.request.form["terms"] = "on"
            self.assertEqual(view._tryRegistration(), False)
            self.assertTrue("email" in view.errors)

            view.errors.clear()
            view.request.form["email"] = "wichert@wiggy net"
            self.assertEqual(view._tryRegistration(), False)
            self.assertTrue("email" in view.errors)

            view.errors.clear()
            view.request.form["email"] = "wichert@wiggy.net"
            self.assertNotEqual(view._tryRegistration(), False)

    def test_terms_not_accepted(self):
        with self._get_view("login", self.portal.client) as view:
            view.errors = {}
            view.request.form["email"] = self.portal._owner[1]
            view.request.form["password1"] = "Secret123Secret"
            view.request.form["password2"] = "Secret123Secret"
            self.assertEqual(view._tryRegistration(), False)
            self.assertTrue("terms" in view.errors)

    def test_registration_not_allowed(self):
        registry = getUtility(IRegistry)
        security_settings = registry.forInterface(ISecuritySchema, prefix="plone")
        security_settings.enable_self_reg = False
        with self._get_view("login", self.portal.client) as view:
            view.errors = {}
            view.request.form["email"] = "jane@example.com"
            view.request.form["password1"] = "Secret123Secret"
            view.request.form["password2"] = "Secret123Secret"
            view.request.form["terms"] = "on"
            with self.assertRaises(Unauthorized):
                view._tryRegistration()


class ResetPasswordTests(EuphorieFunctionalTestCase):
    def add_dummy_survey(self):
        survey = """<sector xmlns="http://xml.simplon.biz/euphorie/survey/1.0">
                      <title>Sector title</title>
                      <survey>
                        <title>Survey title</title>
                      </survey>
                    </sector>"""
        self.loginAsPortalOwner()
        addSurvey(self.portal, survey)
        self.logout()

    def test_unknown_account(self):
        self.add_dummy_survey()
        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()

        # We do not have any account here
        self.assertListEqual(model.Session.query(model.Account).all(), [])
        # Even if the user does not exist, the form submission
        # will be successfully sent
        self.assertTrue(
            browser.url.startswith("http://nohost/plone/client/nl/@@login?came_from")
        )

    def test_invalid_email(self):
        self.add_dummy_survey()
        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        # Test an invalid email address
        browser.getControl(name="form.widgets.email").value = "jane @ joe.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertIn("The specified email is not valid.", browser.contents)
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/@@reset_password_request",
        )

    def test_email(self):
        self.add_dummy_survey()
        addAccount()
        mail_fixture = MockMailFixture()
        browser = self.get_browser()
        browser.open(self.portal.client.nl.absolute_url() + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(len(mail_fixture.storage), 1)
        (args, kw) = mail_fixture.storage[0]
        (mail, mto, mfrom) = args[:3]
        self.assertEqual(mfrom, "discard@simplon.biz")
        self.assertEqual(mto, "jane@example.com")
        self.assertEqual(
            str(mail["Subject"]),
            "OiRA password reset instructions",
        )
        body = (
            mail.get_payload(0)
            .get_payload(decode=True)
            .decode(mail.get_content_charset("utf-8"))
        )
        self.assertTrue("/passwordreset/" in body)

    def test_invalid_reset_key(self):
        """When the request key is invalid the user is invited to request a new
        key."""
        self.add_dummy_survey()
        browser = self.get_browser()
        for url in (
            self.portal.client.nl.absolute_url() + "/passwordreset",
            self.portal.client.nl.absolute_url() + "/passwordreset/foo",
        ):
            browser.open(url)
            browser.getControl(name="form.widgets.new_password").value = (
                "Secret123Secret"
            )
            browser.getControl(name="form.widgets.new_password_confirmation").value = (
                "Secret123Secret"
            )
            browser.getControl(label="Save changes").click()
            self.assertIn("Invalid security token", browser.contents)

    def test_token_invalid_after_use(self):
        self.add_dummy_survey()
        addAccount()
        mail_fixture = MockMailFixture()

        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()

        args = mail_fixture.storage[0][0]
        mail = args[0]
        mail_text = "".join(
            [
                (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset("iso-8859-1")
                )
                for part in mail.walk()
            ]
        )

        reset_url = re.search("http.*passwordreset/\\S*", mail_text).group(0)
        browser.open(reset_url)
        browser.getControl(name="form.widgets.new_password").value = "Test12345678"
        browser.getControl(name="form.widgets.new_password_confirmation").value = (
            "Test12345678"
        )
        browser.getControl(name="form.buttons.save").click()

        self.assertIn("success", browser.contents)

        # Token has been used already - second time should fail
        browser.open(reset_url)
        self.assertIn("Invalid security token", browser.contents)

        # You're free to fill in the form but it won't work
        browser.getControl(name="form.widgets.new_password").value = "Test12345670"
        browser.getControl(name="form.widgets.new_password_confirmation").value = (
            "Test12345670"
        )
        browser.getControl(name="form.buttons.save").click()

        self.assertNotIn("success", browser.contents)

    def test_token_invalid_after_new_request(self):
        self.add_dummy_survey()
        addAccount()
        mail_fixture = MockMailFixture()

        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()

        # Request another password reset without using the first one

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()

        args = mail_fixture.storage[0][0]
        mail = args[0]
        mail_text = "".join(
            [
                (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset("iso-8859-1")
                )
                for part in mail.walk()
            ]
        )

        # Now try using the first token
        reset_url = re.search("http.*passwordreset/\\S*", mail_text).group(0)
        browser.open(reset_url)
        self.assertIn("Invalid security token", browser.contents)

        # You're free to fill in the form but it won't work
        browser.getControl(name="form.widgets.new_password").value = "Test12345678"
        browser.getControl(name="form.widgets.new_password_confirmation").value = (
            "Test12345678"
        )
        browser.getControl(name="form.buttons.save").click()

        self.assertNotIn("success", browser.contents)

    def test_token_expired(self):
        self.add_dummy_survey()
        addAccount()
        mail_fixture = MockMailFixture()

        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()

        args = mail_fixture.storage[0][0]
        mail = args[0]
        mail_text = "".join(
            [
                (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset("iso-8859-1")
                )
                for part in mail.walk()
            ]
        )
        token = re.search("passwordreset/(\\S*)", mail_text).group(1)
        # fake that the token has expired
        ppr = api.portal.get_tool("portal_password_reset")
        ppr._requests[token] = (ppr._requests[token][0], datetime.datetime(2001, 1, 1))
        ppr._p_changed = 1
        transaction.commit()

        reset_url = re.search("http.*passwordreset/\\S*", mail_text).group(0)
        browser.open(reset_url)
        self.assertIn("Invalid security token", browser.contents)

        # You're free to fill in the form but it won't work

        browser.getControl(name="form.widgets.new_password").value = "Test12345678"
        browser.getControl(name="form.widgets.new_password_confirmation").value = (
            "Test12345678"
        )
        browser.getControl(name="form.buttons.save").click()

        self.assertNotIn("success", browser.contents)
        self.assertIn("Invalid security token", browser.contents)

    def test_token_expires_after_12_hours(self):
        self.add_dummy_survey()
        addAccount()
        mail_fixture = MockMailFixture()

        browser = self.get_browser()
        url = self.portal.client.nl.absolute_url()

        browser.open(url + "/@@login")
        browser.getLink("I forgot my password").click()
        browser.getControl(name="form.widgets.email").value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()

        args = mail_fixture.storage[0][0]
        mail = args[0]
        mail_text = "".join(
            [
                (part.get_payload(decode=True) or b"").decode(
                    part.get_content_charset("iso-8859-1")
                )
                for part in mail.walk()
            ]
        )
        token = re.search("passwordreset/(\\S*)", mail_text).group(1)
        ppr = api.portal.get_tool("portal_password_reset")
        _, expiry = ppr._requests[token]
        self.assertLessEqual(
            expiry, datetime.datetime.now() + datetime.timedelta(hours=12)
        )
