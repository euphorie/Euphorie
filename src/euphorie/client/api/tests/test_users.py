import unittest
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase
from Products.Five.testbrowser import Browser


class ViewTests(EuphorieFunctionalTestCase):
    def View(self, *a, **kw):
        from euphorie.client.api.users import View
        return View(*a, **kw)

    def test_do_POST_valid_data(self):
        import mock
        view = self.View(None, None)
        view.input = {'login': 'john', 'password': 'jane'}
        with mock.patch('euphorie.client.api.users.generate_token') \
                as mock_generate_token:
            mock_generate_token.return_value = 'token'
            response = view.do_POST()
        self.assertEqual(response['type'], 'user')


class AuthenticateTests(unittest.TestCase):
    def Authenticate(self, *a, **kw):
        from euphorie.client.api.users import Authenticate
        return Authenticate(*a, **kw)

    def test_render_no_data_provided(self):
        import mock
        view = self.Authenticate(None, mock.Mock())
        view.input = None
        response = view.do_POST()
        self.assertEqual(response['type'], 'error')

    def test_render_missing_data(self):
        import mock
        view = self.Authenticate(None, mock.Mock())
        view.input = {'login': 'foo'}
        response = view.do_POST()
        self.assertEqual(response['type'], 'error')

    def test_render_bad_login(self):
        import mock
        request = mock.Mock()
        view = self.Authenticate(None, request)
        view.input = {'login': 'foo', 'password': 'bar'}
        with mock.patch('euphorie.client.api.users.authenticate') as mock_auth:
            mock_auth.return_value = None
            response = view.do_POST()
            mock_auth.assert_called_once_with('foo', 'bar')
            self.assertEqual(response['type'], 'error')
            self.assertEqual(response['message'], 'Invalid credentials')
            request.response.setStatus.assert_called_once_with(403)

    def test_render_valid_login(self):
        import mock
        view = self.Authenticate(None, None)
        view.input = {'login': 'foo', 'password': 'bar'}
        with mock.patch('euphorie.client.api.users.authenticate') as mock_auth:
            with mock.patch('euphorie.client.api.users.generate_token') \
                    as mock_generate_token:
                with mock.patch('euphorie.client.api.users.user_info') as info:
                    view.sessions = mock.Mock(return_value='sessions')
                    info.return_value = {'foo': 'bar'}
                    mock_auth.return_value = account = mock.Mock()
                    mock_generate_token.return_value = 'auth-token'
                    response = view.do_POST()
                    mock_auth.assert_called_once_with('foo', 'bar')
                    info.assert_called_once_with(account, None)
                    self.assertEqual(response['foo'], 'bar')
                    self.assertEqual(response['token'], 'auth-token')


class AuthenticateBrowserTests(EuphorieFunctionalTestCase):
    def test_authentication_failure(self):
        import json
        browser = Browser()
        browser.raiseHttpErrors = False
        browser.post('http://nohost/plone/client/api/users/authenticate',
                '{"login": "jane", "password": "john"}')
        self.assertTrue(browser.headers['Status'].startswith('403'))
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'error')

    def test_authentication_success(self):
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
