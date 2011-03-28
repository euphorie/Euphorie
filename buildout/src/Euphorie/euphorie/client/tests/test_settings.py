from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase


class AccountSettingsTests(EuphorieFunctionalTestCase):
    def setUp(self):
        from Products.Five.testbrowser import Browser
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import registerUserInClient
        from euphorie.content.tests.utils import BASIC_SURVEY
        super(AccountSettingsTests, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey=self.portal.client["nl"]["ict"]["software-development"]
        self.browser=Browser()
        self.browser.open(survey.absolute_url())
        registerUserInClient(self.browser)

    def testWrongOldPassword(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value="wrong"
        browser.getControl(name="form.widgets.new_password").value="secret"
        browser.getControl(name="form.widgets.new_password.confirm").value="secret"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-settings")
        self.assertTrue("Invalid password" in browser.contents)

    def testNoNewPassword(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value="guest"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-settings")
        self.assertTrue("There were no changes to be saved." in browser.contents)

    def testPasswordMismatch(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value="guest"
        browser.getControl(name="form.widgets.new_password").value="secret"
        browser.getControl(name="form.widgets.new_password.confirm").value="secret2"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-settings")
        self.assertTrue("Password doesn't compare with confirmation value" in browser.contents)

    def testUpdatePassword(self):
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/account-settings")
        browser.getControl(name="form.widgets.old_password").value="guest"
        browser.getControl(name="form.widgets.new_password").value="secret"
        browser.getControl(name="form.widgets.new_password.confirm").value="secret"
        browser.handleErrors=False
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-settings")
        account=Session.query(Account).first()
        self.assertEqual(account.password, "secret")

