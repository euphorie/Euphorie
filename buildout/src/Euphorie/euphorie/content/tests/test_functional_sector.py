from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.CMFCore.utils import _checkPermission


class SectorTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        country=self.portal.sectors.nl
        sector=self._create(country, "euphorie.sector", "sector")
        return sector

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types=[fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.sector" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        sector=self.createSector()
        types=[fti.id for fti in sector.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.surveygroup"]))

    def testCanNotBeCopied(self):
        self.loginAsPortalOwner()
        sector=self.createSector()
        self.assertFalse(sector.cb_isCopyable())



class SectorAsUserTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        country=self.portal.sectors.nl
        sector=self._create(country, "euphorie.sector", "sector")
        sector.login="sector"
        sector.indexObject()
        return sector

    def testGetUser(self):
        self.loginAsPortalOwner()
        self.createSector()
        account=self.portal.acl_users.getUser("sector")
        self.assertTrue(account.getUserId())
        self.assertEqual(account.getUserName(), "sector")

    def testGetUserById(self):
        from plone.uuid.interfaces import IUUID
        self.loginAsPortalOwner()
        sector=self.createSector()
        uid=IUUID(sector)
        account=self.portal.acl_users.getUserById(uid)
        self.assertEqual(account.getUserId(), uid)
        self.assertEqual(account.getUserName(), "sector")

    def testGetUserProperties(self):
        self.loginAsPortalOwner()
        sector=self.createSector()
        sector.title=u"This is a sector"
        sector.contact_email=u"sector@example.com"
        account=self.portal.acl_users.getUser("sector")
        self.assertEqual(account.getProperty("fullname"), "This is a sector")
        self.assertEqual(account.getProperty("email"), "sector@example.com")

    def testSetProperties(self):
        self.loginAsPortalOwner()
        sector=self.createSector()
        sector.title=u"This is a sector"
        account=self.portal.acl_users.getUser("sector")
        account.setProperties(fullname=u"My New Name")
        self.assertEqual(sector.title, u"My New Name")

    def testResetPassword(self):
        # Test for part of http://code.simplon.biz/tracker/tno-euphorie/ticket/111
        from euphorie.content.user import UserAuthentication
        self.loginAsPortalOwner()
        sector=self.createSector()
        sector.title=u"This is a sector"
        pas=self.portal.acl_users
        auth=UserAuthentication(sector)
        self.assertEqual(auth.authenticateCredentials(dict(password="s3cr3t")), None)
        pas.userSetPassword(auth.getUserId(), "s3cr3t")
        self.assertEqual(
                auth.authenticateCredentials(dict(password="s3cr3t")), 
                (auth.getUserId(), auth.getUserName()))




class SectorBrowserTests(EuphorieFunctionalTestCase):
    def testDuplicateLoginNotAllowed(self):
        # Test for http://code.simplon.biz/tracker/euphorie/ticket/152
        from euphorie.content.tests.utils import createSector
        createSector(self.portal, login="sector")
        browser=self.adminBrowser()
        browser.open("%s/sectors/nl/@@manage-users" % self.portal.absolute_url())
        browser.getLink("Add new sector").click()
        browser.getControl(name="form.widgets.title").value="New sector"
        browser.getControl(name="form.widgets.login").value="sector"
        browser.getControl(name="form.widgets.password").value="secret"
        browser.getControl(name="form.widgets.password.confirm").value="secret"
        browser.getControl(name="form.widgets.contact_name").value="John Doe"
        browser.getControl(name="form.widgets.contact_email").value="john@example.com"
        browser.getControl(name="form.buttons.save").click()
        self.assertTrue("This login name is already taken" in browser.contents)




class PermissionTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        country=self.portal.sectors.nl
        sector=self._create(country, "euphorie.sector", "sector")
        sector.login="sector"
        sector.indexObject()
        return sector

    def testSectorWorkflowUsed(self):
        self.setRoles(["Manager"])
        sector=self.createSector()
        wt=self.portal.portal_workflow
        self.assertEqual(wt.getChainFor(sector), ("sector",))
        self.assertEqual(wt.getInfoFor(sector, "review_state"), "hidden")

    def testAnonymous(self):
        self.setRoles(["Manager"])
        sector=self.createSector()
        self.logout()
        self.failUnless(not _checkPermission("Euphorie: Add new RIE Content", sector))
        self.failUnless(not _checkPermission("Access contents information", sector))
        self.failUnless(not _checkPermission("Change portal events", sector))
        self.failUnless(not _checkPermission("Modify portal content", sector))
        self.failUnless(not _checkPermission("View", sector))

    def testSector(self):
        from plone.uuid.interfaces import IUUID
        self.setRoles(["Manager"])
        sector=self.createSector()
        self.login(IUUID(sector))
        self.failUnless(_checkPermission("Euphorie: Add new RIE Content", sector))
        self.failUnless(_checkPermission("Access contents information", sector))
        self.failUnless(_checkPermission("Change portal events", sector))
        self.failUnless(_checkPermission("Modify portal content", sector))
        self.failUnless(_checkPermission("View", sector))

    def testCountryManager(self):
        self.setRoles(["Manager"])
        sector=self.createSector()
        self.portal.acl_users._doAddUser("support", "secret", ["CountryManager"], [])
        self.login("support")
        self.failUnless(_checkPermission("Euphorie: Add new RIE Content", sector))
        self.failUnless(_checkPermission("Access contents information", sector))
        self.failUnless(_checkPermission("Change portal events", sector))
        self.failUnless(_checkPermission("Modify portal content", sector))
        self.failUnless(_checkPermission("View", sector))

    def testManager(self):
        self.setRoles(["Manager"])
        sector=self.createSector()
        self.portal.acl_users._doAddUser("manager", "secret", ["Manager"], [])
        self.login("manager")
        self.failUnless(_checkPermission("Euphorie: Add new RIE Content", sector))
        self.failUnless(_checkPermission("Access contents information", sector))
        self.failUnless(_checkPermission("Change portal events", sector))
        self.failUnless(_checkPermission("Modify portal content", sector))
        self.failUnless(_checkPermission("View", sector))

