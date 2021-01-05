from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client."""
