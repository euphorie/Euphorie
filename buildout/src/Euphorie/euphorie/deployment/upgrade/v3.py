import logging
from htmllaundry import StripMarkup
from Products.CMFCore.utils import getToolByName
from euphorie.content.risk import EnsureInterface


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
        if 'client' in brain.getPath():
            import pdb; pdb.set_trace()
        try:
            solution = brain.getObject()
        except KeyError:
            log.error('Could not get object for %s', brain.getPath())
        description = StripMarkup(solution.description)
        if description != solution.description:
            solution.description = description
        count += 1
    log.info("Updated description for %d solutions", count)
