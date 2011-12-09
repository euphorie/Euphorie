from euphorie.client.tests.database import DatabaseTests
from euphorie.client import model
from euphorie.client.authentication import EuphorieAccountPlugin
from z3c.saconfig import Session


class MockContext(object):
    def absolute_url(self):
        return "http://www.example.com/base"

class MockRequest(object):
    PUBLISHED = MockContext()
    def __init__(self, **kw):
        self.__dict__.update(kw)
    def get(self, key, default=None):
        return getattr(self, key, default)

class MockResponse(object):
    def redirect(self, url, lock):
        self.redirect_url=url
        self.redirect_lock=lock


class EuphorieAccountPluginTests(DatabaseTests):
    def testAuthenticate_Interface(self):
        from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
        from zope.interface.verify import verifyClass
        verifyClass(IAuthenticationPlugin, EuphorieAccountPlugin)

    def testAuthenticate_WrongCredentialType(self):
        plugin=EuphorieAccountPlugin("plugin")
        self.failUnless(plugin.authenticateCredentials(dict(cookie="yummie")) is None)

    def testAuthenticate_UnknownAccount(self):
        plugin=EuphorieAccountPlugin("plugin")
        self.failUnless(plugin.authenticateCredentials(dict(login="login", password=u"secret")) is None)

    def testAuthenticate_ValidLogin(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        info=plugin.authenticateCredentials(dict(login="john", password=u"jane"))
        self.assertEqual(info, ("john", "john"))
        self.failUnless(isinstance(info[0], str))
        self.failUnless(isinstance(info[1], str))

    def testAuthenticate_not_case_sensitive(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        info=plugin.authenticateCredentials({'login': 'JoHn', 'password': u'jane'})
        self.assertEqual(info, ("john", "john"))
        self.failUnless(isinstance(info[0], str))
        self.failUnless(isinstance(info[1], str))

    def testCreateUser_Interface(self):
        from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
        from zope.interface.verify import verifyClass
        verifyClass(IUserFactoryPlugin, EuphorieAccountPlugin)

    def testCreateUser_UnknownAccount(self):
        plugin=EuphorieAccountPlugin("plugin")
        self.failUnless(plugin.createUser(None, "john") is None)

    def testCreateUser_ValidAccount(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        self.failUnless(plugin.createUser(None, "john") is account)

    def testEnumerateUsers_Interface(self):
        from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
        from zope.interface.verify import verifyClass
        verifyClass(IUserEnumerationPlugin, EuphorieAccountPlugin)

    def testEnumerateUsers_NoInexactMatch(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.enumerateUsers(id="john", exact_match=False), [])

    def testEnumerateUsers_SearchById(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        info=plugin.enumerateUsers(id="john", exact_match=True)
        self.assertEqual(info, [dict(id="john", login="john")])
        self.failUnless(isinstance(info[0]["id"], str))
        self.failUnless(isinstance(info[0]["login"], str))

    def testEnumerateUsers_SearchByLogin(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.enumerateUsers(login="john", exact_match=True),
                         [dict(id="john", login="john")])

    def testEnumerateUsers_SearchByLoginAndId(self):
        session=Session()
        account=model.Account(loginname="john", password=u"jane")
        session.add(account)
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.enumerateUsers(login="john", id="john", exact_match=True),
                         [dict(id="john", login="john")])

    def testEnumerateUsers_UnknownAccount(self):
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.enumerateUsers(id="john", exact_match=False), [])

    def testChallenge_Interface(self):
        from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
        from zope.interface.verify import verifyClass
        verifyClass(IChallengePlugin, EuphorieAccountPlugin)

    def testChallenge_RequireIClientSkinLayer(self):
        request=MockRequest(ACTUAL_URL="http://www.example.com/client")
        response=MockResponse()
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.challenge(request, response), False)

    def testChallenge_NoQueryString(self):
        from euphorie.client.interfaces import IClientSkinLayer
        from zope.interface import directlyProvides
        request=MockRequest(ACTUAL_URL="http://www.example.com/client")
        directlyProvides(request, IClientSkinLayer)
        response=MockResponse()
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.challenge(request, response), True)
        self.assertEqual(response.redirect_url, "http://www.example.com/base/@@login?came_from=http%3A%2F%2Fwww.example.com%2Fclient")
        self.assertEqual(bool(response.redirect_lock), True)

    def testChallenge_WithQueryString(self):
        from euphorie.client.interfaces import IClientSkinLayer
        from zope.interface import directlyProvides
        request=MockRequest(ACTUAL_URL="http://www.example.com/client", QUERY_STRING="one=1")
        directlyProvides(request, IClientSkinLayer)
        response=MockResponse()
        plugin=EuphorieAccountPlugin("plugin")
        self.assertEqual(plugin.challenge(request, response), True)
        self.assertEqual(response.redirect_url, "http://www.example.com/base/@@login?came_from=http%3A%2F%2Fwww.example.com%2Fclient%3Fone%3D1")


