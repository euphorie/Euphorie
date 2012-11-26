from euphorie.deployment.tests.functional import EuphorieTestCase


class SetupTests(EuphorieTestCase):
    def testDefaultContenetRemoved(self):
        self.failUnless("Members" not in self.portal.objectIds())
        self.failUnless("news" not in self.portal.objectIds())
        self.failUnless("events" not in self.portal.objectIds())

    def testSectorContainerCreated(self):
        self.failUnless("sectors" in self.portal.objectIds())
        self.assertEqual(
                self.portal.sectors.portal_type, "euphorie.sectorcontainer")

    def testCountriesCreated(self):
        self.assertTrue("nl" in self.portal.sectors)
        self.assertEqual(self.portal.sectors["nl"].country_type, "eu-member")

    def testClientCreated(self):
        self.failUnless("client" in self.portal.objectIds())
        self.assertEqual(self.portal.client.portal_type, "euphorie.client")

    def test_client_api(self):
        client = self.portal.client
        self.assertTrue('api' in client)

    def testClientUserCreated(self):
        user = self.portal.acl_users.getUserById("client")
        self.failUnless(user is not None)

    def testHideComponentProducts(self):
        qi = self.portal.portal_quickinstaller
        installable = qi.listInstallableProducts(skipInstalled=False)
        installable = set([product["id"] for product in installable])
        self.failUnless("euphorie.content" not in installable)
        self.failUnless("euphorie.client" not in installable)

    def testNuPloneEnabled(self):
        st = self.portal.portal_skins
        self.assertEqual(st.getDefaultSkin(), "NuPlone")
