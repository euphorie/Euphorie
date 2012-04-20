import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class APITests(unittest.TestCase):
    def API(self, *a, **kw):
        from euphorie.client.api.entry import API
        return API(*a, **kw)

    def test_get_known_entrypoint(self):
        from euphorie.client.api.users import Users
        api = self.API('api', 'request')
        api.entry_points = {'known': Users}
        child = api['known']
        self.assertTrue(isinstance(child, Users))
        self.assertEqual(child.request, 'request')
        self.assertEqual(child.getId(), 'known')


class BrowserAPITests(EuphorieFunctionalTestCase):
    def test_get_version(self):
        import json
        browser = Browser()
        browser.open('http://nohost/plone/client/api')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['api-version', 'euphorie-version']))
        self.assertEqual(response['api-version'], [1, 0])
