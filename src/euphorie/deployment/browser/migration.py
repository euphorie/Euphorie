# coding=utf-8
from Products.Five import BrowserView
from plone.app.upgrade.utils import loadMigrationProfile
from plone import api

import logging

log = logging.getLogger(__name__)


class PreparePy3(BrowserView):
    def __call__(self):
        # See https://community.plone.org/t/upgrade-to-5-2-failing-with-iatcttool-has-no-attribute-iro/8909/10
        # remove obsolete AT tools
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
            loadMigrationProfile(
                self.context, "profile-Products.ATContentTypes:uninstall"
            )
        except KeyError:
            pass

        return "Finished"
