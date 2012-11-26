from euphorie.deployment.tests.functional import EuphorieTestCase


class CountryTests(EuphorieTestCase):
    def createCountry(self):
        from Acquisition import aq_parent
        from euphorie.content.tests.utils import createSector
        sector = createSector(self.portal, login="sector")
        return aq_parent(sector)

    def testCanNotBeCopied(self):
        self.loginAsPortalOwner()
        country = self.createCountry()
        self.assertFalse(country.cb_isCopyable())
