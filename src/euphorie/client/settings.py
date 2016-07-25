"""
Settings
--------

Change a user's password/email or delete an account.
"""
import datetime
import logging
import smtplib
import socket
import urllib
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from five import grok
from zope import schema
from zope.interface import directlyProvides
from zope.interface import Invalid
from zope.component import getUtility
from zope.i18n import translate
from z3c.form import button
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.schema.email import RFC822MailAddress
from z3c.saconfig import Session
from plone.directives import form
from .. import MessageFactory as _
from euphorie.client.client import IClient
from euphorie.client.country import IClientCountry
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import Account
from euphorie.client.model import AccountChangeRequest
from euphorie.client.session import SessionManager
from euphorie.client.utils import CreateEmailTo
from euphorie.client.utils import randomString
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from Products.MailHost.MailHost import MailHostError

log = logging.getLogger(__name__)

grok.templatedir("templates")


class PasswordChangeSchema(form.Schema):
    old_password = schema.Password(
            title=_(u"label_old_password", default=u"Current Password"),
            required=True)
    form.widget(old_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password = schema.Password(
            title=_(u"label_new_password", default=u"Desired password"))


class AccountDeleteSchema(form.Schema):
    password = schema.Password(
            title=_(u"Your password for confirmation"),
            required=True)
    form.widget(password="z3c.form.browser.password.PasswordFieldWidget")


class EmailChangeSchema(form.Schema):
    loginname = RFC822MailAddress(
            title=_(u"Email address/account name"),
            required=True)

    password = schema.Password(
            title=_(u"Your password for confirmation"),
            required=True)
    form.widget(password="z3c.form.browser.password.PasswordFieldWidget")


class AccountSettings(form.SchemaForm):
    """View name: @@account-settings"""
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("account-settings")
    grok.template("account-settings")

    schema = PasswordChangeSchema
    ignoreContext = True

    label = _(u"title_change_password", default=u"Change password")

    def updateWidgets(self):
        super(AccountSettings, self).updateWidgets()
        self.widgets["old_password"].addClass("password")
        self.widgets["new_password"].addClass("password")

    @button.buttonAndHandler(_(u"Save changes"), name='save')
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage
        (data, errors) = self.extractData()
        if errors:
            return

        user = getSecurityManager().getUser()
        if not data["new_password"]:
            flash(_(u"There were no changes to be saved."), "notice")
            return
        if data["old_password"] != user.password:
            raise WidgetActionExecutionError("old_password",
                    Invalid(_(u"Invalid password")))
        user.password = data["new_password"]
        flash(_(u"Your password was successfully changed."), "success")


class DeleteAccount(form.SchemaForm):
    """"View name: @@account-delete"""
    grok.context(IClientCountry)

    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("account-delete")
    grok.template("account-delete")

    schema = AccountDeleteSchema
    ignoreContext = True

    label = _(u"title_account_delete", default=u"Delete account")

    def updateWidgets(self):
        super(DeleteAccount, self).updateWidgets()
        self.widgets["password"].addClass("password")

    def logout(self):
        pas = getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)
        SessionManager.stop()

    @button.buttonAndHandler(_(u"Delete account"), name='delete')
    def handleDelete(self, action):
        (data, errors) = self.extractData()
        if errors:
            return

        user = getSecurityManager().getUser()
        if user.password != data["password"]:
            raise WidgetActionExecutionError("password",
                    Invalid(_(u"Invalid password")))

        user = getSecurityManager().getUser()
        Session.delete(user)
        self.logout()
        self.request.response.redirect(self.request.client.absolute_url())

    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"), name='cancel')
    def handleCancel(self, action):
        settings_url = "%s/account-settings" % \
                aq_inner(self.context).absolute_url()
        self.request.response.redirect(settings_url)


class NewEmail(form.SchemaForm):
    grok.context(IClientCountry)

    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("new-email")
    grok.template("new-email")

    schema = EmailChangeSchema
    email_template = ViewPageTemplateFile("templates/confirm-email.pt")
    ignoreContext = True

    label = _(u"title_account_settings", default=u"Account settings")

    def updateFields(self):
        super(NewEmail, self).updateFields()
        self.fields["password"].ignoreContext = True

    def updateWidgets(self):
        super(NewEmail, self).updateWidgets()
        self.widgets["password"].addClass("password")

    def getContent(self):
        user = getSecurityManager().getUser()
        directlyProvides(user, EmailChangeSchema)
        return user

    def initiateRequest(self, account, login):
        if account.change_request is None:
            account.change_request = AccountChangeRequest()
        account.change_request.id = randomString()
        account.change_request.expires = datetime.datetime.now() + \
                datetime.timedelta(days=7)
        account.change_request.value = login

        client_url = self.request.client.absolute_url()
        confirm_url = "%s/confirm-change?%s" % (client_url,
                urllib.urlencode({"key": account.change_request.id}))

        site = getUtility(ISiteRoot)
        mailhost = getToolByName(self.context, "MailHost")
        body = self.email_template(account=account, new_login=login,
                client_url=client_url, confirm_url=confirm_url)
        subject = translate(_(u"Confirm OiRA email address change"),
                context=self.request)
        mail = CreateEmailTo(site.email_from_name, site.email_from_address,
                login, subject, body)

        flash = IStatusMessage(self.request).addStatusMessage
        try:
            mailhost.send(mail, login, site.email_from_address, immediate=True)
            log.info("Sent email confirmation to %s", account.email)
        except MailHostError as e:
            log.error("MailHost error sending email confirmation to %s: %s",
                    account.email, e)
            flash(_(u"An error occured while sending the confirmation email."),
                    "error")
            return False
        except smtplib.SMTPException as e:
            log.error("smtplib error sending password reminder to %s: %s",
                    account.email, e)
            flash(_(u"An error occured while sending the confirmation email."),
                    "error")
            return False
        except socket.error as e:
            log.error("Socket error sending password reminder to %s: %s",
                    account.email, e[1])
            flash(_(u"An error occured while sending the confirmation email."),
                    "error")
            return False

        return True

    @button.buttonAndHandler(_(u"Save changes"), name='save')
    def handleSave(self, action):
        flash = IStatusMessage(self.request).addStatusMessage

        (data, errors) = self.extractData()
        if errors:
            return

        user = getSecurityManager().getUser()
        if user.password != data["password"]:
            raise WidgetActionExecutionError("password",
                    Invalid(_(u"Invalid password")))

        settings_url = "%s/account-settings" % \
                aq_inner(self.context).absolute_url()
        if not data["loginname"] or \
                data["loginname"].strip() == user.loginname:
            self.request.response.redirect(settings_url)
            flash(_(u"There were no changes to be saved."), "notice")
            return

        login = data["loginname"].strip().lower()
        existing = Session.query(Account.id).filter(Account.loginname == login)
        if existing.count():
            raise WidgetActionExecutionError("loginname",
                    Invalid(_(u"This email address is not available.")))

        self.initiateRequest(user, login)

        flash(_("email_change_pending",
            default=u"Please confirm your new email address by clicking on "
                    u"the link in the email that will be sent in a few "
                    u"minutes to \"${email}\". Please note that the new "
                    u"email address is also your new login name.",
            mapping={"email": data["loginname"]}), "warning")
        self.request.response.redirect(settings_url)

    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"), name='cancel')
    def handleCancel(self, action):
        settings_url = "%s/account-settings" % \
                aq_inner(self.context).absolute_url()
        self.request.response.redirect(settings_url)


class ChangeEmail(grok.View):
    grok.context(IClient)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.name("confirm-change")
    grok.template("error")

    def update(self):
        key = self.request.get("key")
        if key is None:
            return

        request = Session.query(AccountChangeRequest).get(key)
        if request is None:
            return

        request.account.loginname = request.value
        Session.delete(request)
        flash = IStatusMessage(self.request).addStatusMessage
        flash(_("Your email address has been updated."), "success")
        self.request.response.redirect(aq_inner(self.context).absolute_url())
