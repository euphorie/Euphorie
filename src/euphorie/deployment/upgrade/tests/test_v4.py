from euphorie.client.tests.database import DatabaseTests
from euphorie.deployment.tests.functional import EuphorieTestCase


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
