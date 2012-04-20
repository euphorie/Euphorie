from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class AuthenticateTests(EuphorieFunctionalTestCase):
    def Authenticate(self, *a, **kw):
        from euphorie.client.api.users import Authenticate
        return Authenticate(*a, **kw)

    def test_browser_authentication_failure(self):
        import json
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.post('http://nohost/plone/client/api/users/authenticate',
                '{"login": "jane", "password": "john"}')
        self.assertTrue(browser.headers['Status'].startswith('403'))
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'error')


    def test_browser_authentication_success(self):
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        Session.add(Account(loginname='john', password=u'jane'))
        browser = Browser()
        browser.handleErrors = False
        browser.post('http://nohost/plone/client/api/users/authenticate',
                '{"login": "john", "password": "jane"}')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'user')
