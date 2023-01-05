from euphorie.client import model
from euphorie.content.behaviour.uniqueid import get_next_id
from euphorie.content.solution import ISolution
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName
from sqlalchemy.engine.reflection import Inspector
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager

import logging


log = logging.getLogger(__name__)


def add_column_for_training_notes(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c["name"] for c in inspector.get_columns(model.Risk.__table__.name)]
    if "training_notes" not in columns:
        log.info("Adding training_notes column for risks")
        session.execute(
            "ALTER TABLE %s ADD training_notes TEXT" % model.Risk.__table__.name
        )
        datamanager.mark_changed(session)


def update_nav_types_registry(context):
    """There is a new registry record called plone.displayed_types that
    determines what types get shown in the navigation."""
    loadMigrationProfile(context, "profile-euphorie.deployment.upgrade:to_0020")


def migrate_existing_measures(context):
    ct = getToolByName(context, "portal_catalog")
    risks = ct(portal_type="euphorie.risk")
    count = 0
    for brain in risks:
        risk = brain.getObject()
        existing_measures = getattr(risk, "existing_measures", None)
        if existing_measures:
            solutions = [
                solution.description.strip()
                for solution in risk.values()
                if ISolution.providedBy(solution)
            ]
            for measure in existing_measures.splitlines():
                if measure.strip() not in solutions:
                    id = get_next_id(risk)
                    risk.invokeFactory("euphorie.solution", id)
                    solution = getattr(risk, id)
                    solution.description = measure
                    solution.action_plan = measure
                    count += 1
    log.info("Created %d Solutions", count)


def extend_zodb_path_field(context):
    session = Session()
    session.execute(
        "ALTER TABLE %s ALTER COLUMN zodb_path TYPE varchar(512);"
        % model.SurveySession.__table__.name
    )
    datamanager.mark_changed(session)
