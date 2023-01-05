"""
Unique ids
----------

Within a survey every element must have a unique identification number. This is
managed through two behaviours: a content type with the
:obj:`IIdGenerationRoot` behaviour acts as a id numbering boundary. All items
underneath this root will have a unique number. The `INameFromUniqueId
behaviour` indicates that a type's instances should get unique numbers.
"""

from Acquisition import aq_chain
from euphorie.content import MessageFactory as _
from plone.app.content.namechooser import NormalizingNameChooser
from Products.CMFCore.interfaces import IFolderish
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import Interface


class IIdGenerationRoot(Interface):
    """Marker interface for objects which act as the root for ids.

    Generated ids do not always need to be globally unique. Objects with
    this marked interface (or dexterity behaviour) act as uniqueness
    root.
    """


class INameFromUniqueId(Interface):
    """Marker interface for objects which should get a unique id.

    Objects with this interface automatically get a unique id when they
    are added to an container (as long as INameChooser is used). Ids are
    unique within the context of IIdGenerationRoot.
    """

    id = schema.TextLine(
        title=_("Identifier"),
        description=_("This is a unique identifier for this object."),
        required=True,
    )


def get_next_id(context, ids=None):
    for root in aq_chain(context):
        if IIdGenerationRoot.providedBy(root):
            break
    else:
        raise ValueError("No id generation root found")
    storage = IAnnotations(root, None)
    if storage is None:
        raise ValueError("Id generation root is not annotatable")
    current_max = storage.get("euphorie.content.behaviour.id", 1)
    if ids:
        current_max = max(current_max, max(ids) + 1)
    storage["euphorie.content.behaviour.id"] = current_max + 1
    return str(current_max)


@adapter(IFolderish)
class UniqueNameChooser(NormalizingNameChooser):
    """INameChooser for INameFromUniqueId objects.

    This implementation uses a simple increasing numerical id, starting
    with 1.
    """

    def _assertId(self, object):
        """Make sure the object has a unique id."""
        if getattr(object, "id", False):
            return
        object.id = get_next_id(self.context)

    def chooseName(self, name, object):
        if INameFromUniqueId.providedBy(object):
            self._assertId(object)
            return object.id
        else:
            return super().chooseName(name, object)
