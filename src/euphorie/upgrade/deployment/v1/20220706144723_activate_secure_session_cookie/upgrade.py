from euphorie.deployment.setuphandlers import setupSecureSessionCookie
from ftw.upgrade import UpgradeStep
from plone import api


class ActivateSecureSessionCookie(UpgradeStep):
    """Activate secure session cookie."""

    def __call__(self):
        site = api.portal.get()
        setupSecureSessionCookie(site)
