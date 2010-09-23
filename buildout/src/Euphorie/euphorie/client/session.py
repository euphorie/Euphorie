import logging
from z3c.saconfig import Session
from AccessControl import getSecurityManager
from euphorie.client import model
from euphorie.client.cookie import getCookie
from euphorie.client.cookie import setCookie
from euphorie.client.cookie import deleteCookie
from euphorie.client.utils import getRequest
from euphorie.client.utils import getSecret
from euphorie.client.utils import RelativePath

log = logging.getLogger(__name__)
SESSION_COOKIE = "_eu_session"


class SessionManagerFactory(object):
    """Session management handling for the client.

    Never use this class directly: instead use the global
    :py:data:`SessionManager` instance.
    """

    @property
    def session(self):
        """The current active client session. If no session is active None
        is returned.

        :rtype: :py:class:`euphorie.client.model.SurveySession` or None
        """
        request=getRequest()
        if "euphorie.session" in request.other:
            return request.other["euphorie.session"]

        id=self.id
        if id is None:
            return None

        session=Session.query(model.SurveySession).get(id)
        request.other["euphorie.session"]=session
        return session


    def start(self, title, survey, account=None):
        """Create a new session and activate it.

        :param title: title for the new session.
        :type title: unicode
        :param survey: survey for which the session is being created
        :type survey: :py:class:`euphorie.content.survey.Survey`
        :rtype: :py:class:`euphorie.client.model.SurveySession` instance
        """
        if account is None:
            account=getSecurityManager().getUser()
        request=getRequest()
        zodb_path=RelativePath(request.client, survey)
        session=model.SurveySession(title=title, zodb_path=zodb_path, account=account)
        Session.add(session)
        Session.flush() # flush so we get a session id
        setCookie(request.response, getSecret(), SESSION_COOKIE, session.id)
        request.other["euphorie.session"]=session
        return session


    def resume(self, session):
        """Activate the given session.

        :param session: session to activate
        :type session: :py:class:`euphorie.client.model.SurveySession`
        """
        request=getRequest()
        request.other["euphorie.session"]=session
        setCookie(request.response, getSecret(), SESSION_COOKIE, session.id)


    def stop(self):
        """End the current active session.
        """
        request=getRequest()
        if "euphorie.session" in request.other:
            del request.other["euphorie.session"]
        deleteCookie(request.response, SESSION_COOKIE)



    @property
    def id(self):
        """The id of the current session, or None if there is no active session.

        :rtype: int or None
        """
        request=getRequest()
        if "euphorie.session" in request.other:
            return request.other["euphorie.session"].id

        session_id=getCookie(request, getSecret(), "_eu_session")

        try:
            return int(session_id)
        except TypeError:
            return None




SessionManager = SessionManagerFactory()
"""Global instance of :py:class:`SessionManagerFactory`.
"""


__all__ = ["SessionManager" ]

