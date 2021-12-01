"""
Settings
--------

Change a user's password/email or delete an account.
"""
from Acquisition import aq_inner
from euphorie.client import MessageFactory as _
from euphorie.client.model import Account
from euphorie.client.model import AccountChangeRequest
from euphorie.client.model import get_current_account
from euphorie.client.utils import CreateEmailTo
from euphorie.client.utils import randomString
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from six.moves.urllib.parse import urlencode
from z3c.form import button
from z3c.form import form
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.saconfig import Session
from z3c.schema.email import RFC822MailAddress
from zope import schema
from zope.i18n import translate
from zope.interface import directlyProvides
from zope.interface import Invalid
from zope.interface import invariant

import datetime
import logging
import smtplib
import socket


log = logging.getLogger(__name__)


class PasswordChangeSchema(model.Schema):
    old_password = schema.Password(
        title=_(u"label_old_password", default=u"Current Password"), required=True
    )
    directives.widget(old_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password = schema.Password(
        title=_(u"label_new_password", default=u"Desired password")
    )
    directives.widget(new_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password_confirmation = schema.Password(
        title=_(u"label_new_password_confirmation", default=u"Again password")
    )
    directives.widget(
        new_password_confirmation="z3c.form.browser.password.PasswordFieldWidget"
    )

    @invariant
    def validate_same_value(data):
        if data.new_password != data.new_password_confirmation:
            raise Invalid(_("Password doesn't compare with confirmation value"))


class AccountDeleteSchema(model.Schema):
    password = schema.Password(
        title=_(u"Your password for confirmation"), required=True
    )
    directives.widget(password="z3c.form.browser.password.PasswordFieldWidget")


class EmailChangeSchema(model.Schema):
    loginname = RFC822MailAddress(title=_(u"Email address/account name"), required=True)
    directives.widget("loginname", type="email")

    password = schema.Password(
        title=_(u"Your password for confirmation"), required=True
    )
    directives.widget(password="z3c.form.browser.password.PasswordFieldWidget")


class AccountSettings(AutoExtensibleForm, form.Form):
    """View name: @@account-settings"""

    template = ViewPageTemplateFile("templates/account-settings.pt")

    schema = PasswordChangeSchema
    ignoreContext = True

    label = _(u"title_change_password", default=u"Change password")

    def updateWidgets(self):
        super(AccountSettings, self).updateWidgets()
        self.widgets["old_password"].addClass("password")
        self.widgets["new_password"].addClass("password")

    @button.buttonAndHandler(_(u"Save changes"), name="save")
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage
        (data, errors) = self.extractData()
        if errors:
            for error in errors:
                flash(error.message, "notice")
            return

        user = get_current_account()
        if not data["new_password"]:
            flash(_(u"There were no changes to be saved."), "notice")
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
                "old_password", Invalid(_(u"Invalid password"))
            )
        user.password = data["new_password"]
        flash(_(u"Your password was successfully changed."), "success")

    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.request.client.absolute_url())


class DeleteAccount(AutoExtensibleForm, form.Form):
    """"View name: @@account-delete"""

    template = ViewPageTemplateFile("templates/account-delete.pt")

    schema = AccountDeleteSchema
    ignoreContext = True

    label = _(u"title_account_delete", default=u"Delete account")

    def updateWidgets(self):
        super(DeleteAccount, self).updateWidgets()
        self.widgets["password"].addClass("password")

    def logout(self):
        pas = getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)

    @button.buttonAndHandler(_(u"Delete account"), name="delete")
    def handleDelete(self, action):
        (data, errors) = self.extractData()
        if errors:
            return

        user = get_current_account()
        if not user.verify_password(data["password"]):
            raise WidgetActionExecutionError(
                "password", Invalid(_(u"Invalid password"))
            )

        Session.delete(user)
        self.logout()
        self.request.response.redirect(self.request.client.absolute_url())

    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.request.client.absolute_url())


class NewEmail(AutoExtensibleForm, form.Form):

    template = ViewPageTemplateFile("templates/new-email.pt")

    schema = EmailChangeSchema
    email_template = ViewPageTemplateFile("templates/confirm-email.pt")
    ignoreContext = True

    label = _(u"title_account_settings", default=u"Account settings")

    @property
    def email_from_name(self):
        return api.portal.get_registry_record("plone.email_from_name")

    @property
    def email_from_address(self):
        return api.portal.get_registry_record("plone.email_from_address")

    def updateFields(self):
        super(NewEmail, self).updateFields()
        self.fields["password"].ignoreContext = True

    def updateWidgets(self):
        super(NewEmail, self).updateWidgets()
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
            flash(_(u"An error occured while sending the confirmation email."), "error")
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
        confirm_url = "%s/confirm-change?%s" % (
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
            _(u"Confirm OiRA email address change"), context=self.request
        )
        mail = CreateEmailTo(
            self.email_from_name, self.email_from_address, login, subject, body
        )

        try:
            mailhost.send(mail, login, self.email_from_address, immediate=True)
            log.info("Sent email confirmation to %s", account.email)
        except MailHostError as e:
            log.error(
                "MailHost error sending email confirmation to %s: %s", account.email, e
            )
            flash(_(u"An error occured while sending the confirmation email."), "error")
            return False
        except smtplib.SMTPException as e:
            log.error(
                "smtplib error sending the confirmation email to %s: %s",
                account.email,
                e,
            )
            flash(_(u"An error occured while sending the confirmation email."), "error")
            return False
        except socket.error as e:
            log.error(
                "Socket error sending confirmation email to %s: %s", account.email, e[1]
            )
            flash(_(u"An error occured while sending the confirmation email."), "error")
            return False

        return True

    @button.buttonAndHandler(_(u"Save changes"), name="save")
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage

        (data, errors) = self.extractData()
        if errors:
            return
        url = self.context.absolute_url()

        user = get_current_account()
        if not user.verify_password(data["password"]):
            raise WidgetActionExecutionError(
                "password", Invalid(_(u"Invalid password"))
            )

        settings_url = "%s/account-settings" % url
        if not data["loginname"] or data["loginname"].strip() == user.loginname:
            self.request.response.redirect(settings_url)
            flash(_(u"There were no changes to be saved."), "notice")
            return

        login = data["loginname"].strip().lower()
        existing = Session.query(Account.id).filter(Account.loginname == login)
        if existing.count():
            raise WidgetActionExecutionError(
                "loginname", Invalid(_(u"This email address is not available."))
            )

        self.initiateRequest(user, login)

        flash(
            _(
                "email_change_pending",
                default=(
                    u"Please confirm your new email address by clicking on "
                    u"the link in the email that will be sent in a few "
                    u'minutes to "${email}". Please note that the new '
                    u"email address is also your new login name."
                ),
                mapping={"email": data["loginname"]},
            ),
            "warning",
        )
        self.request.response.redirect("%s/" % url)

    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"), name="cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.request.client.absolute_url())


class ChangeEmail(BrowserView):
    def __call__(self):
        url = "%s/" % aq_inner(self.context).absolute_url()
        flash = IStatusMessage(self.request).addStatusMessage
        key = self.request.get("key")
        if key is None:
            flash(_(u"This request could not be processed."), "warning")
            self.request.response.redirect(url)
            return

        request = Session.query(AccountChangeRequest).get(key)
        if request is None:
            flash(_(u"This request could not be processed."), "warning")
            self.request.response.redirect(url)
            return

        request.account.loginname = request.value
        Session.delete(request)
        flash(_("Your email address has been updated."), "success")
        self.request.response.redirect(url)
