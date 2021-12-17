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
from six.moves.urllib.parse import parse_qs
from six.moves.urllib.parse import urlencode
from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import urlsplit
from z3c.saconfig import Session
from zExceptions import Unauthorized
from zope.lifecycleevent import notify

import datetime
import logging
import os
import re
import six


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
            if isinstance(lang, six.string_types):
                lang = [lang]
            setLanguage(self.request, self.context, lang=lang[0])

    def login(self, account, remember):
        pas = getToolByName(self.context, "acl_users")
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

    def transferGuestSession(self, account_id):
        """Transfer session(s) from guest account to an existing user account"""
        if not account_id:
            return
        account = get_current_account()
        sessions = Session.query(model.SurveySession).filter(
            model.SurveySession.account_id == account_id
        )
        for session in sessions:
            session.account_id = account.id

    def is_valid_password(self, password):
        if (
            len(password) < 12
            or not re.search("[A-Z]", password)
            or not re.search("[a-z]", password)
            or not re.search("[1-9]", password)
        ):
            return False
        return True

    def check_password_policy(self, password):
        if not self.is_valid_password(password):
            return _(
                "error_password_policy_violation",
                default=(
                    u"The password needs to be at least 12 characters long and "
                    u"needs to contain at least one lower case letter, one upper "
                    u"case letter and one digit."
                ),
            )

    def _tryRegistration(self):
        if not self.webhelpers.allow_self_registration:
            raise Unauthorized("No self registration allowed.")
        form = self.request.form
        loginname = form.get("email")
        if not loginname:
            self.errors["email"] = _(
                "error_missing_email", default=u"Please enter your email address"
            )
        elif not EMAIL_RE.match(loginname):
            self.errors["email"] = _(
                "error_invalid_email", default=u"Please enter a valid email address"
            )
        if not form.get("password1"):
            self.errors["password"] = _(
                "error_missing_password", default=u"Please enter a password"
            )
        elif form.get("password1") != form.get("password2"):
            self.errors["password"] = _(
                "error_password_mismatch", default=u"Passwords do not match"
            )
        else:
            policy_error = self.check_password_policy(form.get("password1"))
            if policy_error:
                self.errors["password"] = policy_error
        if not form.get("terms"):
            self.errors["terms"] = _(
                "error_terms_not_accepted",
                default=u"An accout can only be created for you if you accept the "
                u"terms and conditions.",
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
                default=u"An account with this email address already exists.",
            )
            return False

        pm = getToolByName(self.context, "portal_membership")
        if pm.getMemberById(loginname) is not None:
            self.errors["email"] = _(
                "error_email_in_use",
                default=u"An account with this email address already exists.",
            )
            return False

        guest_account_id = self.request.form.get("guest_account_id")
        if guest_account_id:
            account = get_current_account()
            account.loginname = loginname
            account.password = form.get("password1")
            account.account_type = config.CONVERTED_ACCOUNT
            account.created = datetime.datetime.now()
            account.tc_approved = 1
            msg = _(
                "An account was created for you with email address ${email}",
                mapping={"email": loginname},
            )
            api.portal.show_message(msg, self.request, "success")

        else:
            account = model.Account(
                loginname=loginname, password=form.get("password1"), tc_approved=1
            )
        Session().add(account)
        log.info("Registered new account %s", loginname)
        v_url = urlsplit(self.request.URL + "/success").path.replace("@@", "")
        trigger_extra_pageview(self.request, v_url)
        return account

    def __call__(self):
        context = aq_inner(self.context)
        self.errors = {}

        form = self.request.form

        came_from = form.get("came_from")
        if came_from:
            if isinstance(came_from, list):
                # If came_from is both in the querystring and the form data
                came_from = came_from[0]
        else:
            # Set to country url
            came_from = self.webhelpers.country_url
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
                if (
                    isinstance(account, model.Account)
                    and account.getUserName() == form.get("__ac_name", "").lower()
                ):
                    self.transferGuestSession(form.get("guest_account_id"))
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
                        "{0}/terms-and-conditions?{1}".format(
                            context.absolute_url(),
                            urlencode({"came_from": came_from}),
                        )
                    )
                else:
                    self.request.RESPONSE.redirect(came_from)
                return

        self.reset_password_request_url = "{0}/@@reset_password_request?{1}".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )
        self.register_url = "{0}/@@login#registration?{1}".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )
        self.tryout_url = "{0}/@@tryout?{1}".format(
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )

        return self.index()

    def get_image_version(self, name):
        """Needed on the reports overview shown to the guest user
        (view name: @@register_session)
        """
        fdir = os.path.join(
            os.path.dirname(__file__), os.path.join("..", "resources", "media")
        )
        lang = getattr(self.request, "LANGUAGE", "en")
        fname = "{0}_{1}".format(name, lang)
        if os.path.isfile(os.path.join(fdir, fname + ".png")):
            return fname
        return name


class Tryout(SessionsView, Login):
    """Create a guest account

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
    """Create a guest session

    View name: @@new-session-test.html
    """

    def __call__(self):
        self.allow_guest_accounts = api.portal.get_registry_record(
            "euphorie.allow_guest_accounts", default=False
        )
        context = aq_inner(self.context)
        came_from = self.request.form.get("came_from")
        if came_from:
            if isinstance(came_from, list):
                # If came_from is both in the querystring and the form data
                came_from = came_from[0]
        else:
            came_from = context.absolute_url()
        self.register_url = "%s/@@login?%s#registration" % (
            context.absolute_url(),
            urlencode({"came_from": came_from}),
        )
        setLanguage(self.request, self.context)
        if self.request.environ["REQUEST_METHOD"] == "POST":
            if not self.allow_guest_accounts:
                flash = IStatusMessage(self.request).addStatusMessage
                flash(
                    _(
                        u"Starting a test session is not available in this OiRA "
                        u"application."
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
