import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewTests(unittest.TestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.account import View
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
        session.created = datetime.datetime(2012, 4, 20, 16, 5, 23)
        session.modified = datetime.datetime(2012, 4, 23, 11, 46, 23)
        account.sessions = [session]
        with mock.patch('euphorie.client.api.account.get_survey'):
            view = self.View(account, None)
            self.assertEqual(
                    view.sessions(),
                    [{'id': 13,
                      'title': u'This is my title',
                      'created': '2012-04-20T16:05:23',
                      'modified': '2012-04-23T11:46:23'}])

    def test_PUT_no_data(self):
        import mock
        account = mock.Mock()
        account.sessions = []
        view = self.View(account, None)
        view.input = {}
        view.PUT()

    def test_PUT_empty_login(self):
        import mock
        account = mock.Mock()
        account.sessions = []
        view = self.View(account, None)
        view.input = {'login': ''}
        self.assertEqual(view.PUT()['type'], 'error')

    def test_PUT_new_login_in_use(self):
        import mock
        account = mock.Mock()
        account.sessions = []
        view = self.View(account, None)
        view.input = {'login': 'jane'}
        with mock.patch('euphorie.client.api.account.login_available') \
                as mock_available:
            mock_available.return_value = False
            self.assertEqual(view.PUT()['type'], 'error')
            mock_available.assert_called_once_with('jane')

    def test_PUT_set_login_to_same_value(self):
        import mock
        account = mock.Mock()
        account.loginname = 'jane'
        account.sessions = []
        view = self.View(account, None)
        view.input = {'login': 'jane'}
        with mock.patch('euphorie.client.api.account.login_available') \
                as mock_available:
            mock_available.return_value = False
            self.assertEqual(view.PUT()['type'], 'user')
            self.assertTrue(not mock_available.called)


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
