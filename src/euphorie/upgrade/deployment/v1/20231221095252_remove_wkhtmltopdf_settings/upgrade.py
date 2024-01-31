from ftw.upgrade import UpgradeStep
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class RemoveWkhtmltopdfSettings(UpgradeStep):
    """Remove wkhtmltopdf settings."""

    def __call__(self):
        registry = getUtility(IRegistry)
        if "euphorie.wkhtmltopdf.options" in registry.records:
            del registry.records["euphorie.wkhtmltopdf.options"]
