# coding=utf-8
from euphorie.client import model
from euphorie.client.authentication import EuphorieAccountPlugin
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.tests.database import DatabaseTests
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin  # noqa
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin  # noqa
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from z3c.saconfig import Session
from zope.interface import directlyProvides
from zope.interface.verify import verifyClass

import mock


class MockContext(object):

    def absolute_url(self):
        return 'http://www.example.com/base'


class MockRequest(object):
    PUBLISHED = MockContext()

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def get(self, key, default=None):
        return getattr(self, key, default)

    getHeader = get


class MockResponse(object):

    def redirect(self, url, lock):
        self.redirect_url = url
        self.redirect_lock = lock


class EuphorieAccountPluginTests(DatabaseTests):

    def test_extraction_interface(self):
        verifyClass(IExtractionPlugin, EuphorieAccountPlugin)

    def test_extraction_no_token_header(self):
        plugin = EuphorieAccountPlugin('plugin')
        request = mock.Mock()
        request.getHeader.return_value = None
        self.assertEqual(plugin.extractCredentials(request), {})

    def test_extraction_with_token_header(self):
        plugin = EuphorieAccountPlugin('plugin')
        request = mock.Mock()
        request.getHeader.return_value = 'the-token'
        self.assertEqual(
            plugin.extractCredentials(request), {
                'api-token': 'the-token'
            }
        )

    def test_authenticate_interface(self):
        verifyClass(IAuthenticationPlugin, EuphorieAccountPlugin)

    def test_authenticate_token_no_token(self):
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(plugin._authenticate_token({}), None)

    def test_authenticate_token_call_client_authenticate(self):
        plugin = EuphorieAccountPlugin('plugin')
        with mock.patch(
            'euphorie.client.authentication.authenticate_client_token',
            return_value='result'
        ):
            self.assertEqual(
                plugin._authenticate_token({
                    'api-token': 'y'
                }), 'result'
            )

    def test_authenticate_token_call_cms_authenticate(self):
        plugin = EuphorieAccountPlugin('plugin')
        with mock.patch(
            'euphorie.client.authentication.authenticate_cms_token',
            return_value='result'
        ):
            self.assertEqual(
                plugin._authenticate_token({
                    'api-token': 'y'
                }), 'result'
            )

    def test_authenticate_login_wrong_credential_type(self):
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(
            plugin._authenticate_login({
                'cookie': 'yummie'
            }), None
        )

    def test_authenticate_login_unknown_account(self):
        plugin = EuphorieAccountPlugin('plugin')
        credentials = {'login': 'login', 'password': u'secret'}
        self.assertEqual(plugin._authenticate_login(credentials), None)

    def test_authenticate_login_valid_login(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        plugin = EuphorieAccountPlugin('plugin')
        credentials = {'login': 'john', 'password': u'jane'}
        self.assertTrue(plugin._authenticate_login(credentials) is not None)

    def test_authenticate_login_not_case_sensitive(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        plugin = EuphorieAccountPlugin('plugin')
        credentials = {'login': 'JoHn', 'password': u'jane'}
        self.assertTrue(plugin._authenticate_login(credentials) is not None)

    def test_CreateUser_interface(self):
        verifyClass(IUserFactoryPlugin, EuphorieAccountPlugin)

    def test_CreateUser_unknown_account(self):
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(plugin.createUser('1', 'john'), None)

    def testCreateUser_ValidAccount(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        plugin = EuphorieAccountPlugin('plugin')
        self.assertTrue(plugin.createUser('1', 'john') is account)

    def testEnumerateUsers_Interface(self):
        verifyClass(IUserEnumerationPlugin, EuphorieAccountPlugin)

    def testEnumerateUsers_NoInexactMatch(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(
            plugin.enumerateUsers(login='john', exact_match=False), []
        )

    def test_EnumerateUsers_search_by_id(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        request = MockRequest(ACTUAL_URL='http://www.example.com/client')
        directlyProvides(request, IClientSkinLayer)
        plugin = EuphorieAccountPlugin('plugin')
        plugin.REQUEST = request
        info = plugin.enumerateUsers(id='1', exact_match=True)
        self.assertEqual(info, [{'id': '1', 'login': 'john'}])
        self.assertTrue(isinstance(info[0]['id'], str))
        self.assertTrue(isinstance(info[0]['login'], str))

    def test_EnumerateUsers_search_by_login(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        request = MockRequest(ACTUAL_URL='http://www.example.com/client')
        directlyProvides(request, IClientSkinLayer)
        plugin = EuphorieAccountPlugin('plugin')
        plugin.REQUEST = request
        self.assertEqual(
            plugin.enumerateUsers(login='john', exact_match=True), [{
                'id': '1',
                'login': 'john'
            }]
        )

    def test_EnumerateUsers_search_by_login_and_id(self):
        session = Session()
        account = model.Account(loginname='john', password=u'jane')
        session.add(account)
        request = MockRequest(ACTUAL_URL='http://www.example.com/client')
        directlyProvides(request, IClientSkinLayer)
        plugin = EuphorieAccountPlugin('plugin')
        plugin.REQUEST = request
        self.assertEqual(
            plugin.enumerateUsers(id='1', login='john', exact_match=True), [{
                'id': '1',
                'login': 'john'
            }]
        )

    def test_EnumerateUsers_unknown_account(self):
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(plugin.enumerateUsers(id='1', exact_match=False), [])

    def test_Challenge_interface(self):
        verifyClass(IChallengePlugin, EuphorieAccountPlugin)

    def test_Challenge_require_IClientSkinLayer(self):
        request = MockRequest(ACTUAL_URL='http://www.example.com/client')
        response = MockResponse()
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(plugin.challenge(request, response), False)

    def test_Challenge_no_query_string(self):
        request = MockRequest(ACTUAL_URL='http://www.example.com/client')
        directlyProvides(request, IClientSkinLayer)
        response = MockResponse()
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(plugin.challenge(request, response), True)
        self.assertEqual(
            response.redirect_url, 'http://www.example.com/base/@@login?'
            'came_from=http%3A%2F%2Fwww.example.com%2Fclient'
        )
        self.assertEqual(bool(response.redirect_lock), True)

    def test_Challenge_with_query_string(self):
        request = MockRequest(
            ACTUAL_URL='http://www.example.com/client', QUERY_STRING='one=1'
        )
        directlyProvides(request, IClientSkinLayer)
        response = MockResponse()
        plugin = EuphorieAccountPlugin('plugin')
        self.assertEqual(plugin.challenge(request, response), True)
        self.assertEqual(
            response.redirect_url, 'http://www.example.com/base/@@login?'
            'came_from=http%3A%2F%2Fwww.example.com%2Fclient%3Fone%3D1'
        )
