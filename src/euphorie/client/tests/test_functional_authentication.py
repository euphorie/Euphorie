from Acquisition import aq_base
from euphorie.client import config
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import Account
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from z3c.saconfig import Session
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class AuthenticationTests(EuphorieIntegrationTestCase):
    def createAccount(self, login="john", password="jane"):
        session = Session()
        account = Account(loginname=login, password=password)
        session.add(account)
        session.flush()
        return account

    def testGetUserById_UnknownAccount(self):
        self.assertEqual(self.portal.acl_users.getUserById("john"), None)

    def testGetUserById_ValidAccount(self):
        request = self.app.REQUEST
        alsoProvides(request, IClientSkinLayer)
        account = self.createAccount()
        user = self.portal.acl_users.getUserById(str(account.id))
        self.assertTrue(aq_base(user) is account)
        self.assertTrue(isinstance(user.getId(), str))

    def testChallenge_OutsideClient(self):
        self.logout()
        request = self.request
        request._has_challenged = False
        # XXX the NuPloneSkin challenger returns a 403
        noLongerProvides(request, NuPloneSkin)
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(
            request.response.headers["location"],
            "http://nohost/plone/acl_users/credentials_cookie_auth/require_login?came_from=",  # noqa: E501
        )

    def testChallenge_InClient(self):
        self.logout()
        request = self.app.REQUEST
        request["PUBLISHED"] = self.portal
        request._has_challenged = False
        alsoProvides(request, IClientSkinLayer)
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(
            request.response.headers["location"],
            "http://nohost/plone/@@login?came_from=http%3A%2F%2Fnohost#login",
        )


class AuthenticationPluginTests(EuphorieIntegrationTestCase):
    """Check if our authentication plugin is able to authenticate backend users
    also in the frontend.

    This requires the user to have a valid email address.

    The missing row in the SQL database will be created automatically
    if the user has a valid email address.
    """

    def setUp(self):
        super().setUp()
        request = self.app.REQUEST
        alsoProvides(request, IClientSkinLayer)

    def _call_authenticateCredentials(self, credentials):
        acl_users = api.portal.get_tool("acl_users")
        euphorie_plugin = acl_users.euphorie
        return euphorie_plugin.authenticateCredentials(credentials)

    def test_authentication_backend_user_no_email(self):
        credentials = {
            "login": TEST_USER_NAME,
            "password": TEST_USER_PASSWORD,
            "extractor": "credentials_cookie_auth",
        }

        with self.assertLogs("euphorie.client.authentication") as cm:
            self.assertIsNone(self._call_authenticateCredentials(credentials))

        self.assertListEqual(
            cm.output,
            [
                f"WARNING:euphorie.client.authentication:No email address set for user {TEST_USER_NAME!r}. Cannot create a SQL account."  # noqa: E501
            ],
        )

    def test_authentication_backend_user_proper_email(self):
        api.user.get(username=TEST_USER_NAME).setProperties(
            {"email": "foo@example.com"}
        )

        credentials = {
            "login": TEST_USER_NAME,
            "password": TEST_USER_PASSWORD,
            "extractor": "credentials_cookie_auth",
        }
        with self.assertLogs("euphorie.client.authentication") as cm:
            self.assertTupleEqual(
                ("1", "foo@example.com"),
                self._call_authenticateCredentials(credentials),
            )

        self.assertListEqual(
            cm.output,
            [
                "INFO:euphorie.client.authentication:A SQL account 'foo@example.com' was created for user 'test-user'.",  # noqa: E501
            ],
        )

        session = Session()
        self.assertEqual(
            session.query(Account).filter_by(loginname="foo@example.com").one().id, 1
        )
        self.assertEqual(credentials["email_overrides_login"], "foo@example.com")

    def test_authentication_backend_user_proper_email_account_already_existing(self):
        api.user.get(username=TEST_USER_NAME).setProperties(
            {"email": "foo@example.com"}
        )

        session = Session()
        session.add(
            Account(
                loginname="foo@example.com",
                tc_approved=1,
                password=TEST_USER_PASSWORD,
                account_type=config.FULL_ACCOUNT,
            )
        )

        credentials = {
            "login": TEST_USER_NAME,
            "password": TEST_USER_PASSWORD,
            "extractor": "credentials_cookie_auth",
        }
        self.assertTupleEqual(
            ("1", "foo@example.com"),
            self._call_authenticateCredentials(credentials),
        )

    def test_authentication_backend_user_bogus_password(self):
        credentials = {
            "login": TEST_USER_NAME,
            "extractor": "credentials_cookie_auth",
            "password": "malicious_password",
        }
        api.user.get(username=TEST_USER_NAME).setProperties(
            {"email": "foo@example.com"}
        )

        with self.assertLogs("euphorie.client.authentication") as cm:
            self.assertIsNone(
                self._call_authenticateCredentials(credentials),
            )

        self.assertListEqual(
            cm.output,
            [
                f"WARNING:euphorie.client.authentication:Credentials for user {TEST_USER_NAME!r} are not valid according to other plugins. Refusing to create a SQL account.",  # noqa: E501
            ],
        )
