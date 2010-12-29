from zope.interface import Interface
from OFS.interfaces import IObjectClonedEvent
from OFS.event import ObjectClonedEvent
from zope.interface import implements


class IObjectPublishedEvent(IObjectClonedEvent):
    """An object has been published by copying it to the client area."""


class ObjectPublishedEvent(ObjectClonedEvent):
    """An object has been published by copying it to the client area."""
    implements(IObjectPublishedEvent)


class IQuestionContainer(Interface):
    """Marker interface for objects that are used for grouping, but
    not for risks.
    """

