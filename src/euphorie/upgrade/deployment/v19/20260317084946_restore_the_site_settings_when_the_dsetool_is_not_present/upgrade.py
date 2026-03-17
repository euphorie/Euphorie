from ftw.upgrade import UpgradeStep
from importlib.util import find_spec
from logging import getLogger
from plone import api


logger = getLogger(__name__)


class RestoreTheSiteSettingsWhenTheDsetoolIsNotPresent(UpgradeStep):
    """Restore the site settings when the dsetool is not present."""

    def fixup_appconfigtile_navigation(self):
        """Check if the appconfigtile_navigation registry record contains
        the choice and option content types, and if so, remove them.
        """
        key = "plonetheme.nuplone.appconfigtile_navigation"
        value = api.portal.get_registry_record(key)
        if ", 'euphorie.choice', 'euphorie.option'" not in value:
            return

        logger.info(
            "Resetting the appconfigtile_navigation registry record "
            "to remove choice and option content types"
        )
        new_value = value.replace(", 'euphorie.choice', 'euphorie.option'", "")
        api.portal.set_registry_record(key, new_value)

    def fix_module_fti(self):
        """Check if the euphorie.module FTI contains the choice content type
        in its allowed content types, and if so, remove it.
        """
        fti = api.portal.get_tool("portal_types").getTypeInfo("euphorie.module")
        if "euphorie.choice" not in fti.allowed_content_types:
            return

        logger.info(
            "Resetting the allowed content types of the euphorie.module FTI "
            "to remove the choice content type"
        )
        new_allowed_content_types = tuple(
            ct for ct in fti.allowed_content_types if ct != "euphorie.choice"
        )
        fti.allowed_content_types = new_allowed_content_types

    def remove_option_content_type(self):
        """Ensure we do not have the euphorie.option content type"""
        portal_types = api.portal.get_tool("portal_types")
        if "euphorie.option" not in portal_types:
            return

        logger.info(
            "Removing the euphorie.option content type from the portal types tool"
        )
        portal_types._delObject("euphorie.option")

    def remove_choice_content_type(self):
        """Ensure we do not have the euphorie.choice content type"""
        portal_types = api.portal.get_tool("portal_types")
        if "euphorie.choice" not in portal_types:
            return

        logger.info(
            "Removing the euphorie.choice content type from the portal types tool"
        )
        portal_types._delObject("euphorie.choice")

    def __call__(self):
        try:
            find_spec("dsetool.policy")
        except ModuleNotFoundError:
            # Only restore the site settings if we don't have dsetool.policy
            self.fixup_appconfigtile_navigation()
            self.fix_module_fti()
            self.remove_option_content_type()
            self.remove_choice_content_type()
