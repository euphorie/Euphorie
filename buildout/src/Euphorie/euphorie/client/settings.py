from Acquisition import aq_inner
from AccessControl import getSecurityManager
from five import grok
from zope import schema
from zope.interface import directlyProvides
from zope.interface import Invalid
from z3c.form import button
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.schema.email import RFC822MailAddress
from plone.directives import form
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.country import IClientCountry
from Products.statusmessages.interfaces import IStatusMessage


grok.templatedir("templates")


class PasswordChangeSchema(form.Schema):
    old_password = schema.Password(
            title = _(u"label_old_password", default=u"Current Password"),
            required=True)
    form.widget(old_password="z3c.form.browser.password.PasswordFieldWidget")

    new_password = schema.Password(
            title = _(u"label_new_password", default=u"Desired password"))



class EmailChangeSchema(form.Schema):
    loginname = RFC822MailAddress(
            title = _(u"Email address/account name"),
            required=True)



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
            flash(self.formErrorsMessage, "error")
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



class NewEmail(form.SchemaForm):
    grok.context(IClientCountry)

    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("new-email")
    grok.template("new-email")

    schema = EmailChangeSchema

    label = _(u"title_account_settings", default=u"Account settings")

    @button.buttonAndHandler(_(u"Save changes"))
    def handleSave(self, action):
        flash=IStatusMessage(self.request).addStatusMessage
        (data, errors)=self.extractData()
        if errors:
            flash(self.formErrorsMessage, "error")
            return

        user=getSecurityManager().getUser()
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
    
    def getContent(self):
        user=getSecurityManager().getUser()
        directlyProvides(user, EmailChangeSchema)
        return user

