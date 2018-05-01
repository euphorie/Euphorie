# -*- coding: UTF-8 -*-
''' Upgrade the database tables if needed'''
from euphorie.client import model
from logging import getLogger
from pkg_resources import get_distribution
from pkg_resources import parse_version
from Products.Five import zcml
from sqlalchemy.engine.reflection import Inspector
from sys import argv
from z3c.saconfig import Session


logger = getLogger(__name__)
euphorie_version = get_distribution('euphorie').parsed_version

try:
    config = argv[1]
except IndexError:
    config = 'parts/instance/etc/package-includes/999-additional-overrides.zcml'  # noqa: E501

zcml.load_config(config)
session = Session()
inspector = Inspector.from_engine(session.bind)


def execute(statement):
    ''' Execute the given SQL statement and commit immediately after it is
    executed
    '''
    logger.info(statement)
    session.execute(statement)
    session.execute('COMMIT;')


def create_missing_tables():
    ''' This will create the missing tables
    '''
    model.metadata.create_all(Session.bind, checkfirst=True)


def add_group_id_to_account():
    ''' A new 'group_id' column has been added to the 'account' table
    '''
    for column in inspector.get_columns('account'):
        if 'group_id' == column['name']:
            return
    statement = (
        '''
        ALTER TABLE account
            ADD COLUMN group_id character varying(32);
        ALTER TABLE account
            ADD CONSTRAINT account_group_id_fkey
            FOREIGN KEY (group_id)
            REFERENCES "group" (group_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;
        '''
    )
    execute(statement)


def add_group_id_to_session():
    ''' A new 'group_id' column has been added to the 'session' table
    '''
    for column in inspector.get_columns('session'):
        if 'group_id' == column['name']:
            return

    statement = (
        '''
        ALTER TABLE session
            ADD COLUMN group_id character varying(32);
        ALTER TABLE session
            ADD CONSTRAINT session_group_id_fkey
            FOREIGN KEY (group_id)
            REFERENCES public."group" (group_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;
        '''
    )
    execute(statement)


def main():
    # It is always a good idea to run this one
    create_missing_tables()
    if euphorie_version < parse_version('10.0.1'):
        add_group_id_to_account()
        add_group_id_to_session()


if __name__ == "__main__":
    main()
