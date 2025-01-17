"""Traverse a tree item. Tree items are polymorphic entities on the main table
from euphorie.client.model.SurveyTreeItem on the column type.

We have two possible objects:
- euphorie.client.model.Module (type `module`)
- euphorie.client.model.Risk (type `risk`)
"""

from euphorie.client.adapters.session_traversal import ITraversedSurveySession
from euphorie.client.model import Session
from euphorie.client.model import SurveyTreeItem
from zExceptions import NotFound
from zope.component import adapter
from zope.publisher.interfaces.browser import IBrowserRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse


@adapter(ITraversedSurveySession, IBrowserRequest)
class TraversedSessionPublishTraverser(DefaultPublishTraverse):
    """Traverser for the Survey session children."""

    def _make_path(self, pathid):
        return pathid.zfill(3)

    def publishTraverse(self, request, pathid):
        """Return a traversable SQL object."""
        query = (
            Session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session == self.context.session)
            .filter(SurveyTreeItem.path == self._make_path(pathid))
        )
        sqlobj = query.one()
        if sqlobj is None:
            raise NotFound
        return sqlobj.__of__(self.context)


@adapter(SurveyTreeItem, IBrowserRequest)
class SurveyTreeItemPublishTraverser(TraversedSessionPublishTraverser):
    """Traverser for the Survey session children."""

    def _make_path(self, pathid):
        return self.context.path + pathid.zfill(3)
