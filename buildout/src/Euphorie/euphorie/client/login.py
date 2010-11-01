import cgi
import logging
import socket
import smtplib
import urllib
import urlparse
from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import aq_chain
from AccessControl import getSecurityManager
from z3c.saconfig import Session
from five import grok
from zope.interface import Interface
from zope.i18n import translate
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.utils import CreateEmailTo
from euphorie.client.utils import setLanguage
from euphorie.client import model
from euphorie.client.session import SessionManager
from euphorie.client.country import IClientCountry

log=logging.getLogger(__name__)

grok.templatedir("templates")


class LoginView(grok.View):
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("login")
    grok.template("login")

    def setLanguage(self, came_from):
        qs=urlparse.urlparse(came_from)[4]
        if not qs:
            return

        params=cgi.parse_qs(qs)
        lang=params.get("language")
        if not lang:
            return

        setLanguage(self.request, self.context, lang=lang[0])


    def update(self):
        context=aq_inner(self.context)
        came_from=self.request.form.get("came_from")
        if came_from:
            if isinstance(came_from, list):
                # If came_from is both in the querystring and the form data
                came_from=came_from[0]
            self.setLanguage(came_from)
        else:
            came_from=aq_parent(context).absolute_url()

        if self.request.environ["REQUEST_METHOD"]=="POST":
            reply=self.request.form
            if reply["next"]=="previous":
                next=aq_parent(aq_inner(context)).absolute_url()
                self.request.response.redirect(next)
                return

            user=getSecurityManager().getUser()
            if isinstance(user, model.Account) and user.getId()==reply.get("__ac_name"):
                pas=getToolByName(self.context, "acl_users")
                pas.updateCredentials(self.request, self.request.response,
                        user.getId(), reply.get("__ac_password", ""))
                self.request.response.redirect(came_from)
                return
            self.error=True

        self.reminder_url="%s/@@reminder?%s" % (context.absolute_url(), 
                urllib.urlencode(dict(came_from=came_from)))
        self.register_url="%s/@@register?%s" % (context.absolute_url(), 
                urllib.urlencode(dict(came_from=came_from)))



class Reminder(grok.View):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("reminder")

    email_template = ViewPageTemplateFile("templates/reminder-email.pt")

    def _sendReminder(self):
        reply=self.request.form
        loginname=reply.get("loginname")
        if not loginname:
            self.error=_(u"Please enter your email address")
            return False

        account=Session.query(model.Account)\
                .filter(model.Account.loginname==loginname).first()
        if not account:
            self.error=_(u"Unknown email address")
            return False

        site=getUtility(ISiteRoot)
        mailhost=getToolByName(self.context, "MailHost")
        body=self.email_template(loginname=account.loginname, password=account.password)
        subject=translate(_(u"OiRA registration reminder"), context=self.request)
        mail=CreateEmailTo(site.email_from_name, site.email_from_address,
                account.email, subject, body)

        try:
            mailhost.send(mail, account.email, site.email_from_address, immediate=True)
        except MailHostError, e:
            log.error("MailHost error sending password reminder to %s: %s", account.email, e)
            self.error=_(u"An error occured while sending the password reminder")
            return False
        except smtplib.SMTPException, e:
            log.error("smtplib error sending password reminder to %s: %s", account.email, e)
            self.error=_(u"An error occured while sending the password reminder")
            return False
        except socket.error, e:
            log.error("Socket error sending password reminder to %s: %s", account.email, e[1])
            self.error=_(u"An error occured while sending the password reminder")
            return False

        return True


    def update(self):
        context=aq_inner(self.context)
        self.back_url=self.request.form.get("came_from")
        if not self.back_url:
            self.back_url=context.absolute_url()

        if self.request.environ["REQUEST_METHOD"]=="POST":
            if self._sendReminder():
                self.notice=_(u"An email with a password reminder has been sent to your address.")
                self.request.response.redirect(self.back_url)
                
                


class Register(grok.View):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("register")

    def _tryRegistration(self):
        reply=self.request.form
        loginname=reply.get("email")
        if not loginname:
            self.errors["email"]=_("error_missing_email", default=u"Please enter your email address")
        if not reply.get("password1"):
            self.errors["password"]=_("error_missing_password", default=u"Please enter a password")
        elif reply.get("password1")!=reply.get("password2"):
            self.errors["password"]=_("error_password_mismatch", default=u"Passwords do not match")
        if self.errors:
            return False

        session=Session()
        account=session.query(model.Account)\
                .filter(model.Account.loginname==loginname).count()
        if account:
            self.errors["email"]=_("error_email_in_use",
                    default=u"An account with this email address already exists.")
            return False

        pm=getToolByName(self.context, "portal_membership")
        if pm.getMemberById(loginname) is not None:
            self.errors["email"]=_("error_email_in_use",
                    default=u"An account with this email address already exists.")
            return False

        account=model.Account(loginname=reply.get("email"),
                              password=reply.get("password1"))
        Session().add(account)
        return account


    def update(self):
        self.errors={}
        if self.request.environ["REQUEST_METHOD"]=="POST":
            account=self._tryRegistration()
            if account:
                pas=getToolByName(self.context, "acl_users")
                pas.updateCredentials(self.request, self.request.response,
                        account.getId(), account.password)

                came_from=self.request.form.get("came_from")
                if not came_from:
                    came_from=aq_parent(aq_inner(self.context)).absolute_url()

                self.request.response.redirect(came_from)



class Logout(grok.CodeView):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)

    def render(self):
        SessionManager.stop()

        pas=getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)

        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                break
        else:
            obj=self.request.client

        self.request.response.redirect(obj.absolute_url())


