from Acquisition import aq_inner
from AccessControl import getSecurityManager
from five import grok
from zope import schema
from zope.interface import directlyProvides
from zope.interface import Invalid
from z3c.form import button
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.schema.email import RFC822MailAddress
from z3c.saconfig import Session
from plone.directives import form
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.country import IClientCountry
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from euphorie.client.session import SessionManager


grok.templatedir("templates")


class PasswordChangeSchema(form.Schema):
    old_password = schema.Password(
            title = _(u"label_old_password", default=u"Current Password"),
            required=True)
    form.widget(old_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password = schema.Password(
            title = _(u"label_new_password", default=u"Desired password"))



class AccountDeleteSchema(form.Schema):
    password = schema.Password(
            title = _(u"Your password for confirmation"),
            required=True)
    form.widget(password="z3c.form.browser.password.PasswordFieldWidget")



class EmailChangeSchema(form.Schema):
    loginname = RFC822MailAddress(
            title = _(u"Email address/account name"),
            required=True)

    password = schema.Password(
            title = _(u"Your password for confirmation"),
            required=True)
    form.widget(password="z3c.form.browser.password.PasswordFieldWidget")



class AccountSettings(form.SchemaForm):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("account-settings")
    grok.template("account-settings")

    schema = PasswordChangeSchema
    ignoreContext = True

    label = _(u"title_account_settings", default=u"Account settings")


    @button.buttonAndHandler(_(u"Save changes"))
    def handleSave(self, action):
        flash=IStatusMessage(self.request).addStatusMessage
        (data, errors)=self.extractData()
        if errors:
            return

        user=getSecurityManager().getUser()
        if not data["new_password"]:
            flash(_(u"There were no changes to be saved."), "notice")
            return
        if data["old_password"]!=user.password:
            raise WidgetActionExecutionError("old_password",
                    Invalid(_(u"Invalid password")))
        user.password=data["new_password"]
        flash(_(u"Your password was successfully changed."), "success")



class DeleteAccount(form.SchemaForm):
    grok.context(IClientCountry)

    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("account-delete")
    grok.template("account-delete")

    schema = AccountDeleteSchema
    ignoreContext = True

    label = _(u"title_account_delete", default=u"Delete account")

    def logout(self):
        pas=getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)
        SessionManager.stop()


    @button.buttonAndHandler(_(u"Delete account"))
    def handleDelete(self, action):
        (data, errors)=self.extractData()
        if errors:
            return

        user=getSecurityManager().getUser()

        if user.password!=data["password"]:
            raise WidgetActionExecutionError("password",
                    Invalid(_(u"Invalid password")))

        user=getSecurityManager().getUser()
        Session.delete(user)
        self.logout()
        self.request.response.redirect(self.request.client.absolute_url())


    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"))
    def handleCancel(self, action):
        settings_url="%s/account-settings" % aq_inner(self.context).absolute_url()
        self.request.response.redirect(settings_url)



class NewEmail(form.SchemaForm):
    grok.context(IClientCountry)

    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("new-email")
    grok.template("new-email")

    schema = EmailChangeSchema

    label = _(u"title_account_settings", default=u"Account settings")

    def updateFields(self):
        super(NewEmail, self).updateFields()
        self.fields["password"].ignoreContext=True


    def getContent(self):
        user=getSecurityManager().getUser()
        directlyProvides(user, EmailChangeSchema)
        return user


    @button.buttonAndHandler(_(u"Save changes"))
    def handleSave(self, action):
        flash=IStatusMessage(self.request).addStatusMessage
        (data, errors)=self.extractData()
        if errors:
            return

        user=getSecurityManager().getUser()

        if user.password!=data["password"]:
            raise WidgetActionExecutionError("password",
                    Invalid(_(u"Invalid password")))

        settings_url="%s/account-settings" % aq_inner(self.context).absolute_url()
        if not data["loginname"] or data["loginname"].strip()==user.loginname:
            self.request.response.redirect(settings_url)
            flash(_(u"There were no changes to be saved."), "notice")
            return

        flash(_("email_change_pending", default=
            u"Please confirm your new email address by clicking on the link "
            u"in the email that will be sent in a few minutes to "
            u"\"${email}\". Please note that the new email address is also "
            u"your new login name.",
            mapping={"email": data["loginname"]}), "warning")
        self.request.response.redirect(settings_url)
    

    @button.buttonAndHandler(_("button_cancel", default=u"Cancel"))
    def handleCancel(self, action):
        settings_url="%s/account-settings" % aq_inner(self.context).absolute_url()
        self.request.response.redirect(settings_url)

