# -*- coding: UTF-8 -*-
from euphorie.content.solution import ISolution
from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from plone import api
from plone.dexterity.interfaces import IDexterityContainer

import logging

log = logging.getLogger(__name__)


def alembic_upgrade(context):
    alembic_upgrade_to("27")


def unify_action_fields_in_solution(context):
    def walk(node):
        for idx, sub_node in node.ZopeFind(node, search_sub=0):
            if ISolution.providedBy(sub_node):
                yield sub_node
            if IDexterityContainer.providedBy(sub_node):
                for sub_sub_node in walk(sub_node):
                    yield sub_sub_node

    def unifiy_fields(walker):
        count = 0
        for solution in walker:
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

    site = api.portal.get()
    for section in ["sectors", "client"]:
        walker = walk(getattr(site, section))
        log.info('Iterating over section "{}"'.format(section))
        unifiy_fields(walker)
