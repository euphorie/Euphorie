# vi: encoding=utf-8

from euphorie.client.tests.functional import EuphorieClientTestCase
from z3c.saconfig import Session


class AuthenticationTests(EuphorieClientTestCase):
    def createPasPlugin(self):
        from euphorie.client.authentication import addEuphorieAccountPlugin
        from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
        from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
        from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
        from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
        pas=self.portal.acl_users
        addEuphorieAccountPlugin(pas, "euphorie")
        pas.plugins.activatePlugin(IAuthenticationPlugin, "euphorie")
        pas.plugins.activatePlugin(IChallengePlugin, "euphorie")
        pas.plugins.activatePlugin(IUserEnumerationPlugin, "euphorie")
        pas.plugins.activatePlugin(IUserFactoryPlugin, "euphorie")
        # Make sure we are the first user factory plugin
        for _ in pas.plugins.listPlugins(IUserFactoryPlugin):
            pas.plugins.movePluginsUp(IUserFactoryPlugin, ("euphorie",))
        # Make sure we are the first challenge plugin
        for _ in pas.plugins.listPlugins(IChallengePlugin):
            pas.plugins.movePluginsUp(IChallengePlugin, ("euphorie",))

    def createAccount(self, login="john", password=u"jane"):
        from euphorie.client.model import Account
        session=Session()
        account=Account(loginname=login, password=password)
        session.add(account)
        session.flush()
        return account

    def testGetUserById_UnknownAccount(self):
        self.createPasPlugin()
        self.assertEqual(self.portal.acl_users.getUserById("john"), None)

    def testGetUserById_ValidAccount(self):
        from Acquisition import aq_base
        self.createPasPlugin()
        account=self.createAccount()
        user=self.portal.acl_users.getUserById("john")
        self.failUnless(aq_base(user) is account)
        self.failUnless(isinstance(user.getId(), str))

    def testChallenge_OutsideClient(self):
        self.createPasPlugin()
        request=self.app.REQUEST
        request._has_challenged=False
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(request.response.headers["location"],
                         "http://nohost/plone/acl_users/credentials_cookie_auth/require_login?came_from=http%3A//nohost")

    def testChallenge_InClient(self):
        from euphorie.client.interfaces import IClientSkinLayer
        from zope.interface import alsoProvides
        self.createPasPlugin()
        request=self.app.REQUEST
        request.PUBLISHED=self.portal
        request._has_challenged=False
        alsoProvides(request, IClientSkinLayer)
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(request.response.headers["location"],
                         "http://nohost/plone/@@login?came_from=http%3A%2F%2Fnohost")


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

