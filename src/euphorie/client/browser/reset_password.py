from euphorie import MessageFactory as _
from euphorie.client.model import Account
from euphorie.client.utils import CreateEmailTo
from logging import getLogger
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize_contextless
from plone.schema import Email
from plone.supermodel import model
from Products.CMFPlone.PasswordResetTool import InvalidRequestError
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from requests.utils import is_ipv4_address
from urllib.parse import urlencode
from z3c.form import button
from z3c.form.form import EditForm
from z3c.saconfig import Session
from zope import schema
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.publisher.interfaces import IPublishTraverse

import smtplib


logger = getLogger(__name__)


class ResetPasswordFormSchema(model.Schema):
    new_password = schema.Password(
        title=_("label_new_password", default="Desired password"),
    )
    new_password_confirmation = schema.Password(
        title=_("label_confirm_password", default="Confirm your password"),
    )

    @invariant
    def validate_same_value(data):
        if data.new_password != data.new_password_confirmation:
            raise Invalid(_("Password doesn't compare with confirmation value"))


class ResetPasswordRequestSchema(model.Schema):
    email = Email(
        title=_("label_email", default="Email address"),
    )


class BaseForm(AutoExtensibleForm, EditForm):
    """Base class for password the reset forms."""

    title = ""
    description = ""

    @property
    def template(self):
        return self.index

    def redirect(self, target, msg="", msg_type="notice"):
        """Redirect the user to a meaningfull place and add a status
        message."""
        if msg:
            api.portal.show_message(msg, self.request, msg_type)
        self.request.response.redirect(target)

    def updateActions(self):
        """Fix the button classes."""
        super().updateActions()
        for action in self.actions.values():
            action.klass = "pat-button"


class ResetPasswordRequest(BaseForm):
    """Request a link to reset the password."""

    ignoreContext = True
    schema = ResetPasswordRequestSchema

    label = _(
        "title_reset_password_request",
        default="Password recovery",
    )
    description = _(
        "description_reset_password_request",
        ("We will send you an email " "with the instructions to reset your password."),
    )
    button_label = _(
        "label_send_password_reminder",
        default="Send password reminder",
    )

    email_template = ViewPageTemplateFile("templates/password_recovery_email.pt")

    @property
    def email_from_name(self):
        return api.portal.get_registry_record("plone.email_from_name")

    @property
    def email_from_address(self):
        return api.portal.get_registry_record("plone.email_from_address")

    def expiration_timeout(self):
        ppr = api.portal.get_tool("portal_password_reset")
        timeout = ppr.getExpirationTimeout() or 0
        return int(timeout * 24)  # timeout is in days, but templates want in hours.

    def log_error(self, msg):
        """Log an error message, set the view error attribute and return
        False."""
        logger.error(msg)
        self.error = _(
            "An error occured while sending the password reset instructions",
        )
        return False

    def get_remote_host(self):
        forwarded_for = self.request.get("HTTP_X_FORWARDED_FOR")
        if is_ipv4_address(forwarded_for):
            return forwarded_for
        return self.request.get("REMOTE_ADDR")

    def send_mail(self, email):
        account = Session.query(Account).filter(Account.loginname == email).first()
        if not account:
            # We returned True even if the account
            # does not exist to not leak any information
            return True

        ppr = api.portal.get_tool("portal_password_reset")
        # Clean out previous requests by this user
        for token, value in ppr._requests.items():
            if value[0] == account.id:
                del ppr._requests[token]
                ppr._p_changed = 1

        reset_info = ppr.requestReset(account.id)
        reset_info["host"] = self.get_remote_host()
        mailhost = api.portal.get_tool("MailHost")
        body = self.email_template(**reset_info)
        subject = translate(
            _("OiRA password reset instructions"),
            context=self.request,
        )
        mail = CreateEmailTo(
            self.email_from_name,
            self.email_from_address,
            account.email,
            subject,
            body,
        )

        try:
            mailhost.send(
                mail,
                account.email,
                self.email_from_address,
                immediate=True,
            )
            logger.info(
                "Sent password reset instructions to %s",
                account.email,
            )
        except MailHostError as e:
            msg = (
                "MailHost error sending password reset instructions to {}: {}"
            ).format(account.email, e)
            return self.log_error(msg)
        except smtplib.SMTPException as e:
            msg = (
                "smtplib error sending password reset instructions to {}: {}"
            ).format(account.email, e)
            return self.log_error(msg)
        except OSError as e:
            msg = ("Socket error sending password reset instructions to {}: {}").format(
                account.email, e[1]
            )
            return self.log_error(msg)
        return True

    def do_next(self):
        data, error = self.extractData()
        if error:
            return
        email = data.get("email")
        if not self.send_mail(email):
            return
        msg = _(
            "message_password_recovery_email_sent",
            default="An email will be sent to ${email} "
            "if we can find an account for this email address. Please use the "
            "link inside the e-mail to reset your password.",
            mapping={"email": email},
        )
        webhelpers = api.content.get_view(
            name="webhelpers", context=self.context, request=self.request
        )
        redir_url = webhelpers.get_came_from(default=self.context.absolute_url())
        if not redir_url.endswith("login"):
            redir_url = "{}/@@login?{}#login".format(
                redir_url, urlencode({"came_from": redir_url})
            )
        self.redirect(redir_url, msg)

    @button.buttonAndHandler(_("Save"))
    def next_handler(self, action):
        """Check if the security token is correct and if it is change the
        account password with the provided value."""
        self.do_next()

    @button.buttonAndHandler(_("Cancel"))
    def handleCancel(self, action):
        self.redirect(self.context.absolute_url())


@implementer(IPublishTraverse)
class ResetPasswordForm(BaseForm):
    ignoreContext = True
    schema = ResetPasswordFormSchema

    label = _(
        "title_reset_password_form",
        default="Reset password",
    )
    description = _(
        "description_reset_password_form",
        default="",
    )
    button_label = _("Save changes")

    def update(self):
        super().update()
        key = self.key
        ppr = api.portal.get_tool("portal_password_reset")
        try:
            ppr.verifyKey(key)
        except InvalidRequestError:
            self.error = _("Invalid security token, try to request a new one")

    def publishTraverse(self, request, name):
        return self

    @property
    @memoize_contextless
    def key(self):
        """Extract the key from the URL."""
        return self.request.getURL().rpartition("/")[-1]

    def do_save(self):
        """Execute the save action."""
        (data, errors) = self.extractData()
        if errors:
            for err in errors:
                if isinstance(err.error, Exception):
                    self.error = _(
                        "error_password_mismatch", default="Passwords do not match"
                    )
            return

        key = self.key
        ppr = api.portal.get_tool("portal_password_reset")

        try:
            ppr.verifyKey(key)
        except InvalidRequestError:
            self.error = _("Invalid security token, try to request a new one")
            return

        login_view = api.content.get_view(
            name="login",
            context=self.context,
            request=self.request,
        )
        error = login_view.check_password_policy(data["new_password"])
        if error:
            self.error = error
            return

        account_id, expiry = ppr._requests.get(key)
        if ppr.expired(expiry):
            del ppr._requests[key]
            ppr._p_changed = 1
            self.error = _("This URL has expired, try to request a new one")
            return

        account = Session().query(Account).filter(Account.id == account_id).one()
        account.password = data["new_password"]

        # clean out the request
        del ppr._requests[key]
        ppr._p_changed = 1

        current_url = self.context.absolute_url()
        return self.redirect(
            f"{current_url}/@@login?{urlencode(dict(came_from=current_url))}",
            msg=_("Your password was successfully changed."),
        )

    @button.buttonAndHandler(_("Save"))
    def save_handler(self, action):
        """Check if the security token is correct and if it is change the
        account password with the provided value."""
        self.do_save()

    @button.buttonAndHandler(_("Cancel"))
    def handleCancel(self, action):
        self.redirect(self.context.absolute_url())
