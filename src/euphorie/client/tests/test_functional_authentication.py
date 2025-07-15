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

    The row in the SQL database must have been created already
    with the email address of the user.
    """

    def setUp(self):
        super().setUp()
        request = self.app.REQUEST
        alsoProvides(request, IClientSkinLayer)

    def _call_authenticateCredentials(self, credentials):
        acl_users = api.portal.get_tool("acl_users")
        euphorie_plugin = acl_users.euphorie
        return euphorie_plugin.authenticateCredentials(credentials)

    def create_client_account(self):
        authenticator = api.content.get_view(
            "authenticator", context=self.portal, request=self.request
        )
        token = authenticator.token()
        request = self.app.REQUEST.clone()
        request.method = "POST"
        request.form["_authenticator"] = token
        view = api.content.get_view(
            "create-client-account", context=self.portal, request=request
        )
        view()

    def test_authentication_backend_user_proper_email(self):
        email = "foo@example.com"
        api.user.get_current().setMemberProperties({"email": email})

        # We try to login with email address, but at first this fails.
        credentials = {
            "login": email,
            "password": TEST_USER_PASSWORD,
            "extractor": "credentials_cookie_auth",
        }
        self.assertIsNone(self._call_authenticateCredentials(credentials))

        # We call the create-client-account view.
        self.create_client_account()
        session = Session()
        self.assertEqual(
            session.query(Account).filter_by(loginname="foo@example.com").one().id, 1
        )

        # TODO something is wrong here.  TEST_USER_NAME is test-user,
        # TEST_USER_ID is test_user_1_, but when our plugin calls
        # pas.searchUsers(email='foo@example.com', exact_match=True)
        # it finds a user with both id and login test_user_1_.
        # This means that self._validate_credentials_on_others a few lines
        # further on finds nothing.  So something in the setup may be wrong.
        # We should probably just test with a user where user id and login
        # name are the same.
        self.assertTupleEqual(
            (1, "foo@example.com"),
            self._call_authenticateCredentials(credentials),
        )

        self.assertEqual(credentials["login"], TEST_USER_NAME)

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
            (1, "foo@example.com"),
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
                f"WARNING:euphorie.client.authentication:Credentials for user {TEST_USER_NAME!r} are not valid according to other plugins. Refusing to login as a client SQL account.",  # noqa: E501
            ],
        )
