import logging
from Acquisition import aq_parent
from sqlalchemy.engine.reflection import Inspector
from zope.sqlalchemy import datamanager
from z3c.saconfig import Session
from euphorie.client.api.authentication import EuphorieAPIPlugin
from euphorie.client.setuphandlers import add_api_authentication_plugin
from euphorie.client.model import Account


log = logging.getLogger(__name__)


def add_api_authentication(context):
    siteroot = aq_parent(context)
    pas = siteroot.acl_users
    if pas.objectIds([EuphorieAPIPlugin.meta_type]):
        log.info('API authentication plugin already installed.')
        return

    add_api_authentication_plugin(pas)


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
