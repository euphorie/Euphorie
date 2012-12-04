from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class GenericErrorTests(EuphorieFunctionalTestCase):
    def test_View(self):
        import json
        import mock
        with mock.patch('euphorie.content.api.entry.View.do_GET',
                sideEffect=RuntimeError):
            browser = Browser()
            browser.raiseHttpErrors = False
            browser.open('http://nohost/plone/api')
            self.assertTrue(browser.headers['Status'].startswith('500'))
            response = json.loads(browser.contents)
            self.assertEqual(
                    set(response),
                    set(['type', 'message']))
            self.assertEqual(response['type'], 'error')
            self.assertEqual(response['message'], u'An unknown error occurred.')


class NotFoundViewTests(EuphorieFunctionalTestCase):
    def test_404_handled(self):
        import json
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/unknown')
        self.assertTrue(browser.headers['Status'].startswith('404'))
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['type', 'message']))
        self.assertEqual(response['type'], 'error')
        self.assertEqual(response['message'], 'Unknown resource requested.')


class UnauthorizedViewTests(EuphorieFunctionalTestCase):
    def test_view(self):
        import json
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.open('http://nohost/plone/api/countries')
        self.assertTrue(browser.headers['Status'].startswith('401'))
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(
                set(response),
                set(['type', 'message']))
        self.assertEqual(response['type'], 'error')
        self.assertEqual(response['message'], 'Access denied.')
