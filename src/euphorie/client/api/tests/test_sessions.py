from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class BrowserTests(EuphorieFunctionalTestCase):
    def test_no_sessions(self):
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        account = Account(loginname='john', password=u'jane')
        Session.add(account)
        browser = Browser()
        browser.open('http://nohost/plone/client/api/users/1/sessions')
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(['sessions']))
        self.assertEqual(response['sessions'], [])
