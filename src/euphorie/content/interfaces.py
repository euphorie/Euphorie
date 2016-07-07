from OFS.event import ObjectClonedEvent
from OFS.interfaces import IObjectClonedEvent
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements
from zope.interface import Interface


class IEuphorieFormLayer(INuPloneFormLayer):
    """ Browser layer to indicate we want Euphorie form components."""


class IEuphorieContentSkinLayer(IEuphorieFormLayer, NuPloneSkin):
    """Marker interface for the CMS/Content editing skin."""


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
