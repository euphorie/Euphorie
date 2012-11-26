"""
Dirty tree tracking
-------------------

It can be useful to know if a content tree has any unpublished changes. This
behaviour manages that by tracking creation, deletion, moving and modification
of content objects and updating a dirty flag on the first parent object which
provides the :py:obj:`IDirtyTreeRoot` marker interface. The flag is reset on
succesfull workflow transitions.
"""

from Acquisition import aq_base
from Acquisition import aq_chain
from zope.interface import Interface
from five import grok
from zope.lifecycleevent import IObjectModifiedEvent
from zope.lifecycleevent import IObjectMovedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent


class IDirtyTreeRoot(Interface):
    """Marker interface for objects which act as the root of a *dirty tree*.
    """


def clearDirty(obj):
    """Explicitly clear the ditry flag on an object.
    """
    obj.dirty = False


def isDirty(obj):
    """Check if an object is dirty, ie it has modified children.
    """
    if not IDirtyTreeRoot.providedBy(obj):
        raise TypeError("Object does not provide IDirtyTreeRoot")

    return getattr(aq_base(obj), "dirty", False)


def _touchTree(parent):
    """Helper function to update the dirty flag of the first parent
    :py:obj:`IDirtyTreeRoot`.
    """
    for parent in aq_chain(parent):
        if IDirtyTreeRoot.providedBy(parent):
            parent.dirty = True


@grok.subscribe(Interface, IObjectMovedEvent)
def handleObjectMove(obj, event):
    """Event handler for object moves. This includes objects added
    to and removed from containers.
    """
    if event.oldParent is not None:
        _touchTree(event.oldParent)
    if event.newParent is not None:
        _touchTree(event.newParent)


@grok.subscribe(Interface, IObjectModifiedEvent)
def handleObjectModified(obj, event):
    """Event handler for object moves. This includes objects added
    to and removed from containers.
    """
    _touchTree(event.object)


@grok.subscribe(IDirtyTreeRoot, IActionSucceededEvent)
def handleSurveyPublish(obj, event):
    """Event handler for workflow events on a dirty tree root. This
    resets the dirty flag.
    """
    obj.dirty = False
