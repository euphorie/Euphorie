# coding=utf-8
from euphorie.client.api.authentication import authenticate_token
from euphorie.client.api.authentication import generate_token
from euphorie.client.model import Account
from euphorie.client.tests.database import DatabaseTests
from euphorie.client.tests.utils import addAccount
from plone.keyring.interfaces import IKeyManager

import mock
import unittest


class generate_token_tests(unittest.TestCase):

    def generate_token(self, *a, **kw):
        return generate_token(*a, **kw)

    def test_token_depends_on_login(self):
        with mock.patch('euphorie.client.api.authentication.getUtility') \
                as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = 'secret'
            self.assertNotEqual(
                self.generate_token(Account(id=5, loginname='john')),
                self.generate_token(Account(id=5, loginname='jane'))
            )

    def test_token_depends_on_password(self):
        with mock.patch('euphorie.client.api.authentication.getUtility') \
                as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = 'secret'
            self.assertNotEqual(
                self.generate_token(
                    Account(id=5, loginname='john', password='jane')
                ),
                self.generate_token(
                    Account(id=5, loginname='john', password='alice')
                )
            )

    def test_password_not_in_token(self):
        with mock.patch('euphorie.client.api.authentication.getUtility') \
                as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = 'secret'
            self.assertTrue(
                'jane' not in self.generate_token(
                    Account(id=5, loginname='john', password='jane')
                )
            )


class authenticate_token_tests(DatabaseTests):

    def authenticate_token(self, *a, **kw):
        return authenticate_token(*a, **kw)

    def test_bad_token_form(self):
        self.assertEqual(self.authenticate_token('a-b-c'), None)

    def test_bad_id_in_token(self):
        self.assertEqual(self.authenticate_token('a-bc'), None)

    def test_unknown_account(self):
        self.assertEqual(self.authenticate_token('5-bc'), None)

    def test_known_account(self):
        with mock.patch(
            'euphorie.client.api.authentication.generate_token',
            return_value='1-hash'
        ):
            addAccount()
            self.assertEqual(
                self.authenticate_token('1-hash'), ('1', 'jane@example.com')
            )

    def test_invalid_token(self):
        with mock.patch(
            'euphorie.client.api.authentication.generate_token',
            return_value='1-otherhash'
        ):
            addAccount()
            self.assertTrue(self.authenticate_token('1-hash') is None)
