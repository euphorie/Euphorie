from contextlib import contextmanager
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.utils import getRequest
from euphorie.client.utils import setRequest
from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import quickInstallProduct
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import zope
from plone.testing.zope import Browser
from sqlalchemy import event
from transaction import commit
from unittest import mock
from unittest import TestCase
from z3c.saconfig import Session
from Zope2.Startup.datatypes import default_zpublisher_encoding
from zope.interface import alsoProvides
from zope.sqlalchemy.datamanager import NO_SAVEPOINT_SUPPORT

import euphorie.deployment


NO_SAVEPOINT_SUPPORT.remove("sqlite")


class EuphorieFixture(PloneSandboxLayer):
    saconfig_filename = "configure.zcml"

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import euphorie.client.tests
        import euphorie.deployment.tests

        self.loadZCML("configure.zcml", package=euphorie.deployment)
        self.loadZCML("overrides.zcml", package=euphorie.deployment)
        self.loadZCML("configure.zcml", package=euphorie.client.tests)
        self.loadZCML("configure.zcml", package=euphorie.deployment.tests)
        zope.installProduct(app, "Products.membrane")

        self.loadZCML(self.saconfig_filename, package=euphorie.client.tests)
        engine = Session.bind

        @event.listens_for(engine, "connect")
        def do_connect(dbapi_connection, connection_record):
            # disable pysqlite's emitting of the BEGIN statement entirely.
            # also stops it from emitting COMMIT before any DDL.
            dbapi_connection.isolation_level = None

        @event.listens_for(engine, "begin")
        def do_begin(conn):
            # emit our own BEGIN
            conn.execute("BEGIN")

        # Start fresh
        self.testTearDown()

        default_zpublisher_encoding("utf-8")

    def setUpPloneSite(self, portal):
        pw = api.portal.get_tool("portal_workflow")
        pw.setDefaultChain("simple_publication_workflow")

        quickInstallProduct(portal, "plonetheme.nuplone")
        quickInstallProduct(portal, "euphorie.client")
        quickInstallProduct(portal, "euphorie.content")

        all_countries = euphorie.deployment.setuphandlers.COUNTRIES.copy()
        euphorie.deployment.setuphandlers.COUNTRIES = {
            key: all_countries[key]
            for key in all_countries
            if key
            in (
                "de",
                "nl",
            )
        }

        with mock.patch(
            "plone.i18n.utility.LanguageUtility.listSupportedLanguages",
            return_value=[
                ("de", "German"),
                ("nl", "Dutch"),
            ],
        ):
            quickInstallProduct(portal, "euphorie.deployment.tests")

        session = portal.acl_users.get("session")
        # In tests we don't have secure connections
        session.secure = False

    def testSetUp(self):
        """XXX testSetUp and testTearDown should not be necessary, but it seems
        SQL data is not correctly cleared at the end of a test method run, even
        if testTearDown does an explicit transaction.abort()"""
        model.metadata.create_all(Session.bind, checkfirst=True)

    def testTearDown(self):
        Session.remove()
        model.metadata.drop_all(Session.bind)


class EuphorieRobotFixture(EuphorieFixture):
    saconfig_filename = "robot.zcml"


EUPHORIE_FIXTURE = EuphorieFixture()
EUPHORIE_ROBOT_FIXTURE = EuphorieRobotFixture()

EUPHORIE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EUPHORIE_FIXTURE,),
    name="EuphorieFixture:Integration",
)


EUPHORIE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EUPHORIE_FIXTURE,),
    name="EuphorieFixture:Functional",
)


class EuphorieIntegrationTestCase(TestCase):
    layer = EUPHORIE_INTEGRATION_TESTING
    request_layer = IClientSkinLayer

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def loginAsPortalOwner(self):
        return login(self.app, "admin")

    def login(self, username):
        return login(self.portal, username)

    def logout(self):
        return logout()

    @contextmanager
    def _get_view(self, name, obj, survey_session=None, client=None):
        """Get's a view with a proper fresh request.

        If survey_session is set the SessionManager will be configured
        """
        old_request = getRequest()
        request = self.get_client_request(client=client)
        if survey_session is not None:
            request.other["euphorie.session"] = survey_session
        try:
            setRequest(request)
            yield api.content.get_view(name, obj, request)
        finally:
            setRequest(old_request)

    def get_client_request(self, client=None):
        request = self.request.clone()
        request.client = client
        alsoProvides(request, self.request_layer)
        return request


class EuphorieFunctionalTestCase(EuphorieIntegrationTestCase):
    layer = EUPHORIE_FUNCTIONAL_TESTING

    _default_credentials = {
        "username": TEST_USER_NAME,
        "password": TEST_USER_PASSWORD,
    }

    def get_browser(self, logged_in=False, credentials={}):
        """Return a browser, potentially a logged in one.

        The default credentials are the admin ones
        """
        commit()
        browser = Browser(self.app)
        if logged_in or credentials:
            username = credentials.get(
                "username", self._default_credentials["username"]
            )
            password = credentials.get(
                "password", self._default_credentials["password"]
            )
            browser.open("%s/@@login" % self.portal.absolute_url())
            browser.getControl(name="__ac_name").value = username
            browser.getControl(name="__ac_password").value = password
            browser.getForm(id="loginForm").submit()
        return browser
