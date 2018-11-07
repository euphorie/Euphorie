# -*- coding: UTF-8 -*-
''' Upgrade the database tables if needed'''
from __future__ import print_function
from datetime import datetime
from euphorie.client import model
from logging import getLogger
from pkg_resources import get_distribution
from pkg_resources import parse_version
from Products.Five import zcml
from sqlalchemy import sql
from sqlalchemy.engine.reflection import Inspector
from sys import argv
from transaction import commit
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


def add_brand_to_session():
    ''' A new 'brand' column has been added to the 'session' table
    '''
    for column in inspector.get_columns('session'):
        if 'brand' == column['name']:
            return

    statement = (
        '''
        ALTER TABLE session
            ADD COLUMN brand character varying(64);
        '''
    )
    execute(statement)


def add_brand_to_group():
    ''' A new 'brand' column has been added to the 'group' table
    '''
    for column in inspector.get_columns('group'):
        if 'brand' == column['name']:
            return

    statement = (
        '''
        ALTER TABLE "group"
            ADD COLUMN brand character varying(64);
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


def add_published_to_session():
    ''' A new 'published' column has been added to the 'session' table
    '''
    for column in inspector.get_columns('session'):
        if 'published' == column['name']:
            return

    statement = (
        '''
        ALTER TABLE session
            ADD COLUMN published timestamp with time zone;
        '''
    )
    execute(statement)


def add_last_modifier_id_to_session():
    ''' A new 'last_modifier_id' column has been added to the 'session' table
    '''
    for column in inspector.get_columns('session'):
        if 'last_modifier_id' == column['name']:
            return

    statement = (
        '''
        ALTER TABLE session
            ADD COLUMN last_modifier_id integer;
        ALTER TABLE session
            ADD CONSTRAINT session_last_modifier_id_fkey
            FOREIGN KEY (last_modifier_id)
            REFERENCES public.account (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;
        '''
    )
    execute(statement)


def add_last_publisher_id_to_session():
    ''' A new 'last_publisher_id' column has been added to the 'session' table
    '''
    for column in inspector.get_columns('session'):
        if 'last_publisher_id' == column['name']:
            return

    statement = (
        '''
        ALTER TABLE session
            ADD COLUMN last_publisher_id integer;
        ALTER TABLE session
            ADD CONSTRAINT session_last_publisher_id_fkey
            FOREIGN KEY (last_publisher_id)
            REFERENCES public.account (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION;
        '''
    )
    execute(statement)


def hash_passwords():
    ''' We want the passwords stored in the account table to be encrypted
    '''
    accounts = session.query(model.Account).filter(
        sql.or_(
            sql.not_(model.Account.account_type == 'guest'),
            model.Account.account_type == None  # noqa: E711
        )
    )
    total = float(accounts.count())
    start = datetime.now()
    print(
        '{} - {} accounts to convert'.format(
            start.strftime('%Y/%m/%d %H:%M:%S'), int(total)
        )
    )
    cnt = 0
    for account in accounts:
        account.hash_password()
        cnt += 1
        if cnt % 500 == 0:
            print(
                '{} - {} accounts converted ({:2.2f}%)'.format(
                    datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    cnt,
                    cnt / total * 100,
                )
            )
            print('    {}'.format(account.loginname))
    print(
        '{} accounts processed. Finished after {}'.format(
            cnt,
            datetime.now() - start,
        )
    )
    commit()


def main():
    # It is always a good idea to run this one
    create_missing_tables()
    if euphorie_version < parse_version('10.0.1'):
        add_group_id_to_account()
        add_brand_to_session()
        add_group_id_to_session()
        add_published_to_session()
        add_last_modifier_id_to_session()
        add_last_publisher_id_to_session()
        hash_passwords()
    if euphorie_version < parse_version('10.0.2'):
        add_brand_to_group()

if __name__ == "__main__":
    main()
