# coding=utf-8
# coding=utf-8
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from Products.Five import BrowserView

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
    sm.utilities._p_changed = True
    log.info("unregister Utility for {}".format(iface))


class RemoveDocuments(BrowserView):
    def __call__(self):
        portal = api.portal.get()
        log.info("RemoveDocuments")

        documents = portal.documents
        ids = [_id for _id in documents.objectIds()]
        documents.manage_delObjects(ids)
        documents.reindexObject()
        lt = api.portal.get_tool("portal_languages")
        for (code, name) in lt.listSupportedLanguages():
            documents.invokeFactory(
                "euphorie.documentation",
                code,
                title=name,
            )
            log.info("Added documentation folder for %s (%s)", name, code)


class UnistallCollectiveIndexing(BrowserView):
    def __call__(self):
        portal = api.portal.get()
        log.info("UnistallCollectiveIndexing")

        # Remove traces of c.indexing in the site manager
        sm = portal.getSiteManager()
        bad_ids = [
            "collective.indexing.interfaces.IIndexingConfig",
            "collective.indexing.indexer.IPortalCatalogQueueProcessor-portal-catalog",
        ]
        for bad_id in bad_ids:
            if bad_id in sm.objectIds():
                sm._delObject(bad_id)
                sm._p_changed = True

        # Unregister persistent traces of collective.indexing
        try:
            from collective.indexing.indexer import IPortalCatalogQueueProcessor
            from collective.indexing.interfaces import IIndexingConfig
        except ImportError:
            pass
        else:
            for iface, name in (
                (IIndexingConfig, u""),
                (IPortalCatalogQueueProcessor, "portal-catalog"),
            ):
                unregisterUtility(portal, iface, name)


class UnistallArchetypes(BrowserView):
    def __call__(self):
        portal = api.portal.get()
        log.info("UnistallArchetypes")
        loadMigrationProfile(portal, "profile-Products.ATContentTypes:uninstall")
        loadMigrationProfile(portal, "profile-Products.Archetypes:uninstall")

        tools = [
            "portal_languages",
            "portal_tinymce",
            "kupu_library_tool",
            "portal_factory",
            "portal_atct",
            "uid_catalog",
            "archetype_tool",
            "reference_catalog",
            "portal_metadata",
        ]
        for tool in tools:
            try:
                portal.manage_delObjects([tool])
                log.info("Deleted {}".format(tool))
            except AttributeError:
                log.info("{} not found".format(tool))

        # reapply uninstall to get rid of IATCTTool component
        loadMigrationProfile(portal, "profile-Products.ATContentTypes:uninstall")
