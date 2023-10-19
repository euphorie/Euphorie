from zope.interface import implementer


try:
    from plone.base.interfaces.installable import INonInstallable
except ImportError:
    from Products.CMFPlone.interfaces import INonInstallable


@implementer(INonInstallable)
class HideEuphorieProducts:
    def getNonInstallableProfiles(self):
        return []

    def getNonInstallableProducts(self):
        return ["euphorie.content", "euphorie.client"]
