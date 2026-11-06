from plone.base.interfaces.installable import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HideEuphorieProducts:
    def getNonInstallableProfiles(self):
        return []

    def getNonInstallableProducts(self):
        return ["euphorie.content", "euphorie.client"]
