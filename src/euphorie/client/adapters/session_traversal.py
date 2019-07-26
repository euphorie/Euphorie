# coding=utf-8
from Acquisition import Implicit
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.content.survey import ISurvey
from OFS.Traversable import Traversable
from plone.memoize.instance import memoizedproperty
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.namespace import SimpleHandler


class ITraversedSurveySession(Interface):
    """ Interface for TraversedSurveySessions
    """


@implementer(ITraversedSurveySession)
class TraversedSurveySession(Implicit, Traversable):
    """ A traversable session object
    """

    def __init__(self, parent, session_id):
        self.__of__(parent)
        self.session_id = int(session_id)

    @memoizedproperty
    def session(self):
        return (
            Session.query(SurveySession)
            .filter(SurveySession.id == self.session_id)
            .one()
        )


@adapter(ISurvey, IBrowserRequest)
class SessionTraversal(SimpleHandler):

    factory = TraversedSurveySession

    def traverse(self, session_id, ignored):
        return self.factory(self.context, session_id)
