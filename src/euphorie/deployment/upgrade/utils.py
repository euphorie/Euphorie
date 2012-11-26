from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import Table
from sqlalchemy.schema import MetaData


def TableExists(session, table):
    connection = session.bind
    return connection.dialect.has_table(connection, table)


def ColumnExists(session, table, column):
    connection = session.bind
    metadata = MetaData(connection)
    table = Table(table, metadata)
    try:
        connection.dialect.reflecttable(connection, table, None)
    except NoSuchTableError:
        return False
    return column in table.c
