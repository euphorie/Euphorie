from euphorie.testing import EuphorieIntegrationTestCase
from zope.component import getMultiAdapter


class TestSitemenu(EuphorieIntegrationTestCase):
    def test_sitemenu_items_sectors_overview(self):
        """Test, if the site menu contains the expected items."""
        self.loginAsPortalOwner()

        sitemenu = getMultiAdapter((self.portal.sectors, self.request), name="sitemenu")

        menu = sitemenu.actions

        self.assertEqual(menu["title"], "menu_actions")
        self.assertEqual(len(menu["children"]), 2)
        self.assertEqual(menu["children"][0]["title"], "menu_add_new")
        self.assertEqual(menu["children"][1]["title"], "menu_organise")

    def test_sitemenu_items_country(self):
        """Test, if the site menu contains the expected items including the
        country menu on an ICountry context."""
        self.loginAsPortalOwner()

        sitemenu = getMultiAdapter(
            (self.portal.sectors.nl, self.request), name="sitemenu"
        )

        menu = sitemenu.actions

        self.assertEqual(menu["title"], "menu_actions")
        self.assertEqual(len(menu["children"]), 3)
        self.assertEqual(menu["children"][0]["title"], "menu_add_new")
        self.assertEqual(menu["children"][1]["title"], "menu_organise")
        self.assertEqual(menu["children"][2]["title"], "menu_admin")
        self.assertEqual(len(menu["children"][2]["children"]), 1)
        self.assertEqual(
            menu["children"][2]["children"][0]["title"], "menu_country_tools"
        )

    def test_country_menu_availability(self):
        """Test, if the country menu is available in different contexts."""
        sitemenu = getMultiAdapter(
            (self.portal.sectors.nl, self.request), name="sitemenu"
        )
        self.assertIsNotNone(sitemenu.menu_country_tools())

        sitemenu = getMultiAdapter((self.portal.sectors, self.request), name="sitemenu")
        self.assertIsNone(sitemenu.menu_country_tools())

        sitemenu = getMultiAdapter((self.portal, self.request), name="sitemenu")
        self.assertIsNone(sitemenu.menu_country_tools())
