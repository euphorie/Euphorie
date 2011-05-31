import logging
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
