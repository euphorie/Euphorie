"""
Session
-------

Create and update sessions.
"""

import logging
from z3c.saconfig import Session
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl import getSecurityManager
from euphorie.client import model
from euphorie.client.cookie import getCookie
from euphorie.client.cookie import setCookie
from euphorie.client.cookie import deleteCookie
from euphorie.client.utils import getRequest
from euphorie.client.utils import getSecret

log = logging.getLogger(__name__)
SESSION_COOKIE = "_eu_session"


def create_survey_session(title, survey, account=None):
    """Create a new survey session.

    :param title: title for the new session.
    :type title: unicode
    :param survey: survey for which the session is being created
    :type survey: :py:class:`euphorie.content.survey.Survey`
    :rtype: :py:class:`euphorie.client.model.SurveySession` instance
    """
    if account is None:
        account = getSecurityManager().getUser()

    sector = aq_parent(aq_inner(survey))
    country = aq_parent(sector)
    zodb_path = '%s/%s/%s' % (country.id, sector.id, survey.id)
    survey_session = model.SurveySession(
            title=title,
            zodb_path=zodb_path,
            account=account)
    Session.add(survey_session)
    Session.flush()  # flush so we get a session id
    return survey_session


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
        request = getRequest()
        if "euphorie.session" in request.other:
            return request.other["euphorie.session"]

        id = self.id
        if id is None:
            return None

        session = Session.query(model.SurveySession).get(id)
        request.other["euphorie.session"] = session
        return session

    def start(self, title, survey, account=None):
        """Create a new session and activate it.

        :param title: title for the new session.
        :type title: unicode
        :param survey: survey for which the session is being created
        :type survey: :py:class:`euphorie.content.survey.Survey`
        :rtype: :py:class:`euphorie.client.model.SurveySession` instance
        """
        survey_session = create_survey_session(title, survey, account)
        request = getRequest()
        setCookie(request.response, getSecret(), SESSION_COOKIE,
                survey_session.id)
        request.other['euphorie.session'] = survey_session
        return survey_session

    def resume(self, session):
        """Activate the given session.

        :param session: session to activate
        :type session: :py:class:`euphorie.client.model.SurveySession`
        """
        account = aq_base(getSecurityManager().getUser())
        if session.account is not account:
            raise ValueError('Can only resume session for current user.')

        request = getRequest()
        request.other["euphorie.session"] = session
        setCookie(request.response, getSecret(), SESSION_COOKIE, session.id)

    def stop(self):
        """End the current active session.
        """
        request = getRequest()
        if "euphorie.session" in request.other:
            del request.other["euphorie.session"]
        deleteCookie(request.response, SESSION_COOKIE)
        setCookie(request.response, getSecret(), SESSION_COOKIE, '')

    @property
    def id(self):
        """The id of the current session, or None if there is no active
        session.

        This method does not perform any security checks.

        :rtype: int or None
        """
        request = getRequest()
        if "euphorie.session" in request.other:
            return request.other["euphorie.session"].id

        session_id = getCookie(request, getSecret(), "_eu_session")

        try:
            return int(session_id)
        except TypeError:
            return None


SessionManager = SessionManagerFactory()
"""Global instance of :py:class:`SessionManagerFactory`.
"""


__all__ = ["SessionManager"]
