# coding=utf-8
from euphorie.client.model import Account
from euphorie.client.model import AccountChangeRequest
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import MockMailFixture
from euphorie.client.tests.utils import registerUserInClient
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieFunctionalTestCase
from transaction import commit
from z3c.saconfig import Session

import datetime


class AccountSettingsTests(EuphorieFunctionalTestCase):

    def setUp(self):
        super(AccountSettingsTests, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey = self.portal.client["nl"]["ict"]["software-development"]
        self.browser = self.get_browser()
        self.browser.open(survey.absolute_url())
        registerUserInClient(self.browser)

    def testWrongOldPassword(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value = "wrong"
        browser.getControl(name="form.widgets.new_password").value = "secret"
        browser.getControl(
            name="form.widgets.new_password.confirm"
        ).value = "secret"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/account-settings"
        )
        self.assertTrue("Invalid password" in browser.contents)

    def testNoNewPassword(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value = "guest"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/account-settings"
        )
        self.assertTrue(
            "There were no changes to be saved." in browser.contents
        )

    def testPasswordMismatch(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value = "guest"
        browser.getControl(name="form.widgets.new_password").value = "secret"
        browser.getControl(
            name="form.widgets.new_password.confirm"
        ).value = "secret2"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/account-settings"
        )
        self.assertTrue(
            "Password doesn't compare with confirmation value" in
            browser.contents
        )

    def testUpdatePassword(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value = "guest"
        browser.getControl(name="form.widgets.new_password").value = "secret"
        browser.getControl(
            name="form.widgets.new_password.confirm"
        ).value = "secret"
        browser.handleErrors = False
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url,
            "http://nohost/plone/client/nl/account-settings"
        )
        account = Session.query(Account).first()
        self.assertTrue(account.verify_password("secret"))


class AccountDeleteTests(EuphorieFunctionalTestCase):

    def setUp(self):
        super(AccountDeleteTests, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey = self.portal.client["nl"]["ict"]["software-development"]
        self.browser = self.get_browser()
        self.browser.open(survey.absolute_url())
        registerUserInClient(self.browser)

    def testNoDefaultPassword(self):
        browser = self.browser
        browser.handleErrors = False
        browser.open("http://nohost/plone/client/nl/account-delete")
        self.assertEqual(
            browser.getControl(name="form.widgets.password").value, ""
        )

    def testInvalidPassword(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/account-delete")
        browser.getControl(name="form.widgets.password").value = "secret"
        browser.getControl(name="form.buttons.delete").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/account-delete"
        )
        self.assertTrue("Invalid password" in browser.contents)

    def testDelete(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/account-delete")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(name="form.buttons.delete").click()
        self.assertTrue(
            browser.url.startswith("http://nohost/plone/client/nl"))
        self.assertEqual(Session.query(Account).count(), 0)


class NewEmailTests(EuphorieFunctionalTestCase):

    def setUp(self):
        super(NewEmailTests, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey = self.portal.client["nl"]["ict"]["software-development"]
        self.browser = self.get_browser()
        self.browser.open(survey.absolute_url())
        registerUserInClient(self.browser)
        self._mail_fixture = MockMailFixture()
        self.email_send = self._mail_fixture.storage

    def tearDown(self):
        super(NewEmailTests, self).tearDown()
        del self._mail_fixture

    def testNoDefaultPassword(self):
        browser = self.browser
        browser.handleErrors = False
        browser.open("http://nohost/plone/client/nl/new-email")
        self.assertEqual(
            browser.getControl(name="form.widgets.password").value, ""
        )

    def testNoChange(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/new-email"
        )
        self.assertTrue("Required input is missing." in browser.contents)

    def testInvalidPassword(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(
            name="form.widgets.loginname"
        ).value = "jane@example.com"
        browser.getControl(name="form.widgets.password").value = "secret"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/new-email"
        )
        self.assertTrue("Invalid password" in browser.contents)

    def testInvalidEmail(self):
        browser = self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(name="form.widgets.loginname").value = "one two"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/new-email"
        )
        self.assertTrue("Not a valid email address" in browser.contents)

    def testDuplicateEmail(self):
        browser = self.browser
        Session.add(Account(loginname="jane@example.com", password="secret"))
        commit()
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(
            name="form.widgets.loginname"
        ).value = "jane@example.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/new-email"
        )
        self.assertTrue("address is not available" in browser.contents)

    def testChange(self):
        browser = self.browser
        browser.handleErrors = False
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(
            name="form.widgets.loginname"
        ).value = "discard@simplon.biz"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(
            browser.url, "http://nohost/plone/client/nl/account-settings"
        )
        self.assertTrue("Please confirm your new email" in browser.contents)
        self.assertTrue("discard@simplon.biz" in browser.contents)
        self.assertEqual(Session.query(AccountChangeRequest).count(), 1)

        user = Session.query(Account).first()
        self.assertTrue(user.change_request is not None)
        self.assertEqual(user.change_request.value, "discard@simplon.biz")
        self.assertTrue(
            user.change_request.expires >
            datetime.datetime.now() + datetime.timedelta(days=6)
        )

        self.assertEqual(len(self.email_send), 1)
        parameters = self.email_send[0]
        self.assertEqual(parameters[0][1], "discard@simplon.biz")

    def testSecondChangeResetsKey(self):
        browser = self.browser
        browser.handleErrors = False
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(
            name="form.widgets.loginname"
        ).value = "discard@simplon.biz"
        browser.getControl(name="form.buttons.save").click()
        first_key = Session.query(AccountChangeRequest.id).first()[0]
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(
            name="form.widgets.loginname"
        ).value = "discard@simplon.biz"
        browser.getControl(name="form.buttons.save").click()
        second_key = Session.query(AccountChangeRequest.id).first()[0]
        self.assertNotEqual(first_key, second_key)

    def testLowercaseEmail(self):
        browser = self.browser
        browser.handleErrors = False
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value = "guest"
        browser.getControl(
            name="form.widgets.loginname"
        ).value = "DISCARD@sImplOn.biz"
        browser.getControl(name="form.buttons.save").click()
        request = Session.query(AccountChangeRequest).first()
        self.assertEqual(request.value, 'discard@simplon.biz')


class ChangeEmailTests(EuphorieFunctionalTestCase):

    def testMissingKey(self):
        browser = self.get_browser()
        browser.open("http://nohost/plone/client/confirm-change")

    def testUnkownKey(self):
        browser = self.get_browser()
        browser.open("http://nohost/plone/client/confirm-change?key=bad")

    def testValidKey(self):
        account = Account(loginname="login", password="secret")
        account.change_request = AccountChangeRequest(
            id="X" * 16,
            value="new-login",
            expires=datetime.datetime.now() + datetime.timedelta(1)
        )
        Session.add(account)
        Session.flush()
        browser = self.get_browser()
        browser.open(
            "http://nohost/plone/client/confirm-change?key=XXXXXXXXXXXXXXXX"
        )
        self.assertEqual(browser.url, "http://nohost/plone/client")
        self.assertEqual(
            Session.query(Account.loginname).first()[0], "new-login"
        )
