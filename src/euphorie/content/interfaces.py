from OFS.event import ObjectClonedEvent
from OFS.interfaces import IObjectClonedEvent
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import IObjectEvent
from zope.interface.interfaces import ObjectEvent


class IEuphorieContentLayer(NuPloneSkin):
    """Marker interface for Euphorie content."""


class IObjectPublishedEvent(IObjectClonedEvent):
    """An object has been published by copying it to the client area."""


@implementer(IObjectPublishedEvent)
class ObjectPublishedEvent(ObjectClonedEvent):
    """An object has been published by copying it to the client area."""


class ISurveyUnpublishEvent(IObjectEvent):
    """A survey is being removed from the client."""


@implementer(ISurveyUnpublishEvent)
class SurveyUnpublishEvent(ObjectEvent):
    """A survey is being removed from the client."""


class IQuestionContainer(Interface):
    """Marker interface for objects that are used for grouping, but not for
    risks."""


class ICustomRisksModule(Interface):
    """Marker interface to mark a module specifically designated for adding
    custom risks."""
