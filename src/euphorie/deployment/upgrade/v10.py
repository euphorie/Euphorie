# -*- coding: UTF-8 -*-
from euphorie.client import model
from sqlalchemy.engine.reflection import Inspector
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
import logging

log = logging.getLogger(__name__)


def add_column_for_existing_measures(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c['name']
               for c in inspector.get_columns(model.Risk.__table__.name)]
    if 'existing_measures' not in columns:
        log.info('Adding existing_measures column for risks')
        session.execute(
            "ALTER TABLE %s ADD existing_measures TEXT" %
            model.Risk.__table__.name)
        datamanager.mark_changed(session)
