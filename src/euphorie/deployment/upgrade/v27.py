# -*- coding: UTF-8 -*-
from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from plone import api

import logging

log = logging.getLogger(__name__)


def alembic_upgrade(context):
    alembic_upgrade_to("27")


def unify_action_fields_in_solution(context):
    pc = api.portal.get_tool("portal_catalog")
    solutions = pc(portal_type="euphorie.solution")
    count = 0
    for brain in solutions:
        log.debug("Updating description for %s", brain.getPath())
        try:
            solution = brain.getObject()
        except KeyError:
            log.error('Could not get object for %s', brain.getPath())
        action = solution.action_plan.strip()
        prevention_plan = solution.prevention_plan
        prevention_plan = prevention_plan and prevention_plan.strip() or ""
        if prevention_plan:
            action = u"{0}\n{1}".format(action, prevention_plan)
        solution.action = action
        count += 1
        if count % 100 == 0:
            log.info("Handled %d items" % count)
    log.info("Finished. Updated %d solutions" % count)