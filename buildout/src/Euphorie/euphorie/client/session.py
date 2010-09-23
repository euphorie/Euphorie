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
    @property
    def session(self):
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
        if account is None:
            account=getSecurityManager().getUser()
        request=getRequest()
        zodb_path=RelativePath(request.client, survey)
        session=model.SurveySession(title=title, zodb_path=zodb_path, account=account)
        Session.add(session)
        Session.flush() # flush so we get a session id
        setCookie(getSecret(), SESSION_COOKIE, session.id)
        request.other["euphorie.session"]=session
        return session


    def resume(self, session):
        request=getRequest()
        request.other["euphorie.session"]=session
        setCookie(getSecret(), SESSION_COOKIE, session.id)


    def stop(self):
        request=getRequest()
        if "euphorie.session" in request.other:
            del request.other["euphorie.session"]
        deleteCookie(SESSION_COOKIE,)



    @property
    def id(self):
        request=getRequest()
        if "euphorie.session" in request.other:
            return request.other["euphorie.session"].id

        session_id=getCookie(getSecret(), "_eu_session")

        try:
            return int(session_id)
        except TypeError:
            return None




SessionManager = SessionManagerFactory()



__all__ = ["SessionManager" ]

