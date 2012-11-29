import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class APITests(unittest.TestCase):
    def API(self, *a, **kw):
        from ..entry import API
        return API(*a, **kw)


class BrowserAPITests(EuphorieFunctionalTestCase):
    def test_get_version(self):
        import json
        browser = Browser()
        browser.open('http://nohost/plone/api')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['api-version', 'euphorie-version']))
        self.assertEqual(response['api-version'], [1, 0])
