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
from Acquisition import aq_chain
from Acquisition import aq_parent
from euphorie.content.user import IUser
from plone import api
from plone.base.utils import safe_text
from plone.keyring.interfaces import IKeyManager
from Products.membrane.interfaces import IMembraneUserAuth
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
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
        login = credentials.get("login")
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

    def _validate_credentials_on_others(self, credentials):
        """Validate the credentials on other plugins.

        This is used to check if the credentials are valid according to other
        plugins. If the credentials are not valid, we do not authenticate.
        We try the acl_users at the Plone and Zope level.

        The credentials are not the original credentials that were extracted.
        We have updated them to have a valid 'login', other than the email
        address.
        """
        context = api.portal.get()
        for obj in aq_chain(context):
            if not hasattr(aq_base(obj), "acl_users"):
                return
            pas = obj.acl_users
            authenticators = pas.plugins.listPlugins(IAuthenticationPlugin)
            for authenticator_id, authenticator in authenticators:
                if authenticator_id != self.id:
                    log.info("Checking %s at %s", authenticator_id, obj)
                    uid_and_name = authenticator.authenticateCredentials(credentials)
                    if uid_and_name is not None:
                        log.info(
                            "User %r authenticated by %s plugin.",
                            credentials["login"],
                            authenticator_id,
                        )
                        return uid_and_name

    def _maybe_let_backend_account_login_on_client(self, credentials):
        """Maybe let a backend account login on the client side.

        Scenario:

        * Susy is an editor.  She has an account on the backend with
          email address susy@example.com
        * She first logs in on the backend, with login name 'susy',
          and password 'secret'.
        * She improves a survey, and publishes it to the client.
        * Then she goes to the client side to check how the survey looks.
        * Problem: on the client side she needs to authenticate with
          an email address and password, but she has no client side account.

        We help here in the following way:

        * We check if the credentials are valid according to some other
          PAS plugin.
        * We check if there is an SQL account linked to her email.
        * We make her authenticated.  We ignore the password, because one
          of the other plugins has already told us the credentials are valid.

        This was introduced in https://github.com/euphorie/Euphorie/pull/857
        """
        # Only continue if the credentials are extracted by the
        # credentials_cookie_auth extractor.  Basically: only do this when
        # we are at the login form.
        extractor = credentials.get("extractor")
        if extractor != "credentials_cookie_auth":
            return

        # We should have a login name, and it should be an email address.
        email = credentials.get("login")
        if email is None:
            return
        # Let's be safe.
        email = email.strip()
        if not email or "@" not in email:
            return

        # Try to find a user with this email address.
        # Note: this does not find anything for root Zope users.
        pas = self._getPAS()
        result = pas.searchUsers(email=email, exact_match=True)
        if not result:
            return

        user = result[0]
        # Sanity check: does the email really match?  Not every plugin
        # may handle the search correctly.
        if "email" in user and user["email"] != email:
            log.warning(
                "Found user, but email %r does not match requested %r",
                user["email"],
                email,
            )
            return

        # Now we can update the credentials to try authenticating as this user.
        new_credentials = credentials.copy()
        new_credentials["login"] = user.get("login")

        # Check if the credentials are valid according to the other plugins.
        uid_and_name = self._validate_credentials_on_others(new_credentials)
        if not uid_and_name:
            log.warning(
                "Credentials for user %r are not valid according to other plugins. "
                "Refusing to login as a client SQL account.",
                email,
            )
            return

        # Take the validated login name.
        login = uid_and_name[1]

        # Check if we have a matching SQL account.
        sa_session = Session()
        sql_account = (
            sa_session.query(model.Account)
            .filter(model.Account.loginname == email)
            .first()
        )

        if not sql_account:
            log.warning(
                "No SQL account found for email %r. "
                "Maybe user %r needs to trigger creating an account first.",
                email,
                login,
            )
            # Maybe show a status message?  But if the user is not actually
            # a backend user, this might be confusing.
            # api.portal.show_message(
            #     "Please go to the backend and trigger creating an account."
            # )
            return

        # return sql_account.id, email
        # In our test with an LDAP user it seems we need the id in both cases.
        return sql_account.id, sql_account.id

    @security.private
    @graceful_recovery(log_args=False)
    def authenticateCredentials(self, credentials):
        if not IClientSkinLayer.providedBy(self.REQUEST):
            return None

        uid_and_login = self._authenticate_login(credentials)
        if uid_and_login is None:
            uid_and_login = self._authenticate_token(credentials)
        if uid_and_login is None:
            # Handles the use case of a backend user that visits the client
            # side.  We do this after the previous checks, so we don't mess
            # with the standard client login.
            uid_and_login = self._maybe_let_backend_account_login_on_client(credentials)
            if uid_and_login:
                log.debug(
                    "Successfully authenticated backend user on client: %r",
                    uid_and_login,
                )
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
        if not (id or login):
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
