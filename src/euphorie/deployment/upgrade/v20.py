# -*- coding: UTF-8 -*-
from euphorie.client import model
from logging import getLogger
from sqlalchemy.engine.reflection import Inspector
from z3c.saconfig import Session


logger = getLogger(__name__)


def execute(statement):
    ''' Execute the given SQL statement after a transition rollback
    (in order to prevent errors due to DB inconsistencies
    that the upgrade steps want to fix)
    and commit immediately after it is executed
    '''
    session = Session()
    logger.info(statement)
    session.execute('ROLLBACK;')
    session.execute(statement)
    session.execute('COMMIT;')


def add_group_table(context):
    ''' This will create missing tables:
    if the 'group' table is there it will just do nothing
    '''
    model.metadata.create_all(Session.bind)


def add_group_id_to_account(context):
    ''' A new 'group_id' column has been added to the 'account' table
    '''
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = {c['name'] for c in inspector.get_columns('account')}
    if 'group_id' in columns:
        return
    statement = (
        'ALTER TABLE account '
        'ADD COLUMN group_id INTEGER, '
        'ADD CONSTRAINT account_group_id_fkey '
        'FOREIGN KEY (group_id) '
        'REFERENCES "group" (group_id); '
    )
    execute(statement)


def add_group_id_to_session(context):
    ''' A new 'group_id' column has been added to the 'session' table
    '''
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = {c['name'] for c in inspector.get_columns('session')}
    if 'group_id' in columns:
        return
    statement = (
        'ALTER TABLE session '
        'ADD COLUMN group_id INTEGER, '
        'ADD CONSTRAINT session_group_id_fkey '
        'FOREIGN KEY (group_id) '
        'REFERENCES "group"(group_id);'
    )
    execute(statement)
