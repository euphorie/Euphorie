# coding=utf-8
from ...sector import Sector
from ...tests.utils import createSector
from ...user import IUser
from ..authentication import _get_user
from ..authentication import Authenticate
from ..authentication import authenticate_credentials
from ..authentication import authenticate_token
from ..authentication import generate_token
from euphorie.testing import EuphorieFunctionalTestCase
from plone.keyring.interfaces import IKeyManager
from zope.interface import directlyProvides
from zope.publisher.browser import TestRequest

import json
import mock
import unittest


class get_user_tests(unittest.TestCase):
    def _get_user(self, *a, **kw):
        return _get_user(*a, **kw)

    def test_unknown_user(self):
        membrane = mock.Mock()
        membrane.getUserObject.return_value = None
        with mock.patch(
            "euphorie.content.api.authentication.getToolByName", return_value=membrane
        ):
            self.assertEqual(self._get_user(None, "jane"), None)
            membrane.getUserObject.assert_called_once_with(login="jane")

    def test_wrong_user_type(self):
        membrane = mock.Mock()
        membrane.getUserObject.return_value = "user"
        with mock.patch(
            "euphorie.content.api.authentication.getToolByName", return_value=membrane
        ):
            self.assertEqual(self._get_user(None, "jane"), None)

    def test_valid_user(self):
        user = mock.Mock()
        directlyProvides(user, IUser)
        membrane = mock.Mock()
        membrane.getUserObject.return_value = user
        with mock.patch(
            "euphorie.content.api.authentication.getToolByName", return_value=membrane
        ):
            self.assertTrue(self._get_user(None, "jane") is user)


class generate_token_tests(unittest.TestCase):
    def generate_token(self, *a, **kw):
        return generate_token(*a, **kw)

    def test_token_depends_on_login(self):
        with mock.patch(
            "euphorie.content.api.authentication.getUtility"
        ) as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = "secret"
            self.assertNotEqual(
                self.generate_token(Sector(login="jane", password=u"john")),
                self.generate_token(Sector(login="lucy", password=u"john")),
            )

    def test_token_depends_on_password(self):
        with mock.patch(
            "euphorie.content.api.authentication.getUtility"
        ) as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = "secret"
            self.assertNotEqual(
                self.generate_token(Sector(login="jane", password=u"john")),
                self.generate_token(Sector(login="jane", password=u"dave")),
            )


class authenticate_token_tests(unittest.TestCase):
    def authenticate_token(self, *a, **kw):
        return authenticate_token(*a, **kw)

    def test_bad_token_form(self):
        self.assertEqual(self.authenticate_token(None, "a-b-c"), None)

    def test_unknown_account(self):
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value=None
        ):
            self.assertEqual(self.authenticate_token(None, "sector-bc"), None)

    def test_known_account(self):
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value="user"
        ):
            with mock.patch(
                "euphorie.content.api.authentication.generate_token",
                return_value="1-hash",
            ):
                with mock.patch(
                    "euphorie.content.api.authentication.IMembraneUserAuth"
                ) as mock_auth:
                    mock_auth("user", None).getUserId.return_value = "userid"
                    mock_auth("user", None).getUserName.return_value = "login"
                    self.assertEqual(
                        self.authenticate_token(None, "1-hash"), ("userid", "login")
                    )

    def test_invalid_token(self):
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value="user"
        ):
            with mock.patch(
                "euphorie.content.api.authentication.generate_token",
                return_value="1-hash",
            ):
                self.assertEqual(self.authenticate_token(None, "1-hosh"), None)


class authenticate_credentials_tests(unittest.TestCase):
    def authenticate_credentials(self, *a, **kw):
        return authenticate_credentials(*a, **kw)

    def test_unknown_account(self):
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value=None
        ):
            self.assertEqual(
                self.authenticate_credentials(None, "sector", "sector"), None
            )

    def test_locked_account(self):
        user = mock.Mock()
        user.locked = True
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value=user
        ):
            self.assertEqual(
                self.authenticate_credentials(None, "sector", "sector"), None
            )

    def test_bad_password(self):
        user = mock.Mock()
        user.locked = False
        auth = mock.Mock()
        auth.authenticateCredentials.return_value = None
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value=user
        ):
            with mock.patch(
                "euphorie.content.api.authentication.IMembraneUserAuth",
                return_value=auth,
            ):
                self.assertEqual(
                    self.authenticate_credentials(None, "sector", "secret"), None
                )
                auth.authenticateCredentials.assert_called_once_with(
                    {"login": "sector", "password": "secret"}
                )

    def test_valid_credentials(self):
        user = mock.Mock()
        user.locked = False
        auth = mock.Mock()
        auth.authenticateCredentials.return_value = ("id", "login")
        with mock.patch(
            "euphorie.content.api.authentication._get_user", return_value=user
        ):
            with mock.patch(
                "euphorie.content.api.authentication.IMembraneUserAuth",
                return_value=auth,
            ):
                self.assertTrue(
                    self.authenticate_credentials(None, "sector", "secret") is user
                )


class AuthenticateTests(unittest.TestCase):
    def test_do_POST_missing_data(self):
        view = Authenticate(None, TestRequest())
        view.input = {}
        response = view.do_POST()
        self.assertEqual(view.request.response.getStatus(), 403)
        self.assertEqual(set(response), set(["type", "message"]))
        self.assertEqual(response["type"], "error")

    def test_do_POST_bad_credentials(self):
        view = Authenticate("context", TestRequest())
        view.input = {"login": "jane", "password": "john"}
        with mock.patch(
            "euphorie.content.api.authentication.authenticate_credentials",
            return_value=None,
        ) as mock_authentication_credentials:
            response = view.do_POST()
            mock_authentication_credentials.assert_called_once_with(
                "context", "jane", "john"
            )
            self.assertEqual(view.request.response.getStatus(), 403)
            self.assertEqual(set(response), set(["type", "message"]))
            self.assertEqual(response["type"], "error")

    def test_do_POST_correct_credentials(self):
        view = Authenticate(None, TestRequest())
        view.user_url = mock.Mock(return_value="url")
        user = mock.Mock()
        user.title = u"Jane Doe"
        user.login = "jane"
        view.input = {"login": "jane", "password": "john"}
        with mock.patch(
            "euphorie.content.api.authentication.authenticate_credentials",
            return_value=user,
        ):
            with mock.patch(
                "euphorie.content.api.authentication.generate_token",
                return_value="token",
            ) as mock_generate_token:
                response = view.do_POST()
                mock_generate_token.assert_called_once_with(user)
                self.assertEqual(set(response), set(["token", "title", "login", "url"]))
                self.assertEqual(response["token"], "token")
                self.assertEqual(response["title"], u"Jane Doe")
                self.assertEqual(response["login"], "jane")
                self.assertEqual(response["url"], "url")


class AuthenticateBrowserTests(EuphorieFunctionalTestCase):
    def test_bad_login(self):
        browser = self.get_browser()
        browser.raiseHttpErrors = False
        browser.post(
            "http://nohost/plone/api/authenticate",
            '{"login": "sector", "password": "secret"}',
        )
        self.assertTrue(browser.headers["Status"].startswith("403"))
        self.assertEqual(browser.headers["Content-Type"], "application/json")

    def test_valid_login(self):
        createSector(
            self.portal,
            id="my-sector",
            country="nl",
            login="sector",
            password=u"secret",
        )
        browser = self.get_browser()
        browser.post(
            "http://nohost/plone/api/authenticate",
            '{"login": "sector", "password": "secret"}',
        )
        response = json.loads(browser.contents)
        self.assertEqual(set(response), set(["token", "title", "login", "url"]))
        self.assertEqual(
            response["url"], "http://nohost/plone/api/countries/nl/sectors/my-sector"
        )
