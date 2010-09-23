from euphorie.deployment.tests.functional import EuphorieTestCase

class CountryManagerTests(EuphorieTestCase):
    def createCountryManager(self):
        from euphorie.content.tests.utils import _create
        manager=_create(self.portal.sectors["nl"], "euphorie.countrymanager", "mgr")
        return manager

    def testCanNotBeCopied(self):
        self.loginAsPortalOwner()
        manager=self.createCountryManager()
        self.assertFalse(manager.cb_isCopyable())


