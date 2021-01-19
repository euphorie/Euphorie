# coding=utf-8
from ftw.upgrade import UpgradeStep
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.behavior.registration import lookup_behavior_registration
from plone.browserlayer.interfaces import ILocalBrowserLayerType
from plone.dexterity.interfaces import IDexterityFTI

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


class RemoveArchetypesLeftovers(UpgradeStep):
    """Remove Archetypes Leftovers and persistent traces of collecive.indexing
    Run this BEFORE you migrate to plone5.2
    See https://community.plone.org/t/upgrade-to-5-2-failing-with-iatcttool-has-no-attribute-iro/8909/10  # noqa: E501
    """

    def __call__(self):
        portal = api.portal.get()
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
        try:
            loadMigrationProfile(portal, "profile-Products.ATContentTypes:uninstall")
        except KeyError:
            pass

        ptt = api.portal.get_tool("portal_types")
        ftis = [fti for fti in ptt.objectValues() if IDexterityFTI.providedBy(fti)]
        for fti in ftis:
            bad_behaviors = []
            for behavior in fti.behaviors:
                try:
                    lookup_behavior_registration(behavior)
                except Exception:
                    bad_behaviors.append(behavior)
            if bad_behaviors:
                behaviors = [x for x in fti.behaviors if x not in bad_behaviors]
                fti.behaviors = behaviors
                log.warning("Removed {} for FTI {}".format(bad_behaviors, fti.id))

        # Unregister persistent traces of collective.indexing
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

        # Also unregister collective.js.jquery util
        unregisterUtility(portal, ILocalBrowserLayerType, "collective.js.jqueryui")
