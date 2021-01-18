from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HideEuphorieProducts(object):
    def getNonInstallableProducts(self):
        return ["euphorie.content", "euphorie.client"]
