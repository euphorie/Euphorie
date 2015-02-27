# -*- coding: UTF-8 -*-
from euphorie.content.user import IUser
from euphorie.deployment import setuphandlers
from euphorie.deployment.upgrade.utils import ColumnExists
from euphorie.client import model
from plone import api
from plone.dexterity import utils
from sqlalchemy.engine.reflection import Inspector
from z3c.form.interfaces import IDataManager
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
from sqlalchemy.exc import InternalError
import logging
import transaction
import zope.component

log = logging.getLogger(__name__)


def hash_passwords(context):
    """ Make sure IUser passwords are hashed before they're stored in the ZODB.
    """
    catalog = api.portal.get_tool('portal_catalog')
    ps = catalog(object_provides='euphorie.content.user.IUser')
    for p in ps:
        o = p.getObject()
        password = o.password
        if type(password) == str and len(password) == 60:
            log.info('Not hashing password for "%s". Appears to be hashed '
                     'already.' %  p.getPath())
            continue
        elif password is None:
            log.info('Not hashing password for "%s". No password set'
                    %  p.getPath())
            continue

        for schema in utils.iterSchemata(o):
            field = schema.get('password')
            if field and field.interface == IUser:
                dm = zope.component.getMultiAdapter(
                    (o, field), IDataManager).set(password)


def register_password_policy(context):
    setuphandlers.registerPasswordPolicy(context)


def add_column_to_account(context):
    """ Adds a new column to the Account table which indicates whether the
        account in question is a guest account, a converted guest account or
        neither.
    """
    session = Session()
    if ColumnExists(session, "account", "account_type"):
        log.info("account_type column already exists in Account table!")
        return

    log.info('Adding account_type column to Account table')
    q = "ALTER TABLE account ADD COLUMN account_type CHARACTER varying(16)";
    try:
        session.execute(q)
    except InternalError, e:
        # There might be previous SQL queries which failed due to the
        # account_type column not yet being in the Account table. For example,
        # the authenticate method in authentication.py does such a query.
        session.rollback()
        transaction.commit()
        session.execute(q)

    datamanager.mark_changed(session)
    transaction.get().commit()


def add_column_for_custom_risks(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c['name']
               for c in inspector.get_columns(model.Risk.__table__.name)]
    if 'is_custom_risk' not in columns:
        log.info('Adding is_custom_risk column for risks')
        session.execute(
            "ALTER TABLE %s ADD is_custom_risk BOOL NOT NULL DEFAULT FALSE" %
            model.Risk.__table__.name)
        datamanager.mark_changed(session)
