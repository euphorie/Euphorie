"""
Deprecation
-----------

This behaviour implements a very simple deprecation system: objects can be
deprecated using a special deprecation workflow. Deprecated objects will be
skipped when publishing a survey, making them inaccessible in the clients. This
behaviour is managed via the `IDeprecatable` behaviour.
"""

from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent


class IDeprecatable(Interface):
    """Simple behaviour for deprecatable objects.
    """

    def deprecated():
        """Check if the object is deprecated. 
        """


class WorkflowDeprecatable(object):
    """Workflow based implementation for :obj:`IDeprecatable`.

    This implementation checks the workflow state to determine if an
    object has been deprecated. If the workflow state is set to
    `deprecated` the object will be considered to have been deprecated.
    """
    adapts(IDexterityContent)
    implements(IDeprecatable)

    def __init__(self, context):
        self.context=context

    @property
    def deprecated(self):
        wt=getToolByName(self.context, "portal_workflow", None)
        if wt is None:
            return False
        return wt.getInfoFor(self.context, "review_state")=="deprecated"

