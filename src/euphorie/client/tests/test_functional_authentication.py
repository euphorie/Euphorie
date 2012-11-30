# vi: encoding=utf-8

from euphorie.deployment.tests.functional import EuphorieTestCase
from z3c.saconfig import Session


class AuthenticationTests(EuphorieTestCase):
    def createAccount(self, login="john", password=u"jane"):
        from euphorie.client.model import Account
        session = Session()
        account = Account(loginname=login, password=password)
        session.add(account)
        session.flush()
        return account

    def testGetUserById_UnknownAccount(self):
        self.assertEqual(self.portal.acl_users.getUserById("john"), None)

    def testGetUserById_ValidAccount(self):
        from Acquisition import aq_base
        account = self.createAccount()
        user = self.portal.acl_users.getUserById(str(account.id))
        self.failUnless(aq_base(user) is account)
        self.failUnless(isinstance(user.getId(), str))

    def testChallenge_OutsideClient(self):
        request = self.app.REQUEST
        request._has_challenged = False
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(
                request.response.headers["location"],
                "http://nohost/plone/acl_users/credentials_cookie_auth/"
                "require_login?came_from=http%3A//nohost")

    def testChallenge_InClient(self):
        from euphorie.client.interfaces import IClientSkinLayer
        from zope.interface import alsoProvides
        request = self.app.REQUEST
        request.PUBLISHED = self.portal
        request._has_challenged = False
        alsoProvides(request, IClientSkinLayer)
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(
                request.response.headers["location"],
                "http://nohost/plone/@@login?came_from=http%3A%2F%2Fnohost")
