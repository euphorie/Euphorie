from zope.interface import Interface
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent
from OFS.interfaces import IObjectClonedEvent
from OFS.event import ObjectClonedEvent
from zope.interface import implements


class IObjectPublishedEvent(IObjectClonedEvent):
    """An object has been published by copying it to the client area."""


class ObjectPublishedEvent(ObjectClonedEvent):
    """An object has been published by copying it to the client area."""
    implements(IObjectPublishedEvent)


class ISurveyUnpublishEvent(IObjectEvent):
    """A survey is being removed from the client."""


class SurveyUnpublishEvent(ObjectEvent):
    """A survey is being removed from the client."""
    implements(ISurveyUnpublishEvent)


class IQuestionContainer(Interface):
    """Marker interface for objects that are used for grouping, but
    not for risks.
    """

class ICustomRisksModule(Interface):
    """Marker interface to mark a module specifically designated for adding
    custom risks.
    """
