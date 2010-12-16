from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.schema import Table
from sqlalchemy.schema import MetaData

def TableExists(session, table):
    connection=session.bind
    return connection.dialect.has_table(connection, table)



def ColumnExists(session, table, column):
    connection=session.bind
    metadata=MetaData(connection)
    table=Table(table, metadata)
    try:
        connection.dialect.reflecttable(connection, table, [column])
    except NoSuchTableError:
        return False
    return column in table.c


def AddColumn(session, klass, col):
    from sqlalchemy.sql.expression import column
    from sqlalchemy import schema
    from sqlalchemy import util

    column_clause=column(col.key, col.type)
    compiler=session.bind.dialect.ddl_compiler(session.bind.dialect, column_clause)
    command=["ALTER TABLE", '"%s"' % klass.__tablename__, "ADD COLUMN"]
    command.append(compiler.get_column_specification(col))
    for constraint in col.constraints:
        command.append(compiler.process(constraint))

    if "DEFAULT" not in command[-1]:
        if col.type.__class__.__name__=="Boolean":
            command.append("DEFAULT 'f'")
        else:
            command.append("DEFAULT ''")

    session.execute(" ".join(command))

    if col.type.__class__.__name__=="Enum":
        constraint=schema.CheckConstraint(col.in_(col.type.enums), name=col.name,
                _create_rule=util.portable_instancemethod(col.type._should_create_constraint))
        constraint.parent=klass.__table__
        command=["ALTER TABLE", '"%s"' % klass.__tablename__, "ADD ", compiler.process(constraint)]
        session.execute(" ".join(command))

