# coding=utf-8
from Acquisition import aq_parent
from euphorie.content.tests.utils import createSector
from euphorie.testing import EuphorieIntegrationTestCase


class CountryTests(EuphorieIntegrationTestCase):
    def createCountry(self):
        sector = createSector(self.portal, login="sector")
        return aq_parent(sector)

    def testCanNotBeCopied(self):
        country = self.createCountry()
        self.assertFalse(country.cb_isCopyable())

    def testDefaultInfoSections(self):
        country = self.createCountry()
        self.assertEqual(
            country.risk_default_collapsible_sections, ["collapsible_section_information"]
        )
