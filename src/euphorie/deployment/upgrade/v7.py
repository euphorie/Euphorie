# -*- coding: UTF-8 -*-
from euphorie.client import model
from sqlalchemy.engine.reflection import Inspector
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
import logging

log = logging.getLogger(__name__)


def add_columns_to_company_survey(context):
    session = Session()
    inspector = Inspector.from_engine(session.bind)
    columns = [c['name']
               for c in inspector.get_columns(model.Company.__table__.name)]
    if 'needs_met' not in columns:
        log.info('Adding needs_met column for company')
        session.execute(
            "ALTER TABLE %s ADD needs_met BOOL " %
            model.Company.__table__.name)
        datamanager.mark_changed(session)
    if 'recommend_tool' not in columns:
        log.info('Adding recommend_tool column for company')
        session.execute(
            "ALTER TABLE %s ADD recommend_tool BOOL " %
            model.Company.__table__.name)
        datamanager.mark_changed(session)
