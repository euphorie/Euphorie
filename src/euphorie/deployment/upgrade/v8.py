# -*- coding: UTF-8 -*-
from plone import api
from plone.dexterity import utils
from z3c.form.interfaces import IDataManager
from euphorie.content.user import IUser
from euphorie.content.passwordpolicy import EuphoriePasswordPolicy
from euphorie.deployment import setuphandlers
import logging
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
