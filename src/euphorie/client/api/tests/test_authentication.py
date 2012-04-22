import unittest


class EuphorieAPIPluginTests(unittest.TestCase):
    def EuphorieAPIPlugin(self, *a, **kw):
        from euphorie.client.api.authentication import EuphorieAPIPlugin
        return EuphorieAPIPlugin(*a, **kw)

    def test_generate_token_differs_per_account(self):
        import mock
        account1 = mock.Mock()
        account1.id = 15
        account2 = mock.Mock()
        account2.id = 23
        plugin = self.EuphorieAPIPlugin('id')
        plugin._getSecret = mock.Mock(return_value='secret')
        self.assertTrue(
            plugin.generate_token(account1) != plugin.generate_token(account2))

    def test_generate_token_ascii_output(self):
        import re
        import mock
        account = mock.Mock()
        account.id = 15
        plugin = self.EuphorieAPIPlugin('id')
        plugin._getSecret = mock.Mock(return_value='secret')
        token = plugin.generate_token(account)
        self.assertTrue(re.match('^[a-zA-Z0-9/=+-]+$', token))

    def test_extractCredentials_no_token_present(self):
        import mock
        request = mock.Mock()
        request.getHeader.return_value = None
        plugin = self.EuphorieAPIPlugin('id')
        self.assertEqual(plugin.extractCredentials(request), {})
        request.getHeader.assert_called_once_with('X-Euphorie-Token')

    def test_extractCredentials_invalid_token(self):
        import mock
        request = mock.Mock()
        request.getHeader.return_value = 'broken'
        plugin = self.EuphorieAPIPlugin('id')
        self.assertEqual(plugin.extractCredentials(request), {})
        request.getHeader.assert_called_once_with('X-Euphorie-Token')

    def test_extractCredentials_valid_token(self):
        import mock
        request = mock.Mock()
        request.getHeader.return_value = 'dmFsaWQ='
        plugin = self.EuphorieAPIPlugin('id')
        self.assertEqual(
                plugin.extractCredentials(request),
                {'api-token': 'valid'})
        request.getHeader.assert_called_once_with('X-Euphorie-Token')

    def test_authenticateCredentials_no_token(self):
        plugin = self.EuphorieAPIPlugin('id')
        self.assertEqual(plugin.authenticateCredentials({}), None)

    def test_authenticateCredentials_invalid_token(self):
        import mock
        plugin = self.EuphorieAPIPlugin('id')
        with mock.patch('plone.session.tktauth.validateTicket') \
                as mock_validate:
            mock_validate.return_value = None
            credentials = {'api-token': 'token'}
            plugin._getSecret = mock.Mock(return_value='secret')
            self.assertEqual(
                    plugin.authenticateCredentials(credentials),
                    None)
            mock_validate.assert_called_once_with('secret', 'token')

    def test_authenticateCredentials_valid_token_unknown_userid(self):
        import mock
        plugin = self.EuphorieAPIPlugin('id')
        with mock.patch('plone.session.tktauth.validateTicket') \
                as mock_validate:
            mock_validate.return_value = ('dummy', 'userid')
            plugin._getLogin = mock.Mock(return_value=None)
            plugin._getSecret = mock.Mock(return_value='secret')
            credentials = {'api-token': 'token'}
            self.assertEqual(
                    plugin.authenticateCredentials(credentials),
                    None)
            plugin._getLogin.assert_called_once_with('userid')

    def test_authenticateCredentials_valid_token_valid_userid(self):
        import mock
        plugin = self.EuphorieAPIPlugin('id')
        with mock.patch('plone.session.tktauth.validateTicket') \
                as mock_validate:
            mock_validate.return_value = ('dummy', 'userid')
            plugin._getSecret = mock.Mock(return_value='secret')
            plugin._getLogin = mock.Mock(return_value='login')
            credentials = {'api-token': 'token'}
            self.assertEqual(
                    plugin.authenticateCredentials(credentials),
                    ('login', 'login'))
