from euphorie.deployment.tests.functional import EuphorieTestCase


class add_api_authentication_tests(EuphorieTestCase):
    def add_api_authentication(self):
        from euphorie.deployment.upgrade.v4 import add_api_authentication
        add_api_authentication(self.portal.portal_setup)

    def test_already_configured(self):
        self.add_api_authentication()

    def test_plugin_missing(self):
        self.portal.acl_users.manage_delObjects('euphorie_api')
        self.add_api_authentication()
        self.assertTrue('euphorie_api' in self.portal.acl_users.objectIds())
