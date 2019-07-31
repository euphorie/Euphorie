# coding=utf-8
"""
Traverse a tree item.
Tree items are polymorphic entities on the main table
from euphorie.client.model.SurveyTreeItem on the column type

We have two possible objects:
- euphorie.client.model.Module (type `module`)
- euphorie.client.model.Risk (type `risk`)

"""
from euphorie.client.adapters.base import ITraversedSQLObject
from euphorie.client.adapters.session_traversal import ITraversedSurveySession
from Acquisition import Implicit
from euphorie.client.model import Session
from euphorie.client.model import SurveyTreeItem, Module, Risk
from OFS.Traversable import Traversable
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from zExceptions import NotFound
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse


class ITraversedSurveyTreeItem(ITraversedSQLObject):
    """ Base interface for SurveyTreeItem SQL objects
    """


class ITraversedModule(ITraversedSurveyTreeItem):
    """ Interface for Module objects coming from the SQL DB
    """


class ITraversedRisk(ITraversedSurveyTreeItem):
    """ Interface for Module objects coming from the SQL DB
    """


class TraversedTreeItem(Implicit, Traversable):
    sql_klass = SurveyTreeItem

    def __init__(self, parent, tree_item):
        self.aq_parent = parent
        self.__of__(parent)
        self.tree_item = (
            Session.query(SurveyTreeItem)
            .filter(
                and_(
                    self.sql_klass.id == tree_item.id,
                )
            )
            .one()
        )

    def getId(self):
        return str(self.tree_item.id)


@implementer(ITraversedModule)
class TraversedModule(TraversedTreeItem):
    """ A traversable module object
    """

    sql_klass = Module


@implementer(ITraversedRisk)
class TraversedRisk(TraversedTreeItem):
    """ A traversable risk object
    """

    sql_klass = Risk


@adapter(ITraversedSurveySession, IBrowserRequest)
class TraversedSessionPublishTraverser(DefaultPublishTraverse):
    """ Traverser for the Survey session children
    """

    def publishTraverse(self, request, tree_item_id):
        """ Return a traversable SQL object
        """
        # XXX Check if there is a polymorphic method that does that with one
        # query
        try:
            # First look for a generic tree item
            item = (
                Session.query(SurveyTreeItem)
                .filter(
                    and_(
                        SurveyTreeItem.id == tree_item_id,
                        SurveyTreeItem.session == self.context.session,
                    )
                )
                .one()
            )
        except NoResultFound:
            raise NotFound

        # if found look for the proper item type
        if item.type == "module":
            sql_klass = Module
        elif item.type == "risk":
            sql_klass = Risk
        else:
            raise Exception("Error unknown tree item %s" % tree_item_id)

        tree_item = (
            Session.query(sql_klass)
            .filter(
                and_(
                    sql_klass.id == tree_item_id,
                )
            )
            .one()
        )

        return tree_item.__of__(self.context)
