import unittest


def _createSession():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine("sqlite:///")
    return sessionmaker(bind=engine)()


class TableExistsTests(unittest.TestCase):
    def TableExists(self, session, table):
        from euphorie.deployment.upgrade.utils import TableExists
        return TableExists(session, table)

    def testMissingTable(self):
        session = _createSession()
        self.assertEqual(self.TableExists(session, "dummy"), False)

    def testExistingTable(self):
        session = _createSession()
        session.execute("CREATE TABLE dummy (id INT);")
        self.assertEqual(self.TableExists(session, "dummy"), True)


class ColumnExistsTests(unittest.TestCase):
    def ColumnExists(self, session, table, column):
        from euphorie.deployment.upgrade.utils import ColumnExists
        return ColumnExists(session, table, column)

    def testMissingTable(self):
        session = _createSession()
        self.assertEqual(self.ColumnExists(session, "dummy", "id"), False)

    def testExistingTable(self):
        session = _createSession()
        session.execute("CREATE TABLE dummy (id INT);")
        self.assertEqual(self.ColumnExists(session, "dummy", "foo"), False)

    def testExistingColumn(self):
        session = _createSession()
        session.execute("CREATE TABLE dummy (id INT);")
        self.assertEqual(self.ColumnExists(session, "dummy", "id"), True)
