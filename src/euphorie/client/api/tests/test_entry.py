# coding=utf-8
from euphorie.client.api.entry import API
from euphorie.client.api.users import Users
from euphorie.testing import EuphorieFunctionalTestCase

import json
import unittest


class APITests(unittest.TestCase):

    def test_get_known_entrypoint(self):
        api = API('api', 'request')
        api.entry_points = {'known': Users}
        child = api['known']
        self.assertTrue(isinstance(child, Users))
        self.assertEqual(child.request, 'request')
        self.assertEqual(child.getId(), 'known')


class BrowserAPITests(EuphorieFunctionalTestCase):

    def test_get_version(self):
        browser = self.get_browser()
        browser.open('http://nohost/plone/client/api')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
            set(response), set(['api-version', 'euphorie-version'])
        )
        self.assertEqual(response['api-version'], [1, 0])
