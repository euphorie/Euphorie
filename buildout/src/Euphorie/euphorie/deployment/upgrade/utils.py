
def TableExists(session, table):
    stmt = """SELECT tablename
              FROM pg_tables
              WHERE tablename='%(table)s';"""

    row = session.execute(stmt % dict(table=table)).scalar()
    return bool(row)



def ColumnExists(session, table, column):
    return bool(ColumnType(session, table, column))



def ColumnType(session, table, column):
    stmt = """SELECT pg_catalog.format_type(atttypid, atttypmod)
              FROM pg_attribute
              WHERE attrelid=(SELECT oid FROM pg_class WHERE relname='%(table)s') AND
                    attname='%(column)s';"""
    row = session.execute(stmt % dict(table=table, column=column)).scalar()
    return row


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

