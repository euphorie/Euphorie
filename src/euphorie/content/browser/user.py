from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client import config
from euphorie.client import model
from euphorie.content import MessageFactory as _
from plone import api
from Products.Five import BrowserView
from z3c.saconfig import Session
from zExceptions import Redirect
from zExceptions import Unauthorized
from zope.component import getMultiAdapter

import logging


logger = logging.getLogger(__name__)


class Lock(BrowserView):
    """Lock or unlock a User account.

    View name: @@lock
    """

    def __call__(self):
        if self.request.method != "POST":
            raise Unauthorized
        authenticator = getMultiAdapter(
            (self.context, self.request), name="authenticator"
        )
        if not authenticator.verify():
            raise Unauthorized

        self.context.locked = locked = self.request.form.get("action", "lock") == "lock"
        if locked:
            api.portal.show_message(
                _(
                    "message_user_locked",
                    default='Account "${title}" has been locked.',
                    mapping=dict(title=self.context.title),
                ),
                self.request,
                "success",
            )
        else:
            api.portal.show_message(
                _(
                    "message_user_unlocked",
                    default='Account "${title}" has been unlocked.',
                    mapping=dict(title=self.context.title),
                ),
                self.request,
                "success",
            )

        country = aq_parent(aq_inner(self.context))
        self.request.response.redirect("%s/@@manage-users" % country.absolute_url())


class CreateClientAccount(BrowserView):
    """Create client account for current backend user.

    View name: @@create-client-account
    """

    def check_authorized(self):
        """Check if the user is authorized.

        Raise Unauthorized otherwise.

        We could have called this method `is_authorized`, returned True or
        False, and let our caller raise Authorized.  But then in the traceback
        (if this exception is not ignored) you cannot see the reason why the
        user is not authorized.
        """
        if self.request.method != "POST":
            raise Unauthorized
        authenticator = api.content.get_view(
            "authenticator", self.context, self.request
        )
        if not authenticator.verify():
            raise Unauthorized
        if api.user.is_anonymous():
            raise Unauthorized

        return

    def check_root_zope_user(self):
        """Check if the authenticated user is a root zope user.

        If so: redirect with a message.

        The reason is that root Zope users may be able to set an email, but
        our EuphorieAccount plugin is not able to find the user back with
        this code:

            pas.searchUsers(email=email, exact_match=True)

        But in our @@settings page, a root Zope user can only set a password,
        not an email address, so this may not happen much in practice.
        Still, we should check.
        """
        user = api.user.get_current()
        pas = aq_parent(user)
        site = aq_parent(pas)
        # Check if site is a Plone site.
        # Alternative would be to check if this is an empty string,
        # because then we are at the Zope root:
        # "/".join(aq_parent(pas).getPhysicalPath()):
        is_plone_site = False
        try:
            is_plone_site = site.portal_type == "Plone Site"
        except AttributeError:
            pass
        if is_plone_site:
            return
        # The user exists in the root Zope acl_users.
        api.portal.show_message(
            message=_(
                "Creating a client account is not supported for root Zope users. "
                "Please login as a different user."
            ),
            request=self.request,
            type="error",
        )
        raise Redirect(self.context.absolute_url())

    def check_email(self):
        """Check if the authenticated user has an email address.

        If not: redirect with a message.
        """
        user = api.user.get_current()
        email = user.getProperty("email")
        if email:
            return email
        api.portal.show_message(
            message=_("Please set an email address first."),
            request=self.request,
            type="error",
        )
        portal_url = api.portal.get().absolute_url()
        self.request.response.redirect(f"{portal_url}/@@settings")

    def get_sql_account(self, email):
        """Get existing SQL account for this email address, if it exists."""
        return (
            Session()
            .query(model.Account)
            .filter(model.Account.loginname == email)
            .first()
        )

    def generate_password(self):
        """Generate random password."""
        reg = api.portal.get_tool(name="portal_registration")
        return reg.generatePassword()

    def create_account(self, email, password):
        """Create SQL account."""
        sql_account = model.Account(
            loginname=email,
            tc_approved=1,
            password=password,
            account_type=config.FULL_ACCOUNT,
        )
        Session().add(sql_account)
        return sql_account

    def __call__(self):
        # Check if the user is authorized.  This call may raise an Unauthorized.
        self.check_authorized()

        # Check if this is a root Zope user.  This call may raise a Redirect.
        self.check_root_zope_user()

        # Check if user has an email address.
        email = self.check_email()
        if not email:
            return

        # From here on, we always want to redirect to the current context at the end.
        self.request.response.redirect(self.context.absolute_url())

        # Check for existing account.
        sql_account = self.get_sql_account(email)
        if sql_account:
            api.portal.show_message(
                _(
                    "message_user_unlocked",
                    default="A client account for ${email} already exists.",
                    mapping=dict(
                        email=email,
                    ),
                ),
                request=self.request,
                type="warn",
            )
            return

        # Account does not exist.  Create it.
        password = self.generate_password()
        logger.info("Generated password %r for user %r.", password, email)
        sql_account = self.create_account(email, password)
        api.portal.show_message(
            message=_("A client account was created."), request=self.request
        )
