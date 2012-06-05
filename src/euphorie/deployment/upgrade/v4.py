import logging
from sqlalchemy.engine.reflection import Inspector
from Acquisition import aq_parent
from zope.sqlalchemy import datamanager
from z3c.saconfig import Session
from euphorie.client.model import Account
from euphorie.client.model import ActionPlan
from euphorie.client.setuphandlers import enable_plugin_and_move_to_top


log = logging.getLogger(__name__)


def add_actionplan_reference(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c['name']
               for c in inspector.get_columns(ActionPlan.__table__.name)]
    if 'reference' not in columns:
        log.info('Adding reference column for action plans')
        session.execute('ALTER TABLE action_plan ADD COLUMN reference TEXT')


def allow_empty_password(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = inspector.get_columns(Account.__table__.name)
    password = [c for c in columns if c['name'] == 'password'][0]
    if not password['nullable']:
        log.info('Dropping NOT NULL constraint for account.password')
        session.execute(
                'ALTER TABLE account ALTER COLUMN password DROP NOT NULL')
        datamanager.mark_changed(session)


def enable_extra_pas_interfaces(context):
    pas = aq_parent(context).acl_users
    enable_plugin_and_move_to_top(pas, pas.euphorie)
