from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class NotFoundViewTests(EuphorieFunctionalTestCase):
    def test_404_handled(self):
        import json
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/client/api/bad')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['type', 'message']))
        self.assertEqual(response['type'], 'error')
