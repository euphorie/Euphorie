import cgi
import logging
import re
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
from plone.session.plugins.session import cookie_expiration_date
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from .interfaces import IClientSkinLayer
from .utils import CreateEmailTo
from .utils import setLanguage
from .model import Account
from .session import SessionManager
from .country import IClientCountry
from .conditions import checkTermsAndConditions
from .conditions import approvedTermsAndConditions
from .. import MessageFactory as _

log = logging.getLogger(__name__)

# I know this is a stupid regular expression, but it Works For Us(tm)
EMAIL_RE = re.compile(
    r'[_a-z0-9+-]+(\.[_a-z0-9+-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})',
    re.IGNORECASE)

grok.templatedir("templates")


class Login(grok.View):
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("login")
    grok.template("login")

    def setLanguage(self, came_from):
        qs = urlparse.urlparse(came_from)[4]
        if not qs:
            return
        params = cgi.parse_qs(qs)
        lang = params.get("language")
        if not lang:
            return
        setLanguage(self.request, self.context, lang=lang[0])

    def login(self, account, remember):
        pas = getToolByName(self.context, "acl_users")
        pas.updateCredentials(self.request, self.response,
                account.loginname, account.password)
        if remember:
            self.response.cookies['__ac']['expires'] = cookie_expiration_date(120)
            self.response.cookies['__ac']['max_age'] = 120 * 24 * 60 * 60

    def update(self):
        context = aq_inner(self.context)
        came_from = self.request.form.get("came_from")
        if came_from:
            if isinstance(came_from, list):
                # If came_from is both in the querystring and the form data
                came_from = came_from[0]
            self.setLanguage(came_from)
        else:
            came_from = aq_parent(context).absolute_url()

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply["next"] == "previous":
                next = aq_parent(aq_inner(context)).absolute_url()
                self.response.redirect(next)
                return

            account = getSecurityManager().getUser()
            if isinstance(account, Account) and \
                    account.getUserName() == reply.get("__ac_name", '').lower():
                self.login(account, bool(self.request.form.get('remember')))

                if checkTermsAndConditions() and \
                        not approvedTermsAndConditions(account):
                    self.response.redirect(
                        "%s/terms-and-conditions?%s" %
                        (context.absolute_url(),
                            urllib.urlencode({"came_from": came_from})))
                else:
                    self.response.redirect(came_from)
                return
            self.error = True

        self.reminder_url = "%s/@@reminder?%s" % (context.absolute_url(),
                urllib.urlencode({'came_from': came_from}))
        self.register_url = "%s/@@register?%s" % (context.absolute_url(),
                urllib.urlencode({'came_from': came_from}))


class Reminder(grok.View):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("reminder")

    email_template = ViewPageTemplateFile("templates/reminder-email.pt")

    def _sendReminder(self):
        reply = self.request.form
        loginname = reply.get("loginname")
        if not loginname:
            self.error = _(u"Please enter your email address")
            return False

        account = Session.query(Account)\
                .filter(Account.loginname == loginname).first()
        if not account:
            self.error = _(u"Unknown email address")
            return False

        site = getUtility(ISiteRoot)
        mailhost = getToolByName(self.context, "MailHost")
        body = self.email_template(
                loginname=account.loginname,
                password=account.password)
        subject = translate(_(u"OiRA registration reminder"),
                context=self.request)
        mail = CreateEmailTo(site.email_from_name, site.email_from_address,
                account.email, subject, body)

        try:
            mailhost.send(mail, account.email, site.email_from_address,
                    immediate=True)
            log.info("Sent password reminder to %s", account.email)
        except MailHostError, e:
            log.error("MailHost error sending password reminder to %s: %s",
                    account.email, e)
            self.error = _(
                    u"An error occured while sending the password reminder")
            return False
        except smtplib.SMTPException, e:
            log.error("smtplib error sending password reminder to %s: %s",
                    account.email, e)
            self.error = _(
                    u"An error occured while sending the password reminder")
            return False
        except socket.error, e:
            log.error("Socket error sending password reminder to %s: %s",
                    account.email, e[1])
            self.error = _(
                    u"An error occured while sending the password reminder")
            return False
        return True

    def update(self):
        context = aq_inner(self.context)
        self.back_url = self.request.form.get("came_from")
        if not self.back_url:
            self.back_url = context.absolute_url()

        if self.request.environ["REQUEST_METHOD"] == "POST":
            if self._sendReminder():
                flash = IStatusMessage(self.request).addStatusMessage
                flash(_(u"An email with a password reminder has been "
                        u"sent to your address."), "notice")
                self.request.response.redirect(self.back_url)


class Register(grok.View):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("register")

    def _tryRegistration(self):
        reply = self.request.form
        loginname = reply.get("email")
        if not loginname:
            self.errors["email"] = _("error_missing_email",
                    default=u"Please enter your email address")
        elif not EMAIL_RE.match(loginname):
            self.errors["email"] = _("error_invalid_email",
                    default=u"Please enter a valid email address")
        if not reply.get("password1"):
            self.errors["password"] = _("error_missing_password",
                    default=u"Please enter a password")
        elif reply.get("password1") != reply.get("password2"):
            self.errors["password"] = _("error_password_mismatch",
                    default=u"Passwords do not match")
        if self.errors:
            return False

        session = Session()
        loginname = loginname.lower()
        account = session.query(Account)\
                .filter(Account.loginname == loginname).count()
        if account:
            self.errors["email"] = _("error_email_in_use",
                default=u"An account with this email address already exists.")
            return False

        pm = getToolByName(self.context, "portal_membership")
        if pm.getMemberById(loginname) is not None:
            self.errors["email"] = _("error_email_in_use",
                default=u"An account with this email address already exists.")
            return False

        account = Account(loginname=loginname,
                                password=reply.get("password1"))
        Session().add(account)
        log.info("Registered new account %s", loginname)
        return account

    def update(self):
        self.errors = {}
        if self.request.environ["REQUEST_METHOD"] == "POST":
            account = self._tryRegistration()
            if account:
                pas = getToolByName(self.context, "acl_users")
                pas.updateCredentials(self.request, self.request.response,
                        account.getUserName(), account.password)

                country_url = aq_inner(self.context).absolute_url()
                came_from = self.request.form.get("came_from")
                if not came_from:
                    came_from = country_url

                if checkTermsAndConditions():
                    self.request.response.redirect(
                            "%s/terms-and-conditions?%s" % (
                                self.request.client.absolute_url(),
                                urllib.urlencode({"came_from": came_from})))
                else:
                    self.request.response.redirect(came_from)


class Logout(grok.CodeView):
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)

    def render(self):
        SessionManager.stop()

        pas = getToolByName(self.context, "acl_users")
        pas.resetCredentials(self.request, self.request.response)

        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                break
        else:
            obj = self.request.client

        self.request.response.redirect(obj.absolute_url())
