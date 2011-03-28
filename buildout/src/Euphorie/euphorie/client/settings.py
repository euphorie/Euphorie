from five import grok
from zope import schema
from AccessControl import getSecurityManager
from zope.interface import Invalid
from z3c.form import button
from z3c.form.interfaces import WidgetActionExecutionError
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
            title = _(u"label_new_password", default=u"New password"))



class AccountSettings(form.SchemaForm):
    grok.context(IClientCountry)
    grok.require("euphorie.client.ViewSurvey")
    grok.layer(IClientSkinLayer)
    grok.name("account-settings")
    grok.template("account-settings")

    schema = PasswordChangeSchema

    label = _(u"title_account_settings", default=u"Account settings")

    ignoreContext = True

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

