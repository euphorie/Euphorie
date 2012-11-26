import logging
from sqlalchemy.sql import func
from htmllaundry import StripMarkup
from Products.CMFCore.utils import getToolByName
from euphorie.content.risk import EnsureInterface
from z3c.saconfig import Session
from euphorie.deployment.upgrade.utils import TableExists
from euphorie.deployment.upgrade.utils import ColumnExists
from euphorie.client import model
from zope.sqlalchemy import datamanager
import transaction


log = logging.getLogger(__name__)


def set_evaluation_method_interfaces(context):
    ct = getToolByName(context, "portal_catalog")
    risks = ct(portal_type="euphorie.risk")
    count = 0
    for brain in risks:
        log.debug("Updating interfaces for %s", brain.getPath())
        risk = brain.getObject()
        EnsureInterface(risk)
        count += 1
    log.info("Updated interfaces for %d risks", count)


def convert_solution_description_to_text(context):
    ct = getToolByName(context, "portal_catalog")
    risks = ct(portal_type="euphorie.solution")
    count = 0
    for brain in risks:
        log.debug("Updating description for %s", brain.getPath())
        try:
            solution = brain.getObject()
        except KeyError:
            log.error('Could not get object for %s', brain.getPath())
        description = StripMarkup(solution.description)
        if description != solution.description:
            solution.description = description
        count += 1
    log.info("Updated description for %d solutions", count)


def add_wp_column_to_company(context):
    session = Session()
    if TableExists(session, "company"):
        session.execute(
            "ALTER TABLE company ADD workers_participated bool DEFAULT NULL")
        model.metadata.create_all(session.bind, checkfirst=True)
        datamanager.mark_changed(session)
        transaction.get().commit()

    log.info("Added new column 'workers_participated' to table 'company'")


def lowercase_login(context):
    session = Session()
    session.query(model.Account).update(
                    {'loginname': func.lower(model.Account.loginname)},
                    synchronize_session=False)
    datamanager.mark_changed(session)


def add_has_description_column(context):
    session = Session()
    if ColumnExists(session, 'tree', 'has_description'):
        return

    transaction.get().commit()
    session.execute(
            "ALTER TABLE tree ADD has_description bool DEFAULT 'f'")
    model.metadata.create_all(session.bind, checkfirst=True)
    datamanager.mark_changed(session)
    transaction.get().commit()
    log.info("Added new column 'has_description' to table 'tree'")
