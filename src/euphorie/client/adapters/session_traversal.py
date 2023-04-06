from Acquisition import Implicit
from euphorie.client.model import Session
from euphorie.client.model import SessionRedirect
from euphorie.client.model import SurveySession
from euphorie.content.survey import ISurvey
from OFS.Traversable import Traversable
from plone.memoize.instance import memoizedproperty
from sqlalchemy.orm.exc import NoResultFound
from zExceptions import NotFound
from zExceptions import Redirect
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.namespace import SimpleHandler


class ITraversedSurveySession(Interface):
    """Interface for TraversedSurveySessions."""


@implementer(ITraversedSurveySession)
class TraversedSurveySession(Implicit, Traversable):
    """A traversable session object."""

    def __init__(self, parent, session_id):
        self.__of__(parent)
        self.session_id = int(session_id)
        self.id = f"++session++{self.session_id}"
        self.zodb_path = "/".join(parent.getPhysicalPath()[-3:])

    def getId(self):
        return self.id

    @memoizedproperty
    def session(self):
        try:
            return (
                Session.query(SurveySession)
                .filter(
                    SurveySession.id == self.session_id,
                    SurveySession.zodb_path == self.zodb_path,
                )
                .one()
            )
        except NoResultFound:
            raise NotFound


@adapter(ISurvey, IBrowserRequest)
class SessionTraversal(SimpleHandler):
    factory = TraversedSurveySession

    def get_redirect(self, session_id):
        query = Session.query(SessionRedirect).filter(
            SessionRedirect.old_session_id == session_id
        )
        if query.count() == 0:
            return None
        new_session_id = query.one().new_session_id
        return self.get_redirect(new_session_id) or new_session_id

    def traverse(self, session_id, ignored):
        new_session_id = self.get_redirect(session_id)
        if new_session_id:
            new_traversed_session = self.factory(self.context, new_session_id)
            raise Redirect(
                "/".join(
                    [new_traversed_session.__of__(self.context).absolute_url()]
                    + self.context.REQUEST.path
                )
            )
        return self.factory(self.context, session_id)
