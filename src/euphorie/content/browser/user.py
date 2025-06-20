from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client import config
from euphorie.client import model
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.content import MessageFactory as _
from plone import api
from Products.Five import BrowserView
from z3c.saconfig import Session
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

    def __call__(self):
        if IClientSkinLayer.providedBy(self.request):
            # This can only be called on the backend.
            raise Unauthorized
        if self.request.method != "POST":
            raise Unauthorized
        authenticator = getMultiAdapter(
            (self.context, self.request), name="authenticator"
        )
        if not authenticator.verify():
            raise Unauthorized
        if api.user.is_anonymous():
            raise Unauthorized

        # Check if user has an email address.
        user = api.user.get_current()
        email = user.getProperty("email")
        if not email:
            api.portal.show_message(
                message=_("Please set an email address first."),
                request=self.request,
                type="error",
            )
            portal_url = api.portal.get().absolute_url()
            self.request.response.redirect(f"{portal_url}/@@settings")
            return

        # From here on, we always want to redirect to the current context at the end.
        self.request.response.redirect(self.context.absolute_url())

        # Check for existing account.
        sa_session = Session()
        sql_account = (
            sa_session.query(model.Account)
            .filter(model.Account.loginname == email)
            .first()
        )
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

        else:
            # Generate random password.
            reg = api.portal.get_tool(name="portal_registration")
            password = reg.generatePassword()
            logger.info("Generated password %r for user %r.", password, email)
            sql_account = model.Account(
                loginname=email,
                tc_approved=1,
                password=password,
                account_type=config.FULL_ACCOUNT,
            )
            sa_session.add(sql_account)
            api.portal.show_message(
                message=_("A client account was created."), request=self.request
            )
        return "done"
