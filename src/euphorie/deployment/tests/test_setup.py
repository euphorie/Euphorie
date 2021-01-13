# coding=utf-8
from euphorie.testing import EuphorieIntegrationTestCase


class SetupTests(EuphorieIntegrationTestCase):
    def testDefaultContenetRemoved(self):
        self.assertTrue("Members" not in self.portal.objectIds())
        self.assertTrue("news" not in self.portal.objectIds())
        self.assertTrue("events" not in self.portal.objectIds())

    def testSectorContainerCreated(self):
        self.assertTrue("sectors" in self.portal.objectIds())
        self.assertEqual(self.portal.sectors.portal_type, "euphorie.sectorcontainer")

    def testCountriesCreated(self):
        self.assertTrue("nl" in self.portal.sectors)
        self.assertEqual(self.portal.sectors["nl"].country_type, "eu-member")

    def testClientCreated(self):
        self.assertTrue("client" in self.portal.objectIds())
        self.assertEqual(self.portal.client.portal_type, "euphorie.client")

    def testClientUserCreated(self):
        user = self.portal.acl_users.getUserById("client")
        self.assertTrue(user is not None)

    def testHideComponentProducts(self):
        qi = self.portal.portal_quickinstaller
        installable = qi.listInstallableProducts(skipInstalled=False)
        installable = set([product["id"] for product in installable])
        self.assertTrue("euphorie.content" not in installable)
        self.assertTrue("euphorie.client" not in installable)

    def testNuPloneEnabled(self):
        st = self.portal.portal_skins
        self.assertEqual(st.getDefaultSkin(), "NuPlone")
