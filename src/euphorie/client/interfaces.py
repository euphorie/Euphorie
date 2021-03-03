from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.component.interfaces import ObjectEvent
from zope.interface import implements
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client."""


class ICustomRisksModifiedEvent(Interface):
    """Custom risks were modified"""


class CustomRisksModifiedEvent(ObjectEvent):

    implements(ICustomRisksModifiedEvent)
