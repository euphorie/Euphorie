from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from zope.interface import implements


class HideEuphorieProducts(object):
    implements(INonInstallable)

    def getNonInstallableProducts(self):
        return ["euphorie.content", "euphorie.client"]
