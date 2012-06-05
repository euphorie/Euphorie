from euphorie.client.tests.database import DatabaseTests
from euphorie.deployment.tests.functional import EuphorieTestCase


class add_api_authentication_tests(EuphorieTestCase):
    def add_api_authentication(self):
        from euphorie.deployment.upgrade.v4 import add_api_authentication
        add_api_authentication(self.portal.portal_setup)

    def test_already_configured(self):
        self.add_api_authentication()

    def test_plugin_missing(self):
        self.portal.acl_users.manage_delObjects('euphorie_api')
        self.add_api_authentication()
        self.assertTrue('euphorie_api' in self.portal.acl_users.objectIds())


class allow_empty_password_tests(DatabaseTests):
    create_tables = False

    def allow_empty_password(self):
        from euphorie.deployment.upgrade.v4 import allow_empty_password
        allow_empty_password(None)

    def test_not_nullable(self):
        import mock
        from z3c.saconfig import Session
        session = Session()
        session.execute('CREATE TABLE account (password TEXT)')
        session.execute = mock.Mock()
        self.allow_empty_password()
        self.assertTrue(not session.execute.called)

    def test_nullable(self):
        import mock
        from z3c.saconfig import Session
        session = Session()
        session.execute('CREATE TABLE account (password TEXT NOT NULL)')
        session.execute = mock.Mock()
        self.allow_empty_password()
        session.execute.assert_called_once_with(
                'ALTER TABLE account ALTER COLUMN password DROP NOT NULL')
