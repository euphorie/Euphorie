from ...tests.utils import createSector
from ..authentication import generate_token
from euphorie.testing import EuphorieFunctionalTestCase

import json


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_require_authentication(self):
        browser = self.get_browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = self.get_browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['countries']))
        self.assertEqual(len(response['countries']), 2)
        nl = [c for c in response['countries'] if c['id'] == 'nl'][0]
        self.assertEqual(set(nl), set(['id', 'title', 'country-type']))
        self.assertEqual(nl['id'], u'nl')
        self.assertEqual(nl['title'], u'The Netherlands')
        self.assertEqual(nl['country-type'], u'eu-member')
