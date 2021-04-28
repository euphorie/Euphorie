# coding=utf-8
from ftw.upgrade import UpgradeStep
from plone import api

import logging


log = logging.getLogger(__name__)


def unregisterUtility(context, iface, name=""):
    sm = context.getSiteManager()
    old = sm._utility_registrations.get((iface, name))
    if not old:
        return
    util = old[0]
    if name:
        sm.unregisterUtility(util, iface, name=name)
    else:
        sm.unregisterUtility(provided=iface)
    if util:
        del util
    if not name:
        sm.utilities.unsubscribe((), iface)
    if iface in sm.utilities.__dict__["_provided"]:
        del sm.utilities.__dict__["_provided"][iface]
    if iface in sm.utilities._subscribers[0]:
        del sm.utilities._subscribers[0][iface]
    sm._utility_registrations._p_changed = True
    sm.utilities._p_changed = True


class RemoveCollectiveIndexing(UpgradeStep):
    """Unregister persistent traces of collective.indexing"""

    def __call__(self):
        portal = api.portal.get()

        try:
            from collective.indexing.indexer import IPortalCatalogQueueProcessor
            from collective.indexing.interfaces import IIndexingConfig
        except ImportError:
            pass
        else:
            cp = api.portal.get_tool("portal_controlpanel")
            cp.unregisterConfiglet("IndexingSettings")
            for iface, name in (
                (IIndexingConfig, u""),
                (IPortalCatalogQueueProcessor, "portal-catalog"),
            ):
                unregisterUtility(portal, iface, name)

        # Remove yet more traces of c.indexing in the site manager
        sm = portal.getSiteManager()
        bad_ids = [
            "collective.indexing.interfaces.IIndexingConfig",
            "collective.indexing.indexer.IPortalCatalogQueueProcessor-portal-catalog",
        ]
        for bad_id in bad_ids:
            if bad_id in sm.objectIds():
                sm._delObject(bad_id)
                sm._p_changed = True
