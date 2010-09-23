"""
Publication
-----------

This behaviour prevents deletion of published objects. Since external systems
may reference a survey item once it has been published it should not be
possible to delete that item. The :obj:`IPublishRemovalProtection` behaviour
manages this with help from the :obj:`CheckObjectRemoval` event handler.

If the current user has the *Euphorie: Delete published content* deletion is
allowed. This makes it possible for site managers to delete content.
"""

from AccessControl import Unauthorized
from OFS.interfaces import IObjectWillBeRemovedEvent
from OFS.interfaces import IObjectClonedEvent
from OFS.event import ObjectClonedEvent
from zope.component import adapter
from zope.interface import implements
from Products.CMFCore.utils import _checkPermission
from zope import schema
from euphorie.content import MessageFactory as _
from plone.directives import form


class IPublishRemovalProtection(form.Schema):
    """Prevent an object from being deleted after it is published.

    Once a survey item has been published it might be referenced by
    external systems. To prevent such references from breaking this
    behaviour prevents objects from being deleted after they have
    been published. This is implemented through the :obj:`
    """

    published = schema.Bool(
            title = _(u"Published"),
            description = _(u"Flag indicating if this object has ever been "
                            u"published. Published objects can not be "
                            u"deleted, only marked as deprecated."),
            default = False,
            required = True)
    form.omitted("published")


@adapter(IPublishRemovalProtection, IObjectWillBeRemovedEvent)
def CheckObjectRemoval(obj, event):
    """Pre-removal event handler.

    This event handler is triggered for all objects with a
    :obj:`IPublishRemovalProtection` marker before they are removed.
    It checks if the *published* flag is set, and if so it raises
    an `Unauthorized` exception to pevent deletion.

    If the current user has the *Euphorie: Delete published content*
    deletion is allowed.
    """

    if getattr(obj, "published", False) and \
            not _checkPermission("Euphorie: Delete published content", obj):
        raise Unauthorized("Deletion of published content is not allowed")



class IObjectPublishedEvent(IObjectClonedEvent):
    """An object has been published by copying it to the client area."""


class ObjectPublishedEvent(ObjectClonedEvent):
    """An object has been published by copying it to the client area."""
    implements(IObjectPublishedEvent)


@adapter(IPublishRemovalProtection, IObjectPublishedEvent)
def ObjectPublished(obj, event):
    """Set published flag for all items with IPublishRemovalProtection behaviour.

    Note that we do not have to recurse into children ourselves: the
    `IObjectPublishedEvent` event is derived from `IObjectCopiedEvent`,
    which `Products.CMFCore` re-dispatches to all children.
    """
    obj.published=True
