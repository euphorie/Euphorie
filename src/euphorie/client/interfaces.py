from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import ObjectEvent
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client."""


class ICustomRisksModifiedEvent(Interface):
    """Custom risks were modified"""


@implementer(ICustomRisksModifiedEvent)
class CustomRisksModifiedEvent(ObjectEvent):
    """Custom risks were modified"""
