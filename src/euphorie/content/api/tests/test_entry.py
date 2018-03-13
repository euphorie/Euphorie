# coding=utf-8
from ...tests.utils import createSector
from ..authentication import generate_token
from euphorie.testing import EuphorieFunctionalTestCase

import json


class BrowserAPITests(EuphorieFunctionalTestCase):

    def test_get_version(self):
        browser = self.get_browser()
        browser.open('http://nohost/plone/api')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
            set(response), set(['api-version', 'euphorie-version', 'account'])
        )
        self.assertEqual(response['api-version'], [1, 0])
        self.assertEqual(response['account'], None)

    def test_authenticated_user(self):
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api')
        response = json.loads(browser.contents)
        self.assertEqual(response['account'], 'sector')
