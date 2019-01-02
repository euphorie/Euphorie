# vi: encoding=utf-8
from Acquisition import aq_base
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import Account
from euphorie.testing import EuphorieIntegrationTestCase
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from z3c.saconfig import Session
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


class AuthenticationTests(EuphorieIntegrationTestCase):

    def createAccount(self, login="john", password=u"jane"):
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
        self.failUnless(aq_base(user) is account)
        self.failUnless(isinstance(user.getId(), str))

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
            "http://nohost/plone/acl_users/credentials_cookie_auth/"
            "require_login?came_from=http%3A//nohost"
        )

    def testChallenge_InClient(self):
        self.logout()
        request = self.app.REQUEST
        request['PUBLISHED'] = self.portal
        request._has_challenged = False
        alsoProvides(request, IClientSkinLayer)
        self.portal.acl_users(None, request)
        self.portal.acl_users._unauthorized()
        self.assertEqual(
            request.response.headers["location"],
            "http://nohost/plone/@@login?came_from=http%3A%2F%2Fnohost",
        )
