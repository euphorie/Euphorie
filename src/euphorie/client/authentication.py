import logging
import traceback
import urllib
import sqlalchemy.exc
from z3c.saconfig import Session
from Acquisition import aq_parent
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from OFS.Cache import Cacheable
from zope.publisher.interfaces.browser import IBrowserView
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.utils import createViewName
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client import model


log = logging.getLogger(__name__)


def graceful_recovery(default=None, log_args=True):
    """Decorator to safely use SQLAlchemy in PAS plugins. This decorator
    makes sure SQL exceptions are caught and logged.

    Code from Malthe Borch's pas.plugins.sqlalchemy package.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                value = func(*args, **kwargs)
            except sqlalchemy.exc.SQLAlchemyError, e:
                if log_args is False:
                    args = ()
                    kwargs = {}

                formatted_tb = traceback.format_exc()

                try:
                    exc_str = str(e)
                except:
                    exc_str = "<%s at 0x%x>" % ( e.__class__.__name__, id(e))

                log.critical(
                    "caught SQL-exception: "
                    "%s (in method ``%s``; arguments were %s)\n\n%s" % (
                    exc_str,
                    func.__name__, ", ".join(
                        [repr(arg) for arg in args] +
                        ["%s=%s" % (name, repr(value)) for (name, value) in kwargs.items()]
                        ), formatted_tb))
                return default
            return value
        return wrapper
    return decorator



manage_addEuphorieAccountPlugin = PageTemplateFile("templates/addPasPlugin", globals(), 
                __name__="manage_addEuphorieAccountPlugin")


def addEuphorieAccountPlugin(self, id, title='', REQUEST=None):
    """Add an EuphorieAccountPlugin to a Pluggable Authentication Service.
    """
    p=EuphorieAccountPlugin(id, title)
    self._setObject(p.getId(), p)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect("%s/manage_workspace"
                "?manage_tabs_message=Euphorie+Account+Manager+plugin+added." %
                self.absolute_url())


class EuphorieAccountPlugin(BasePlugin, Cacheable):
    meta_type = "Euphorie account manager"
    security = ClassSecurityInfo()

    manage_options = BasePlugin.manage_options + Cacheable.manage_options


    def __init__(self, id, title=None):
        self._setId(id)
        self.title=title

    #
    # IAuthenticationPlugin implementation
    #

    security.declarePrivate('authenticateCredentials')
    @graceful_recovery(log_args=False)
    def authenticateCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')

        if not login or not password:
            return None

        login = login.lower()
        accounts = Session().query(model.Account)\
                .filter(model.Account.loginname==login)\
                .filter(model.Account.password==password).count()

        if accounts==1:
            return (login, login)

    #
    # IUserFactoryPlugin implementation
    @graceful_recovery()
    def createUser(self, user_id, name):
        name = name.lower()
        account=Session().query(model.Account)\
                .filter(model.Account.loginname==name).first()
        return account


    #
    # IUserEnumerationPlugin implementation
    #
    @graceful_recovery()
    def enumerateUsers(self, id=None, login=None, exact_match=False,
                       sort_by=None, max_results=None, **kw):
        if not exact_match:
            return []
        
        if id and login and id!=login:
            return []

        login=login or id
        if self._isKnownAccount(login):
            return [dict(id=login, login=login)]

        return []

    # 
    # IChallengePlugin implementation
    #
    def challenge(self, request, response):
        if not IClientSkinLayer.providedBy(request):
            return False

        current_url=request.get("ACTUAL_URL", "")
        query=request.get("QUERY_STRING")
        if query:
            if not query.startswith("?"):
                query="?"+query
            current_url+=query

        context=request.PUBLISHED
        if IBrowserView.providedBy(context):
            context=aq_parent(context)

        login_url="%s/@@login?%s" % (context.absolute_url(), 
                urllib.urlencode(dict(came_from=current_url)))
        response.redirect(login_url, lock=True)
        return True


    #
    # Utility functiones
    #
    def _isKnownAccount(self, loginname):
        """Utility function to check if a loginname is valid."""
        viewname=createViewName("_isKnownAccount", loginname)
        keywords=dict(login=loginname)
        result=self.ZCacheable_get(view_name=viewname, keywords=keywords,
                default=None)
        if result is not None:
            return result

        matches=Session().query(model.Account)\
                .filter(model.Account.loginname==loginname).count()
        result=bool(matches)

        self.ZCacheable_set(result, view_name=viewname, keywords=keywords)
        return result


classImplements(
    EuphorieAccountPlugin,
    IAuthenticationPlugin,
    IChallengePlugin,
    IUserEnumerationPlugin,
    IUserFactoryPlugin)

InitializeClass(EuphorieAccountPlugin)

