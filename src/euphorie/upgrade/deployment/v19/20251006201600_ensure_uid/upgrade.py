from Acquisition import aq_base
from ftw.upgrade import UpgradeStep
from plone import api
from plone.uuid.interfaces import ATTRIBUTE_NAME
from plone.uuid.interfaces import IUUIDGenerator
from zope.component import getUtility

import logging


logger = logging.getLogger(__name__)


class EnsureUidIsSet(UpgradeStep):
    """Ensure that all current content has a UID."""

    def __call__(self):
        """Upgrade step to set a UID if content does not have it yet."""
        logger.info("Ensuring all items have a UID.")
        catalog = api.portal.get_tool("portal_catalog")
        generator = getUtility(IUUIDGenerator)
        missing = 0
        for brain in catalog.getAllBrains():
            if brain.UID is not None:
                continue
            obj = brain.getObject()
            if getattr(aq_base(obj), ATTRIBUTE_NAME, None):
                obj.reindexObject(idxs=["UID"])
                continue
            missing += 1
            uuid = generator()
            setattr(obj, ATTRIBUTE_NAME, uuid)
            obj.reindexObject(idxs=["UID"])
            if missing % 1000 == 0:
                logger.info(
                    "Progress: Have set a UID on %d items that were missing it.",
                    missing,
                )
        logger.info("Have set a UID on %d items that were missing it.", missing)
