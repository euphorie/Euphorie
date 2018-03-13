# coding=utf-8
from euphorie.client.api.users import Authenticate
from euphorie.client.api.users import View
from euphorie.client.model import Account
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from z3c.saconfig import Session

import json
import mock
import unittest


class ViewTests(EuphorieIntegrationTestCase):

    def test_do_POST_valid_data(self):
        view = View(None, self.request.clone())
        view.input = {'login': 'john', 'password': 'jane'}
        with mock.patch(
            'euphorie.client.api.users.generate_token'
        ) as mock_generate_token:
            mock_generate_token.return_value = 'token'
            response = view.do_POST()
        self.assertEqual(response['type'], 'user')


class AuthenticateTests(unittest.TestCase):

    def test_render_no_data_provided(self):
        view = Authenticate(None, mock.Mock())
        view.input = None
        response = view.do_POST()
        self.assertEqual(response['type'], 'error')

    def test_render_missing_data(self):
        view = Authenticate(None, mock.Mock())
        view.input = {'login': 'foo'}
        response = view.do_POST()
        self.assertEqual(response['type'], 'error')

    def test_render_bad_login(self):
        request = mock.Mock()
        view = Authenticate(None, request)
        view.input = {'login': 'foo', 'password': 'bar'}
        with mock.patch('euphorie.client.api.users.authenticate') as mock_auth:
            mock_auth.return_value = None
            response = view.do_POST()
            mock_auth.assert_called_once_with('foo', 'bar')
            self.assertEqual(response['type'], 'error')
            self.assertEqual(response['message'], 'Invalid credentials')
            request.response.setStatus.assert_called_once_with(403)


class AuthenticateIntegrationTests(EuphorieIntegrationTestCase):

    def test_render_valid_login(self):
        view = Authenticate(None, self.request.clone())
        view.input = {'login': 'foo', 'password': 'bar'}
        with mock.patch('euphorie.client.api.users.authenticate') as mock_auth:
            with mock.patch(
                'euphorie.client.api.users.generate_token'
            ) as mock_generate_token:
                with mock.patch('euphorie.client.api.users.user_info') as info:
                    view.sessions = mock.Mock(return_value='sessions')
                    info.return_value = {'foo': 'bar'}
                    mock_auth.return_value = account = mock.Mock()
                    mock_generate_token.return_value = 'auth-token'
                    response = view.do_POST()
                    mock_auth.assert_called_once_with('foo', 'bar')
                    info.assert_called_once_with(account, view.request)
                    self.assertEqual(response['foo'], 'bar')
                    self.assertEqual(response['token'], 'auth-token')


class AuthenticateBrowserTests(EuphorieFunctionalTestCase):

    def test_authentication_failure(self):
        browser = self.get_browser()
        browser.raiseHttpErrors = False
        browser.post(
            'http://nohost/plone/client/api/users/authenticate',
            '{"login": "jane", "password": "john"}'
        )
        self.assertTrue(browser.headers['Status'].startswith('403'))
        self.assertEqual(browser.headers['Content-Type'], 'application/json')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'error')

    def test_authentication_success(self):
        Session.add(Account(loginname='john', password=u'jane'))
        browser = self.get_browser()
        browser.handleErrors = False
        browser.post(
            'http://nohost/plone/client/api/users/authenticate',
            '{"login": "john", "password": "jane"}'
        )
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'user')
