import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.user import View
        return View(*a, **kw)

    def test_sessions_no_sessions(self):
        import mock
        account = mock.Mock()
        account.sessions = []
        view = self.View(account, None)
        self.assertEqual(view.sessions(), [])

    def test_sessions_with_session(self):
        import datetime
        import mock
        account = mock.Mock()
        session = mock.Mock()
        session.id = 13
        session.title = u'This is my title'
        session.modified = datetime.datetime(2012, 4, 20, 16, 5, 23)
        account.sessions = [session]
        view = self.View(account, None)
        self.assertEqual(
                view.sessions(),
                [{'id': 13,
                  'title': u'This is my title',
                  'modified': '2012-04-20T16:05:23'}])


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_user_info(self):
        import json
        from z3c.saconfig import Session
        from euphorie.client.model import Account
        Session.add(Account(loginname='john', password=u'jane'))
        browser = Browser()
        browser.handleErrors = False
        browser.open('http://nohost/plone/client/api/users/1')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'user')
