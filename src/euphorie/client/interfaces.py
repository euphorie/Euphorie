from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import ObjectEvent
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


INTERVAL_DAILY = "daily"
INTERVAL_HOURLY = "hourly"
INTERVAL_MINUTELY = "minutely"
INTERVAL_MANUAL = "manual"


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

    # The interval, this notification should be checked.
    # One of "daily", "hourly", "minutely"
    interval = Attribute("Interval")

    # Return True if this category is available for the current user.
    available = Attribute("Available")

    def notify():
        """Send a notification."""
