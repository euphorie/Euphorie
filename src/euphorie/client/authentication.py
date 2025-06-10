"""
Authentication
--------------

User account plugins and authentication.
"""

from . import model
from .interfaces import IClientSkinLayer
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Acquisition import aq_base
from Acquisition import aq_parent
from euphorie.client import config
from euphorie.content.user import IUser
from plone import api
from plone.base.utils import safe_text
from plone.keyring.interfaces import IKeyManager
from Products.membrane.interfaces import IMembraneUserAuth
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.tools.memberdata import MemberData
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IUserFactoryPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from urllib.parse import urlencode
from z3c.saconfig import Session
from zope.component import getUtility
from zope.publisher.interfaces.browser import IBrowserView

import hashlib
import hmac
import logging
import sqlalchemy.exc
import traceback


log = logging.getLogger(__name__)


class NotImplementedError(Exception):
    def __init__(self, message):
        self.message = message


def _get_user(context, login):
    membrane = api.portal.get_tool("membrane_tool")
    user = membrane.getUserObject(login=login)
    if not IUser.providedBy(user):
        return None
    else:
        return user


def generate_token(user):
    """Convenience utility to generate token for the user."""
    manager = getUtility(IKeyManager)
    hasher = hmac.new(manager.secret(), digestmod=hashlib.sha256)
    hasher.update(user.login)
    # Note that unlike authenticate_credentials we access the password
    # directly here. This is fine since here we do not care how the password
    # is stored: even if it is hashed the token will be fine.
    hasher.update(user.password.encode("utf-8"))
    return f"{user.login}-{hasher.hexdigest()}"


def authenticate_cms_token(context, token):
    try:
        (login, hash) = token.split("-")
    except ValueError:
        return None
    user = _get_user(context, login)
    if user is None or generate_token(user) != token:
        return None
    else:
        auth = IMembraneUserAuth(user, None)
        return (auth.getUserId(), auth.getUserName())


def graceful_recovery(default=None, log_args=True):
    """Decorator to safely use SQLAlchemy in PAS plugins. This decorator makes
    sure SQL exceptions are caught and logged.

    Code from Malthe Borch's pas.plugins.sqlalchemy package.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                value = func(*args, **kwargs)
            except sqlalchemy.exc.SQLAlchemyError as e:
                if log_args is False:
                    args = ()
                    kwargs = {}

                formatted_tb = traceback.format_exc()

                try:
                    exc_str = str(e)
                except Exception:
                    exc_str = f"<{e.__class__.__name__} at 0x{id(e):x}>"

                log.critical(
                    "caught SQL-exception: "
                    "%s (in method ``%s``; arguments were %s)\n\n%s"
                    % (
                        exc_str,
                        func.__name__,
                        ", ".join(
                            [repr(arg) for arg in args]
                            + [
                                f"{name}={repr(value)}"
                                for (name, value) in kwargs.items()
                            ]
                        ),
                        formatted_tb,
                    )
                )
                return default
            return value

        return wrapper

    return decorator


manage_addEuphorieAccountPlugin = PageTemplateFile(
    "templates/addPasPlugin", globals(), __name__="manage_addEuphorieAccountPlugin"
)


def addEuphorieAccountPlugin(self, id, title="", REQUEST=None):
    """Add an EuphorieAccountPlugin to a Pluggable Authentication Service."""
    p = EuphorieAccountPlugin(id, title)
    self._setObject(p.getId(), p)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace"
            "?manage_tabs_message=Euphorie+Account+Manager+plugin+added."
            % self.absolute_url()
        )


class EuphorieAccountPlugin(BasePlugin):
    meta_type = "Euphorie account manager"
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    def extractCredentials(self, request):
        """IExtractionPlugin implementation."""
        token = request.getHeader("X-Euphorie-Token")
        if token:
            return {"api-token": token}
        else:
            return {}

    @security.private
    def _authenticate_token(self, credentials):
        """IAuthenticationPlugin implementation."""
        token = credentials.get("api-token")
        if not token:
            return None
        account = authenticate_cms_token(self, token)
        return account

    @security.private
    def _authenticate_login(self, credentials):
        login = credentials.get("email_overrides_login") or credentials.get("login")
        password = credentials.get("password")
        account = authenticate(login, password)
        if account is not None:
            return (str(account.id), account.loginname)
        else:
            return None

    @security.private
    def _get_survey_session(self):
        for parent in self.REQUEST.other["PARENTS"]:
            if isinstance(parent, model.SurveySession):
                return parent
        else:
            return None

    def _validate_credentials_on_others(self, credentials, context=None):
        """Validate the credentials on other plugins.

        This is used to check if the credentials are valid according to other
        plugins. If the credentials are not valid, we do not create an account.
        """
        if context is None:
            context = api.portal.get()

        if hasattr(aq_base(context), "acl_users"):
            plugins = context.acl_users.plugins
            authenticators = plugins.listPlugins(IAuthenticationPlugin)
            for authenticator_id, authenticator in authenticators:
                if authenticator_id != self.id:
                    uid_and_name = authenticator.authenticateCredentials(credentials)
                    if uid_and_name is not None:
                        log.debug(
                            "User %r authenticated by %s plugin.",
                            credentials.get("login"),
                            authenticator_id,
                        )
                        return True

        # Let's see if we can find a parent context that has other
        # authenticator plugins.
        # This will be tipically Zope's user plougin.
        parent = aq_parent(context)
        if parent is None:
            # We reached the top of the hierarchy without finding a valid
            # authenticator.
            return False

        return self._validate_credentials_on_others(credentials, context=parent)

    def _create_account_if_missing(self, credentials):
        """Create a SQL account if it does not exist yet.

        The user must have an email property which will be used as the loginname
        on the client.
        """
        extractor = credentials.get("extractor")
        if extractor != "credentials_cookie_auth":
            # Only create an account if the credentials are extracted by the
            # credentials_cookie_auth extractor.
            return

        login = credentials.get("login")
        if not login:
            return

        user = api.user.get(username=login)

        if not isinstance(user, MemberData):
            return

        email = user.getProperty("email")
        if not email or login == email:
            log.warning(
                "No email address set for user %r. Cannot create a SQL account.",
                login,
            )
            return

        sa_session = Session()

        sql_account = (
            sa_session.query(model.Account)
            .filter(model.Account.loginname == email)
            .first()
        )

        if sql_account:
            credentials["login"] = email
            return

        password = credentials.get("password")
        if not password:
            # If no password is provided, we cannot create an account.
            log.warning(
                "No password provided for user %r. Cannot create a SQL account.",
                email,
            )
            return

        # If we have a password we need to check if it is valid
        # according to the other plugins.
        if not self._validate_credentials_on_others(credentials):
            log.warning(
                "Credentials for user %r are not valid according to other plugins. "
                "Refusing to create a SQL account.",
                login,
            )
            return

        # we want to use the email to login to the client.
        credentials["email_overrides_login"] = email

        sql_account = model.Account(
            loginname=email,
            tc_approved=1,
            password=password,
            account_type=config.FULL_ACCOUNT,
        )
        sa_session.add(sql_account)
        log.info("A SQL account %r was created for user %r.", email, login)

    @security.private
    @graceful_recovery(log_args=False)
    def authenticateCredentials(self, credentials):
        if not IClientSkinLayer.providedBy(self.REQUEST):
            return None

        # Handles the use case of a backend user that has not yet
        # been created in the SQL database.
        self._create_account_if_missing(credentials)

        uid_and_login = self._authenticate_login(credentials)
        if uid_and_login is None:
            uid_and_login = self._authenticate_token(credentials)
        if uid_and_login is not None:
            session = self._get_survey_session()
            if session is not None:
                # Verify if current session matches the user. This prevents
                # a cookie hijack attack.
                if str(session.account_id) != uid_and_login[0]:
                    return None
            return uid_and_login
        else:
            return None

    @graceful_recovery()
    def createUser(self, user_id, name):
        """IUserFactoryPlugin implementation."""
        # It only happens with a call from the authomatic plugin that name
        # is empty. In that case, user_id is actually the user's loginname.
        # Force a an explicit search by loginname in that case.
        # Reason: we have users with a loginname that is an integer (!). In such
        # a case, query like `get(user_id)` matches the 'id' column in Account
        # first. If the loginname that is an integer also corresponds to an id
        # in the Account table, we would find the wrong user.
        if not IClientSkinLayer.providedBy(self.REQUEST):
            return None
        if not name:
            return (
                Session()
                .query(model.Account)
                .filter(model.Account.loginname == user_id)
                .one()
            )
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return None
        return Session().query(model.Account).get(user_id)

    @graceful_recovery()
    def enumerateUsers(
        self,
        id=None,
        login=None,
        exact_match=False,
        sort_by=None,
        max_results=None,
        **kw,
    ):
        """IUserEnumerationPlugin implementation."""
        if not exact_match:
            return []
        if not IClientSkinLayer.providedBy(self.REQUEST):
            return []

        query = Session().query(model.Account)
        if id is not None:
            try:
                query = query.filter(model.Account.id == int(id))
            except ValueError:
                return []
        if login:
            query = query.filter(model.Account.loginname == login)
        account = query.first()
        if account is not None:
            return [{"id": str(account.id), "login": account.loginname}]
        return []

    def updateUser(self, user_id, login_name):
        """Changes the user's username. New method available since Plone 4.3.
        Euphorie doesn't support this.

        :returns: False
        """
        return False

    def updateEveryLoginName(self, quit_on_first_error=True):
        """Update login names of all users to their canonical value.

        This should be done after changing the login_transform
        property of PAS.

        You can set quit_on_first_error to False to report all errors
        before quitting with an error.  This can be useful if you want
        to know how many problems there are, if any.

        :raises: NotImplementedError
        """
        raise NotImplementedError(
            "updateEveryLoginName method is not implemented by Euphorie"
        )

    def challenge(self, request, response):
        """IChallengePlugin implementation."""
        if not IClientSkinLayer.providedBy(request):
            return False

        current_url = request.get("ACTUAL_URL", "")
        query = request.get("QUERY_STRING")
        if query:
            if not query.startswith("?"):
                query = "?" + query
            current_url += query

        context = request.get("PUBLISHED")
        if not context:
            log.error(
                "Refusing to authenticate because no context has been found in %r",  # noqa: E501
                request,
            )
            return False
        if IBrowserView.providedBy(context):
            context = aq_parent(context)

        # In case of a deep link (anything deeper than to the country), open
        # the login form directly.
        deep_link = False
        try:
            webhelpers = api.content.get_view("webhelpers", context, request)
        except Exception:
            pass
        else:
            path = current_url.split(webhelpers.client_url)[-1]
            elems = [item for item in path.split("/") if item]
            if len(elems) > 1:
                deep_link = True

        login_url = "{url}/@@login?{came_from}{fragment}".format(
            url=context.absolute_url(),
            came_from=urlencode(dict(came_from=current_url)),
            fragment="#login" if deep_link else "",
        )
        response.redirect(login_url, lock=True)
        return True


def authenticate(login, password):
    """Try to authenticate a user using the given login and password.

    :param unicode login: login name
    :param unicode password: users password
    :return: :py:class:`Account <euphorie.client.model.Account>` instance

    If the credentials are valid the matching account is returned. For invalid
    credentials None is returned instead.
    """
    if not login or not password:
        return None
    password = safe_text(password)

    login = login.lower()
    accounts = Session().query(model.Account).filter(model.Account.loginname == login)
    for account in accounts:
        if account.verify_password(password):
            return account


classImplements(
    EuphorieAccountPlugin,
    IAuthenticationPlugin,
    IChallengePlugin,
    IExtractionPlugin,
    IUserEnumerationPlugin,
    IUserFactoryPlugin,
)

InitializeClass(EuphorieAccountPlugin)
