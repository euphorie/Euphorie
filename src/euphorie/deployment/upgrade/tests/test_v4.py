from euphorie.client.tests.database import DatabaseTests


class add_actionplan_reference_tests(DatabaseTests):
    create_tables = False

    def add_actionplan_reference(self):
        from euphorie.deployment.upgrade.v4 import add_actionplan_reference
        add_actionplan_reference(None)

    def test_not_nullable(self):
        import mock
        from z3c.saconfig import Session
        session = Session()
        session.execute('CREATE TABLE action_plan (reference TEXT)')
        session.execute = mock.Mock()
        self.add_actionplan_reference()
        self.assertTrue(not session.execute.called)

    def test_nullable(self):
        import mock
        from z3c.saconfig import Session
        session = Session()
        session.execute('CREATE TABLE action_plan (foo INT)')
        session.execute = mock.Mock()
        self.add_actionplan_reference()
        session.execute.assert_called_once_with(
                'ALTER TABLE action_plan ADD COLUMN reference TEXT')


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
