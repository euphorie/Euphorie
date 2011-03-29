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



class AccountDeleteTests(EuphorieFunctionalTestCase):
    def setUp(self):
        from Products.Five.testbrowser import Browser
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import registerUserInClient
        from euphorie.content.tests.utils import BASIC_SURVEY
        super(AccountDeleteTests, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey=self.portal.client["nl"]["ict"]["software-development"]
        self.browser=Browser()
        self.browser.open(survey.absolute_url())
        registerUserInClient(self.browser)

    def testNoDefaultPassword(self):
        browser=self.browser
        browser.handleErrors=False
        browser.open("http://nohost/plone/client/nl/account-delete")
        self.assertEqual(
            browser.getControl(name="form.widgets.password").value, "")

    def testInvalidPassword(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/account-delete")
        browser.getControl(name="form.widgets.password").value="secret"
        browser.getControl("Delete account").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-delete")
        self.assertTrue("Invalid password" in browser.contents)

    def testDelete(self):
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/account-delete")
        browser.getControl(name="form.widgets.password").value="guest"
        browser.getControl("Delete account").click()
        self.assertEqual(browser.url, "http://nohost/plone/client")
        self.assertEqual(Session.query(Account).count(), 0)



class NewEmailTests(EuphorieFunctionalTestCase):
    def setUp(self):
        from Products.Five.testbrowser import Browser
        from euphorie.client.tests.utils import addSurvey
        from euphorie.client.tests.utils import registerUserInClient
        from euphorie.content.tests.utils import BASIC_SURVEY
        super(NewEmailTests, self).setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        survey=self.portal.client["nl"]["ict"]["software-development"]
        self.browser=Browser()
        self.browser.open(survey.absolute_url())
        registerUserInClient(self.browser)

    def testNoDefaultPassword(self):
        browser=self.browser
        browser.handleErrors=False
        browser.open("http://nohost/plone/client/nl/new-email")
        self.assertEqual(
            browser.getControl(name="form.widgets.password").value, "")

    def testNoChange(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value="guest"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-settings")
        self.assertTrue("There were no changes to be saved." in browser.contents)

    def testInvalidPassword(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value="secret"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/new-email")
        self.assertTrue("Invalid password" in browser.contents)

    def testInvalidEmail(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value="guest"
        browser.getControl(name="form.widgets.loginname").value="one two"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/new-email")
        self.assertTrue("Not a valid RFC822 email address" in browser.contents)

    def testChange(self):
        browser=self.browser
        browser.open("http://nohost/plone/client/nl/new-email")
        browser.getControl(name="form.widgets.password").value="guest"
        browser.getControl(name="form.widgets.loginname").value="discard@simplon.biz"
        browser.getControl("Save changes").click()
        self.assertEqual(browser.url, "http://nohost/plone/client/nl/account-settings")
        self.assertTrue("Please confirm your new email" in browser.contents)
        self.assertTrue("discard@simplon.biz" in browser.contents)
