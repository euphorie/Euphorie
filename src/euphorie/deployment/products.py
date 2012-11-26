from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable


class HideEuphorieProducts(object):
    implements(INonInstallable)

    def getNonInstallableProducts(self):
        return ["euphorie.content", "euphorie.client"]
