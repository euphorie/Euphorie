"""
Settings
--------

Change a user's password/email or delete an account.
"""

from Acquisition import aq_inner
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.model import Account
from euphorie.client.model import AccountChangeRequest
from euphorie.client.model import get_current_account
from euphorie.client.model import NotificationSubscription
from euphorie.client.utils import CreateEmailTo
from euphorie.client.utils import randomString
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.instance import memoize
from plone.protect.interfaces import IDisableCSRFProtection
from plone.schema import Email
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from urllib.parse import urlencode
from z3c.form import button
from z3c.form import form
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.saconfig import Session
from zope import schema
from zope.component import getAdapters
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import directlyProvides
from zope.interface import Invalid
from zope.interface import invariant

import datetime
import logging
import smtplib


log = logging.getLogger(__name__)


class UserMenu(BrowserView):
    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def menu_contents(self):
        return [
            {
                "class_outer": "menu-item-preferences",
                "class_inner": "icon-cog",
                "url": f"{self.webhelpers.country_url}/preferences",
                "label": _("title_preferences", default="Preferences"),
            },
            {
                "class_outer": "menu-item-change-password",
                "class_inner": "icon-key",
                "url": f"{self.webhelpers.country_url}/account-settings",
                "label": _("title_change_password", default="Change password"),
            },
            {
                "class_outer": "menu-item-change-email-address",
                "class_inner": "icon-mail",
                "url": f"{self.webhelpers.country_url}/new-email",
                "label": _("Change email address"),
            },
            {
                "class_outer": "menu-item-delete-account",
                "class_inner": "icon-cancel-circle",
                "url": f"{self.webhelpers.country_url}/account-delete",
                "label": _("Delete account"),
            },
            {
                "class_outer": "menu-item-logout",
                "class_inner": "icon-exit",
                "url": f"{self.webhelpers.country_url}/logout",
                "label": _("navigation_logout", default="Logout"),
            },
        ]


class PasswordChangeSchema(model.Schema):
    old_password = schema.Password(
        title=_("label_old_password", default="Current Password"),
        required=True,
    )
    directives.widget(old_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password = schema.Password(
        title=_("label_new_password", default="Desired password")
    )
    directives.widget(new_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password_confirmation = schema.Password(
        title=_("label_new_password_confirmation", default="Again password")
    )
    directives.widget(
        new_password_confirmation="z3c.form.browser.password.PasswordFieldWidget"
    )

    @invariant
    def validate_same_value(data):
        if data.new_password != data.new_password_confirmation:
            raise Invalid(_("Password doesn't compare with confirmation value"))


class AccountDeleteSchema(model.Schema):
    password = schema.Password(title=_("Your password for confirmation"), required=True)
    directives.widget(password="z3c.form.browser.password.PasswordFieldWidget")


class EmailChangeSchema(model.Schema):
    loginname = Email(title=_("Email address/account name"), required=True)
    directives.widget("loginname", type="email")

    password = schema.Password(title=_("Your password for confirmation"), required=True)
    directives.widget(password="z3c.form.browser.password.PasswordFieldWidget")


class PreferencesSchema(model.Schema):
    first_name = schema.TextLine(
        title=_("label_first_name", default="First name"), required=False
    )
    last_name = schema.TextLine(
        title=_("label_last_name", default="Last name"), required=False
    )


class Preferences(AutoExtensibleForm, form.Form):
    template = ViewPageTemplateFile("templates/preferences.pt")
    no_splash = True
    schema = PreferencesSchema

    @property
    def show_personal_details(self):
        return api.portal.get_registry_record(
            "euphorie.personal_details__enabled", default=True
        )

    @property
    def show_notifications(self):
        return api.portal.get_registry_record(
            "euphorie.notifications__enabled", default=False
        )

    @property
    def allow_notification_settings(self):
        return api.portal.get_registry_record(
            "euphorie.notifications__allow_user_settings", default=True
        )

    @property
    @memoize
    def current_user(self):
        return get_current_account()

    def getContent(self):
        user = self.current_user
        directlyProvides(user, PreferencesSchema)
        return user

    @property
    def all_notifications(self):
        notifications = getAdapters((self.context, self.request), INotificationCategory)
        # Return the available notifications, sorted by title.
        notifications = [
            notification[1]
            for notification in notifications
            if notification[1].available
        ]
        return sorted(
            notifications,
            key=lambda notification: translate(notification.title),
        )

    @property
    @memoize
    def existing_notification_subscriptions(self):
        subscriptions = Session.query(NotificationSubscription).filter(
            NotificationSubscription.account_id == self.current_user.getId()
        )
        return {subscription.category: subscription for subscription in subscriptions}

    def subscribe_notification(self, category_id):
        notification = self.existing_notification_subscriptions.get(category_id)
        if notification:
            notification.enabled = True
            return
        Session.add(
            NotificationSubscription(
                account_id=self.current_user.getId(),
                category=category_id,
                enabled=True,
            )
        )

    def unsubscribe_notification(self, category_id):
        notification = self.existing_notification_subscriptions.get(category_id)
        if notification:
            notification.enabled = False
            return
        Session.add(
            NotificationSubscription(
                account_id=self.current_user.getId(),
                category=category_id,
                enabled=False,
            )
        )

    @button.buttonAndHandler(_("Save"), name="save")
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage
        (data, errors) = self.extractData()
        if errors:
            for error in errors:
                flash(error.message, "notice")
            return
        user = self.current_user
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]

        if self.show_notifications and self.allow_notification_settings:
            for notification in self.all_notifications:
                if self.request.get("notifications", {}).get(notification.id):
                    self.subscribe_notification(notification.id)
                else:
                    self.unsubscribe_notification(notification.id)


class AccountSettings(AutoExtensibleForm, form.Form):
    """View name: @@account-settings."""

    template = ViewPageTemplateFile("templates/account-settings.pt")

    schema = PasswordChangeSchema
    ignoreContext = True

    label = _("title_change_password", default="Change password")

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["old_password"].addClass("password")
        self.widgets["new_password"].addClass("password")

    @button.buttonAndHandler(_("Save changes"), name="save")
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage
        (data, errors) = self.extractData()
        if errors:
            for error in errors:
                flash(error.message, "notice")
            return

        user = get_current_account()
        if not data["new_password"]:
            flash(_("There were no changes to be saved."), "notice")
            return
        login_view = api.content.get_view(
            name="login",
            context=self.context,
            request=self.request,
        )
        error = login_view.check_password_policy(data["new_password"])
        if error:
            raise WidgetActionExecutionError("new_password", Invalid(error))
        if not user.verify_password(data["old_password"]):
            raise WidgetActionExecutionError(
                "old_password", Invalid(_("Invalid password"))
            )
        user.password = data["new_password"]
        flash(_("Your password was successfully changed."), "success")

    @button.buttonAndHandler(_("button_cancel", default="Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.request.client.absolute_url())


class DeleteAccount(AutoExtensibleForm, form.Form):
    """View name: @@account-delete."""

    template = ViewPageTemplateFile("templates/account-delete.pt")

    schema = AccountDeleteSchema
    ignoreContext = True

    label = _("title_account_delete", default="Delete account")

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["password"].addClass("password")

    def logout(self):
        pas = getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)

    @button.buttonAndHandler(_("Delete account"), name="delete")
    def handleDelete(self, action):
        (data, errors) = self.extractData()
        if errors:
            return

        user = get_current_account()
        if not user.verify_password(data["password"]):
            raise WidgetActionExecutionError("password", Invalid(_("Invalid password")))

        Session.delete(user)
        self.logout()
        self.request.response.redirect(self.request.client.absolute_url())

    @button.buttonAndHandler(_("button_cancel", default="Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.request.client.absolute_url())


class NewEmail(AutoExtensibleForm, form.Form):
    template = ViewPageTemplateFile("templates/new-email.pt")

    schema = EmailChangeSchema
    email_template = ViewPageTemplateFile("templates/confirm-email.pt")
    ignoreContext = True

    label = _("title_change_email", default="Change email address")

    @property
    def email_from_name(self):
        return api.portal.get_registry_record("plone.email_from_name")

    @property
    def email_from_address(self):
        return api.portal.get_registry_record("plone.email_from_address")

    def updateFields(self):
        super().updateFields()
        self.fields["password"].ignoreContext = True

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["password"].addClass("password")

    def getContent(self):
        user = get_current_account()
        directlyProvides(user, EmailChangeSchema)
        return user

    def initiateRequest(self, account, login):
        flash = IStatusMessage(self.request).addStatusMessage
        # Make it work when acl_users is in Memcached: We need to fetch the
        # account again, to prevent DetachedInstanceError
        account_query = Session.query(Account).filter(Account.id == account.id)
        if not account_query.count():
            log.error("Account could not be fetched")
            flash(
                _("An error occured while sending the confirmation email."),
                "error",
            )
            return False
        account = account_query.one()
        if account.change_request is None:
            account.change_request = AccountChangeRequest()
        account.change_request.id = randomString()
        account.change_request.expires = datetime.datetime.now() + datetime.timedelta(
            days=7
        )
        account.change_request.value = login

        client_url = self.request.client.absolute_url()
        confirm_url = "{}/confirm-change?{}".format(
            client_url,
            urlencode({"key": account.change_request.id}),
        )

        mailhost = getToolByName(self.context, "MailHost")
        body = self.email_template(
            account=account,
            new_login=login,
            client_url=client_url,
            confirm_url=confirm_url,
        )
        subject = translate(
            _("Confirm OiRA email address change"), context=self.request
        )
        mail = CreateEmailTo(
            self.email_from_name, self.email_from_address, login, subject, body
        )

        try:
            mailhost.send(mail, login, self.email_from_address, immediate=True)
            log.info("Sent email confirmation to %s", account.email)
        except MailHostError as e:
            log.error(
                "MailHost error sending email confirmation to %s: %s",
                account.email,
                e,
            )
            flash(
                _("An error occured while sending the confirmation email."),
                "error",
            )
            return False
        except smtplib.SMTPException as e:
            log.error(
                "smtplib error sending the confirmation email to %s: %s",
                account.email,
                e,
            )
            flash(
                _("An error occured while sending the confirmation email."),
                "error",
            )
            return False
        except OSError as e:
            log.error(
                "Socket error sending confirmation email to %s: %s",
                account.email,
                e[1],
            )
            flash(
                _("An error occured while sending the confirmation email."),
                "error",
            )
            return False

        return True

    @button.buttonAndHandler(_("Save changes"), name="save")
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage

        (data, errors) = self.extractData()
        if errors:
            return
        url = self.context.absolute_url()

        user = get_current_account()
        if not user.verify_password(data["password"]):
            raise WidgetActionExecutionError("password", Invalid(_("Invalid password")))

        settings_url = "%s/account-settings" % url
        if not data["loginname"] or data["loginname"].strip() == user.loginname:
            self.request.response.redirect(settings_url)
            flash(_("There were no changes to be saved."), "notice")
            return

        login = data["loginname"].strip().lower()
        existing = Session.query(Account.id).filter(Account.loginname == login)
        if existing.count():
            raise WidgetActionExecutionError(
                "loginname", Invalid(_("This email address is not available."))
            )

        self.initiateRequest(user, login)

        flash(
            _(
                "email_change_pending",
                default=(
                    "Please confirm your new email address by clicking on "
                    "the link in the email that will be sent in a few "
                    'minutes to "${email}". Please note that the new '
                    "email address is also your new login name."
                ),
                mapping={"email": data["loginname"]},
            ),
            "warning",
        )
        self.request.response.redirect("%s/" % url)

    @button.buttonAndHandler(_("button_cancel", default="Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.request.client.absolute_url())


class ChangeEmail(BrowserView):
    def __call__(self):
        url = "%s/" % aq_inner(self.context).absolute_url()
        flash = IStatusMessage(self.request).addStatusMessage
        key = self.request.get("key")
        if key is None:
            flash(_("This request could not be processed."), "warning")
            self.request.response.redirect(url)
            return

        request = Session.query(AccountChangeRequest).get(key)
        if request is None:
            flash(_("This request could not be processed."), "warning")
            self.request.response.redirect(url)
            return

        request.account.loginname = request.value
        alsoProvides(self.request, IDisableCSRFProtection)
        Session.delete(request)
        flash(_("Your email address has been updated."), "success")
        self.request.response.redirect(url)
