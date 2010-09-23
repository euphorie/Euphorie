import unittest
from euphorie.content.tests.functional import EuphorieContentTestCase
from Products.CMFCore.utils import _checkPermission


class SectorTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
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


class SectorAsUserTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
        sector=self._create(country, "euphorie.sector", "sector")
        return sector

    def testGetUser(self):
        self.loginAsPortalOwner()
        self.createSector()
        account=self.portal.acl_users.getUserById("sector")
        self.assertEqual(account.getUserId(), "sector")
        self.assertEqual(account.getUserName(), "sector")

    def testGetUserProperties(self):
        self.loginAsPortalOwner()
        sector=self.createSector()
        sector.title=u"This is a sector"
        sector.contact_email=u"sector@example.com"
        account=self.portal.acl_users.getUserById("sector")
        self.assertEqual(account.getProperty("fullname"), "This is a sector")
        self.assertEqual(account.getProperty("email"), "sector@example.com")

    def testSetPropertes(self):
        self.loginAsPortalOwner()
        sector=self.createSector()
        sector.title=u"This is a sector"
        account=self.portal.acl_users.getUserById("sector")
        account.setProperties(fullname=u"My New Name")
        self.assertEqual(sector.title, u"My New Name")



class PermissionTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSector(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
        sector=self._create(country, "euphorie.sector", "sector")
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
        self.setRoles(["Manager"])
        sector=self.createSector()
        self.login("sector")
        self.failUnless(_checkPermission("Euphorie: Add new RIE Content", sector))
        self.failUnless(_checkPermission("Access contents information", sector))
        self.failUnless(_checkPermission("Change portal events", sector))
        self.failUnless(_checkPermission("Modify portal content", sector))
        self.failUnless(_checkPermission("View", sector))

    def testSupport(self):
        self.setRoles(["Manager"])
        sector=self.createSector()
        self.portal.acl_users._doAddUser("support", "secret", ["Support"], [])
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



def test_suite():
        return unittest.defaultTestLoader.loadTestsFromName(__name__)


