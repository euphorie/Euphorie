# coding=utf-8
from euphorie.client.api.account import View
from euphorie.client.api.authentication import generate_token
from euphorie.client.tests.utils import addAccount
from euphorie.testing import EuphorieFunctionalTestCase

import datetime
import json
import mock
import unittest


class ViewTests(unittest.TestCase):

    def test_sessions_no_sessions(self):
        account = mock.Mock()
        account.sessions = []
        view = View(account, None)
        self.assertEqual(view.sessions(), [])

    def test_sessions_with_session(self):
        account = mock.Mock()
        session = mock.Mock()
        session.id = 13
        session.zodb_path = 'nl/ict/software-development'
        session.title = u'This is my title'
        session.created = datetime.datetime(2012, 4, 20, 16, 5, 23)
        session.modified = datetime.datetime(2012, 4, 23, 11, 46, 23)
        account.sessions = [session]
        with mock.patch('euphorie.client.api.account.get_survey'):
            view = View(account, None)
            self.assertEqual(
                    view.sessions(),
                    [{'id': 13,
                      'survey': 'nl/ict/software-development',
                      'title': u'This is my title',
                      'created': '2012-04-20T16:05:23',
                      'modified': '2012-04-23T11:46:23'}])

    def test_do_PUT_no_data(self):
        account = mock.Mock()
        account.sessions = []
        view = View(account, None)
        view.input = {}
        view.do_PUT()

    def test_do_PUT_empty_login(self):
        account = mock.Mock()
        account.sessions = []
        view = View(account, None)
        view.input = {'login': ''}
        self.assertEqual(view.do_PUT()['type'], 'error')

    def test_do_PUT_new_login_in_use(self):
        account = mock.Mock()
        account.sessions = []
        view = View(account, None)
        view.input = {'login': 'jane'}
        with mock.patch('euphorie.client.api.account.login_available') \
                as mock_available:
            mock_available.return_value = False
            self.assertEqual(view.do_PUT()['type'], 'error')
            mock_available.assert_called_once_with('jane')

    def test_do_PUT_set_login_to_same_value(self):
        account = mock.Mock()
        account.loginname = 'jane'
        account.sessions = []
        view = View(account, None)
        view.input = {'login': 'jane'}
        with mock.patch('euphorie.client.api.account.login_available') \
                as mock_available:
            mock_available.return_value = False
            self.assertEqual(view.do_PUT()['type'], 'user')
            self.assertTrue(not mock_available.called)


class ViewBrowserTests(EuphorieFunctionalTestCase):
    def test_user_info(self):
        account = addAccount()
        browser = self.get_browser()
        browser.addHeader('X-Euphorie-Token', generate_token(account))
        browser.handleErrors = False
        browser.open('http://nohost/plone/client/api/users/1')
        response = json.loads(browser.contents)
        self.assertEqual(response['type'], 'user')
