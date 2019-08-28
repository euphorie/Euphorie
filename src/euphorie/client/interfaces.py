from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client.
    """
