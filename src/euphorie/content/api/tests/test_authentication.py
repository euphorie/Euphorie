import unittest


class get_user_tests(unittest.TestCase):
    def _get_user(self, *a, **kw):
        from ..authentication import _get_user
        return _get_user(*a, **kw)

    def test_unknown_user(self):
        import mock
        membrane = mock.Mock()
        membrane.getUserObject.return_value = None
        with mock.patch('euphorie.content.api.authentication.getToolByName',
                return_value=membrane):
            self.assertEqual(self._get_user(None, 'jane'), None)
            membrane.getUserObject.assert_called_once_with(login='jane')

    def test_wrong_user_type(self):
        import mock
        membrane = mock.Mock()
        membrane.getUserObject.return_value = 'user'
        with mock.patch('euphorie.content.api.authentication.getToolByName',
                return_value=membrane):
            self.assertEqual(self._get_user(None, 'jane'), None)

    def test_valid_user(self):
        from zope.interface import directlyProvides
        import mock
        from ...user import IUser
        user = mock.Mock()
        directlyProvides(user, IUser)
        membrane = mock.Mock()
        membrane.getUserObject.return_value = user
        with mock.patch('euphorie.content.api.authentication.getToolByName',
                return_value=membrane):
            self.assertTrue(self._get_user(None, 'jane') is user)


class generate_token_tests(unittest.TestCase):
    def generate_token(self, *a, **kw):
        from ..authentication import generate_token
        return generate_token(*a, **kw)

    def test_token_depends_on_login(self):
        import mock
        from plone.keyring.interfaces import IKeyManager
        from ...sector import Sector
        with mock.patch('euphorie.content.api.authentication.getUtility') \
                as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = 'secret'
            self.assertNotEqual(
                    self.generate_token(Sector(login='jane', password=u'john')),
                    self.generate_token(Sector(login='lucy', password=u'john')))

    def test_token_depends_on_password(self):
        import mock
        from plone.keyring.interfaces import IKeyManager
        from ...sector import Sector
        with mock.patch('euphorie.content.api.authentication.getUtility') \
                as mock_getUtility:
            mock_getUtility(IKeyManager).secret.return_value = 'secret'
            self.assertNotEqual(
                    self.generate_token(Sector(login='jane', password=u'john')),
                    self.generate_token(Sector(login='jane', password=u'dave')))
