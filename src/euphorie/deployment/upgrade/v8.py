# -*- coding: UTF-8 -*-
from euphorie.client import MessageFactory as _
from euphorie.client import model
from euphorie.client.country import IClientCountry
from euphorie.client.publish import EnableCustomRisks
from euphorie.client.sector import IClientSector
from euphorie.content.user import IUser
from euphorie.deployment import setuphandlers
from euphorie.deployment.upgrade.utils import ColumnExists
from euphorie.deployment.upgrade.utils import TableExists
from plone import api
from plone.dexterity import utils
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import InternalError
from z3c.appconfig.interfaces import IAppConfig
from z3c.appconfig.utils import asBool
from z3c.form.interfaces import IDataManager
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
import logging
import transaction
import zope.component
import datetime

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
    except InternalError as e:
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


def make_risk_id_column_nullable(context):
    """ Make the risk_id column of the Risk table nullable.
        This is so that the user can create custom risks. These risks don't
        have dexterity counterparts in the survey, so we don't have a value for
        risk_id.
    """
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    log.info('Making the risk_id column of Risk table nullable')
    session.execute(
        "ALTER TABLE %s ALTER COLUMN risk_id DROP NOT NULL;" %
        model.Risk.__table__.name
    )
    datamanager.mark_changed(session)


def enable_longer_zodb_paths(context):
    session = Session()
    session.execute(
        "ALTER TABLE %s ALTER COLUMN zodb_path TYPE varchar(512);" %
        model.SurveyTreeItem.__table__.name
    )
    datamanager.mark_changed(session)


def enable_custom_risks_on_all_modules(context):
    """ """
    appconfig = zope.component.getUtility(IAppConfig)
    if not asBool(appconfig["euphorie"].get("allow_user_defined_risks")):
        log.warning(
            "Custom risks are not enabled. Set 'allow_user_defined_risks' to "
            "true in euphorie.ini for enabling them.")
        return
    portal = api.portal.get()
    client = portal.client
    count = 0
    for country in client.objectValues():
        if IClientCountry.providedBy(country):
            for sector in country.objectValues():
                if IClientSector.providedBy(sector):
                    for survey in sector.objectValues():
                        try:
                            is_new = EnableCustomRisks(survey)
                            count += 1
                            custom = getattr(survey, 'custom-risks', None)
                            if custom:
                                custom.title = _(u'title_other_risks', default=u"Added risks (by you)")
                                custom.description = _(
                                    u"description_other_risks",
                                    default=u"In case you have identified risks not included in "
                                    u"the tool, you are able to add them now:")
                                custom.question = _(
                                    u"question_other_risks",
                                    default=u"<p>Would you now like to add your own defined risks "
                                    u"to this tool?</p><p><strong>Important:</strong> In "
                                    u"order to avoid duplicating risks, we strongly recommend you "
                                    u"to go first through all the previous modules, if you have not "
                                    u"done it yet.</p><p>If you don't need to add risks, please select 'No.'</p>")
                            if is_new:
                                survey.published = (
                                    survey.id, survey.title, datetime.datetime.now())
                        except Exception as e:
                            log.error("Could not enable custom risks for module. %s" % e)
    log.info('All %d published surveys can now have custom risks.' % count)
    session = Session()
    if TableExists(session, "tree"):
        session.execute(
            "UPDATE tree SET title = 'title_other_risks' WHERE zodb_path ='custom-risks'")
        model.metadata.create_all(session.bind, checkfirst=True)
        datamanager.mark_changed(session)
        transaction.get().commit()
        log.info('Set correct title on all exisiting sessions for custom risks module.')


def drop_constraint_no_duplicates_in_tree(context):
    session = Session()
    if TableExists(session, "tree"):
        session.execute(
            "ALTER TABLE tree DROP CONSTRAINT no_duplicates")
        model.metadata.create_all(session.bind, checkfirst=True)
        datamanager.mark_changed(session)
        transaction.get().commit()
    log.info("Removed the constraint `no_duplicates` from table tree.")
