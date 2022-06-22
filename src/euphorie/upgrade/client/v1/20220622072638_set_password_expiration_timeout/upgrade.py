from ftw.upgrade import UpgradeStep
from plone import api


class SetPasswordExpirationTimeout(UpgradeStep):
    """Set password expiration timeout."""

    def __call__(self):
        ppr = api.portal.get_tool("portal_password_reset")
        ppr.setExpirationTimeout(0.5)
