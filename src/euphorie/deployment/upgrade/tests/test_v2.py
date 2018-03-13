from euphorie.testing import EuphorieFunctionalTestCase


class addCountryGroupingTests(EuphorieFunctionalTestCase):
    def addCountryGrouping(self):
        from euphorie.deployment.upgrade.v2 import addCountryGrouping
        addCountryGrouping(self.portal.portal_setup)

    def testKeepWrongType(self):
        self.portal.sectors["nl"].country_type = "region"
        self.addCountryGrouping()
        self.assertEqual(self.portal.sectors["nl"].country_type, "region")

    def testSetMissingType(self):
        del self.portal.sectors["nl"].country_type
        self.addCountryGrouping()
        self.assertEqual(self.portal.sectors["nl"].country_type, "eu-member")
