from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_require_authentication(self):
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries')
        self.assertTrue(browser.headers['Status'].startswith('401'))

    def test_authenticated_user(self):
        import json
        from ...tests.utils import createSector
        from ..authentication import generate_token
        sector = createSector(self.portal, login='sector', password=u'sector')
        browser = Browser()
        browser.handleErrors = False
        browser.addHeader('X-Euphorie-Token', generate_token(sector))
        browser.open('http://nohost/plone/api/countries')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['countries']))
        self.assertGreater(len(response['countries']), 30)
        nl = [c for c in response['countries'] if c['id'] == 'nl'][0]
        self.assertEqual(set(nl), set(['id', 'title', 'country-type']))
        self.assertEqual(nl['id'], u'nl')
        self.assertEqual(nl['title'], u'The Netherlands')
        self.assertEqual(nl['country-type'], u'eu-member')
