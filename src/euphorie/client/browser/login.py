"""
Login
-----

Register new users, login/logout, create a "Guest user" account and convert
existing guest accounts to normal accounts.
"""

from ..country import IClientCountry
from ..utils import setLanguage
from .conditions import approvedTermsAndConditions
from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.client import config
from euphorie.client import MessageFactory as _
from euphorie.client import model
from euphorie.client.browser.country import SessionsView
from euphorie.client.model import get_current_account
from euphorie.content.survey import ISurvey
from plone import api
from plone.memoize.view import memoize
from plone.session.plugins.session import cookie_expiration_date
from plonetheme.nuplone.tiles.analytics import trigger_extra_pageview
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.PlonePAS.events import UserLoggedInEvent
from Products.statusmessages.interfaces import IStatusMessage
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlsplit
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope.lifecycleevent import notify

import datetime
import logging
import os
import re


log = logging.getLogger(__name__)

# I know this is a stupid regular expression, but it Works For Us(tm)
EMAIL_RE = re.compile(
    r"[_a-z0-9+-]+(\.[_a-z0-9+-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})",
    re.IGNORECASE,
)


class Login(BrowserView):
    error = False
    errors = {}

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def setLanguage(self, came_from):
        qs = urlparse(came_from)[4]
        params = parse_qs(qs)
        lang = params.get("language")
        if not lang:
            if IClientCountry.providedBy(self.context):
                lang = getattr(self.context, "language", None)
            elif ISurvey.providedBy(self.context):
                lang = self.context.language
        if lang:
            if isinstance(lang, str):
                lang = [lang]
            setLanguage(self.request, self.context, lang=lang[0])

    def login(self, account, remember):
        pas = getToolByName(self.context, "acl_users")
        with api.env.adopt_user(username=account.getUserName()):
            pas.updateCredentials(
                self.request,
                self.request.RESPONSE,
                account.loginname,
                account.password,
            )
        notify(UserLoggedInEvent(account))
        if remember:
            self.request.RESPONSE.cookies["__ac"]["expires"] = cookie_expiration_date(
                120
            )  # noqa: E501
            self.request.RESPONSE.cookies["__ac"]["max_age"] = (
                120 * 24 * 60 * 60
            )  # noqa: E501

    def transferGuestSession(self):
        """Transfer session(s) from guest account to an existing user account.

        The guest account is expected to go the login form as an authenticated user.

        For this reason we can know from the session plugin who he is even
        if during the request process we are now logged in as a new user.
        """
        new_account = get_current_account()
        if new_account is None:
            # We are not logged in with a postgres account,
            # so we cannot transfer any session
            return

        plugin = self.context.acl_users.session
        old_credentials = plugin.authenticateCredentials(
            plugin.extractCredentials(self.request)
        )
        if old_credentials is None:
            # We came here as anonymous user, no need to proceed
            return

        old_authenticated_account_id = old_credentials[0]

        try:
            old_authenticated_account_id = int(old_authenticated_account_id)
        except (ValueError, TypeError):
            # This happens when we login as a backend user
            # and the account id happens to be the email address
            # These users are never guests accounts, so we can skip the transfer
            return

        old_account = (
            Session.query(model.Account)
            .filter(
                model.Account.account_type == config.GUEST_ACCOUNT,
                model.Account.id == old_authenticated_account_id,
            )
            .first()
        )

        if old_account is None:
            # We check that the previously authenticated user was actually
            # a guest account that has been converted.
            # This prevents that a regular logged in user A logs in as B
            # and then all the sessions are transferred to B
            return

        sessions = Session.query(model.SurveySession).filter(
            model.SurveySession.account_id == old_authenticated_account_id
        )
        for session in sessions:
            session.account_id = new_account.id
            session.touch()
        Session.delete(old_account)

    def is_valid_password(self, password):
        if (
            len(password) < 12
            or not re.search("[A-Z]", password)
            or not re.search("[a-z]", password)
            or not re.search("[0-9]", password)
        ):
            return False
        return True

    def check_password_policy(self, password):
        if not self.is_valid_password(password):
            return _(
                "error_password_policy_violation",
                default=(
                    "The password needs to be at least 12 characters long and "
                    "needs to contain at least one lower case letter, one upper "
                    "case letter and one digit."
                ),
            )

    def _tryRegistration(self):
        if not self.webhelpers.allow_self_registration:
            raise Unauthorized("No self registration allowed.")
        form = self.request.form
        loginname = form.get("email")
        if not loginname:
            self.errors["email"] = _(
                "error_missing_email", default="Please enter your email address"
            )
        elif not EMAIL_RE.match(loginname):
            self.errors["email"] = _(
                "error_invalid_email", default="Please enter a valid email address"
            )
        if not form.get("password1"):
            self.errors["password"] = _(
                "error_missing_password", default="Please enter a password"
            )
        elif form.get("password1") != form.get("password2"):
            self.errors["password"] = _(
                "error_password_mismatch", default="Passwords do not match"
            )
        else:
            policy_error = self.check_password_policy(form.get("password1"))
            if policy_error:
                self.errors["password"] = policy_error
        if not form.get("terms"):
            self.errors["terms"] = _(
                "error_terms_not_accepted",
                default="An accout can only be created for you if you accept the "
                "terms and conditions.",
            )

        if self.errors:
            return False

        # Check honeypot fields
        if form.get("user_name") or form.get("user_email"):
            return False

        session = Session()
        loginname = loginname.lower()
        account = (
            session.query(model.Account)
            .filter(model.Account.loginname == loginname)
            .count()
        )
        if account:
            self.errors["email"] = _(
                "error_email_in_use",
                default="An account with this email address already exists.",
            )
            return False

        pm = getToolByName(self.context, "portal_membership")
        if pm.getMemberById(loginname) is not None:
            self.errors["email"] = _(
                "error_email_in_use",
                default="An account with this email address already exists.",
            )
            return False

        account = get_current_account()
        if account and account.account_type == config.GUEST_ACCOUNT:
            account.loginname = loginname
            account.password = form.get("password1")
            account.account_type = config.CONVERTED_ACCOUNT
            account.created = datetime.datetime.now()
            account.tc_approved = 1
            account.first_name = form.get("first_name")
            account.last_name = form.get("last_name")
            msg = _(
                "An account was created for you with email address ${email}",
                mapping={"email": loginname},
            )
            api.portal.show_message(msg, self.request, "success")
        else:
            account = model.Account(
                loginname=loginname,
                password=form.get("password1"),
                tc_approved=1,
                first_name=form.get("first_name"),
                last_name=form.get("last_name"),
            )
            Session().add(account)
        log.info("Registered new account %r", loginname)
        v_url = urlsplit(self.request.URL + "/success").path.replace("@@", "")
        trigger_extra_pageview(self.request, v_url)
        return account

    def get_or_create_account_for_backend_user(self):
        """Get or create an account for the currently logged in backend user.

        This is used when a backend user tries to log in to the client.

        The account will be created if there is no record in the database
        with the same email address as the backend user.

        The account will be returned when the record exists but the password used
        is different to the one stored in the database (e.g. is an ldap password).
        """
        form_email = self.request.form.get("__ac_name", "")
        if not form_email:
            return

        user = api.user.get_current()
        pas_email = user.getProperty("email", "")

        if form_email != pas_email:
            return

        account = (
            Session()
            .query(model.Account)
            .filter(model.Account.loginname == form_email)
            .first()
        )
        if account:
            return account

        password = self.request.form.get("__ac_password", "")
        if not password:
            reg = api.portal.get_tool(name="portal_registration")
            password = reg.generatePassword()

        account = model.Account(
            loginname=form_email,
            tc_approved=1,
            password=password,
            account_type=config.FULL_ACCOUNT,
        )
        Session().add(account)
        Session().flush()
        return account

    def __call__(self):
        context = aq_inner(self.context)
        self.errors = {}

        form = self.request.form

        came_from = self.webhelpers.get_came_from(default=self.webhelpers.country_url)
        self.setLanguage(came_from)

        account = get_current_account()

        self.allow_guest_accounts = api.portal.get_registry_record(
            "euphorie.allow_guest_accounts", default=False
        )
        lang = api.portal.get_current_language()

        self.show_whofor = False if lang in ("fr",) else True
        self.show_what_to_do = False if lang in ("fr",) else True
        self.show_how_long = False if lang in ("fr",) else True
        self.show_why_register = True
        self.show_prepare = False if lang in ("fr",) else True

        if self.request.method == "POST":
            if form.get("action") == "login":

                # Handle backend users that login to the client
                if not account and not api.user.is_anonymous():
                    account = self.get_or_create_account_for_backend_user()

                if (
                    isinstance(account, model.Account)
                    and account.getUserName() == form.get("__ac_name", "").lower()
                ):
                    self.transferGuestSession()
                    self.login(account, bool(self.request.form.get("remember")))
                    v_url = urlsplit(self.request.URL + "/success").path.replace(
                        "@@", ""
                    )
                    trigger_extra_pageview(self.request, v_url)
                else:
                    self.error = True

            elif form.get("action") == "register":
                account = self._tryRegistration()
                if account:
                    pas = getToolByName(self.context, "acl_users")
                    with api.env.adopt_user(username=account.getUserName()):
                        pas.updateCredentials(
                            self.request,
                            self.request.response,
                            account.getUserName(),
                            account.password,
                        )
                else:
                    self.error = True

            if not self.error:
                if api.portal.get_registry_record(
                    "euphorie.terms_and_conditions", default=False
                ) and not approvedTermsAndConditions(account):
                    self.request.RESPONSE.redirect(
                        "{}/terms-and-conditions?{}".format(
                            context.absolute_url(),
                            urlencode({"came_from": came_from}),
                        )
                    )
                else:
                    self.request.RESPONSE.redirect(came_from)
                return

        self.reset_password_request_url = "{}/@@reset_password_request?{}".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )
        self.register_url = "{}/@@login#registration?{}".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )
        self.tryout_url = "{}/@@tryout?{}".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )

        return self.index()

    def get_image_version(self, name):
        """Needed on the reports overview shown to the guest user (view name:

        @@register_session)
        """
        fdir = os.path.join(
            os.path.dirname(__file__), os.path.join("..", "resources", "media")
        )
        lang = getattr(self.request, "LANGUAGE", "en")
        fname = f"{name}_{lang}"
        if os.path.isfile(os.path.join(fdir, fname + ".png")):
            return fname
        return name


class Tryout(SessionsView, Login):
    """Create a guest account.

    View name: @@tryout
    """

    def createGuestAccount(self):
        account = model.Account(
            loginname="guest-%s" % datetime.datetime.now().isoformat(),
            account_type=config.GUEST_ACCOUNT,
        )
        Session().add(account)
        return account

    def __call__(self):
        came_from = self.request.form.get("came_from")
        if not came_from:
            return self.request.response.redirect(api.portal.get().absolute_url())

        # Check honeypot fields
        if self.request.form.get("user_name") or self.request.form.get("user_email"):
            return self.request.response.redirect(api.portal.get().absolute_url())

        account = self.createGuestAccount()
        self.login(account, False)
        client_url = self.request.client.absolute_url()
        came_from = came_from.replace(client_url, "")
        if came_from.startswith("/"):
            came_from = came_from[1:]
        try:
            survey = self.context.restrictedTraverse(came_from)
        except KeyError:
            survey = None
        # This might happen if we're linking to a dedicated session. Try to
        # strip the session information from the came_from and try again
        except (AttributeError, Unauthorized):
            came_from = came_from.split("++session++")[0]
            try:
                survey = self.context.restrictedTraverse(came_from)
            except KeyError:
                survey = None
        if not ISurvey.providedBy(survey):
            return self.request.response.redirect(came_from)
        info = dict(action="new", survey=came_from)
        self._NewSurvey(info, account)


class CreateTestSession(Tryout):
    """Create a guest session.

    View name: @@new-session-test.html
    """

    def __call__(self):
        self.allow_guest_accounts = api.portal.get_registry_record(
            "euphorie.allow_guest_accounts", default=False
        )
        context = aq_inner(self.context)
        webhelpers = api.content.get_view(
            name="webhelpers", context=self.context, request=self.request
        )
        came_from = webhelpers.get_came_from(default=context.absolute_url())
        self.register_url = "{}/@@login?{}#registration".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )
        setLanguage(self.request, self.context)
        if self.request.environ["REQUEST_METHOD"] == "POST":
            if not self.allow_guest_accounts:
                flash = IStatusMessage(self.request).addStatusMessage
                flash(
                    _(
                        "Starting a test session is not available in this OiRA "
                        "application."
                    ),
                    "error",
                )
                self.request.response.redirect(came_from)
            else:
                form = self.request.form
                if form["action"] == "new":
                    account = self.createGuestAccount()
                    self.login(account, False)
                    self._NewSurvey(form, account)
        self._updateSurveys()
        return self.index()


class Logout(BrowserView):
    def __call__(self):
        pas = getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)

        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                break
        else:
            obj = self.request.client

        self.request.response.redirect(obj.absolute_url())
