# -*- coding: UTF-8 -*-
from euphorie.client import model
from plone.app.upgrade.utils import loadMigrationProfile
from sqlalchemy.engine.reflection import Inspector
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
import logging

log = logging.getLogger(__name__)


def add_column_for_training_notes(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c['name']
               for c in inspector.get_columns(model.Risk.__table__.name)]
    if 'training_notes' not in columns:
        log.info('Adding training_notes column for risks')
        session.execute(
            "ALTER TABLE %s ADD training_notes TEXT" %
            model.Risk.__table__.name)
        datamanager.mark_changed(session)


def update_nav_types_registry(context):
    ''' There is a new registry record called
    plone.displayed_types
    that determines what types get shown in the navigation
    '''
    loadMigrationProfile(
        context,
        'profile-euphorie.deployment.upgrade:to_0020'
    )
