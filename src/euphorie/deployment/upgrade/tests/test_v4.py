from euphorie.deployment.tests.functional import EuphorieTestCase

class add_client_api_tests(EuphorieTestCase):
    def add_client_api(self):
        from euphorie.deployment.upgrade.v4 import add_client_api
        add_client_api(self.portal.portal_setup)

    def test_api_already_exists(self):
        self.add_client_api()

    def test_missing(self):
        del self.portal.client['api']
        self.add_client_api()
        self.assertTrue('api' in self.portal.client)
