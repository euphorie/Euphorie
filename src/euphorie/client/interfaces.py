from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import ObjectEvent
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client."""


class ICustomRisksModifiedEvent(Interface):
    """Custom risks were modified."""


@implementer(ICustomRisksModifiedEvent)
class CustomRisksModifiedEvent(ObjectEvent):
    """Custom risks were modified."""


class INotificationCategory(Interface):
    """A notification category adapter."""

    id = Attribute("Id")  # The id of the category
    title = Attribute("Title")  # The title of the category
    description = Attribute("Description")  # A description of the category

    def notify():
        """Send a notification."""
