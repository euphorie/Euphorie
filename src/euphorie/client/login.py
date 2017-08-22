"""
Login
-----

Register new users, login/logout, create a "Guest user" account and convert
existing guest accounts to normal accounts.
"""

from .. import MessageFactory as _
from .conditions import approvedTermsAndConditions
from .conditions import checkTermsAndConditions
from .country import IClientCountry
from .country import View as CountryView
from .interfaces import IClientSkinLayer
from .session import SessionManager
from .utils import CreateEmailTo
from .utils import setLanguage
from AccessControl import getSecurityManager
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client import config
from euphorie.client import model
from euphorie.content.survey import ISurvey
from five import grok
from plone import api
from plone.session.plugins.session import cookie_expiration_date
from plonetheme.nuplone.tiles.analytics import trigger_extra_pageview
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from z3c.saconfig import Session
from zope import component
from zope.i18n import translate
from zope.interface import Interface
import cgi
import datetime
import logging
import os
import re
import smtplib
import socket
import urllib
import urlparse

log = logging.getLogger(__name__)

# I know this is a stupid regular expression, but it Works For Us(tm)
EMAIL_RE = re.compile(
    r'[_a-z0-9+-]+(\.[_a-z0-9+-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})',
    re.IGNORECASE)

grok.templatedir("templates")


class Login(grok.View):
    """View name: @@login"""
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("login")
    grok.template("login")

    def setLanguage(self, came_from):
        qs = urlparse.urlparse(came_from)[4]
        params = cgi.parse_qs(qs)
        lang = params.get("language")
        if not lang:
            if IClientCountry.providedBy(self.context):
                lang = getattr(self.context, 'language', None)
                if lang and isinstance(lang, basestring):
                    lang = [lang]
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

    def transferGuestSession(self, session_id):
        """ Transfer guest session to an existing user account
        """
        if not session_id:
            return
        account = getSecurityManager().getUser()
        session = Session.query(model.SurveySession).get(session_id)
        session.account_id = account.id
        SessionManager.resume(session)

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

        account = getSecurityManager().getUser()
        appconfig = component.getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.allow_guest_accounts = settings.get('allow_guest_accounts', False)

        if self.request.environ["REQUEST_METHOD"] == "POST":
            reply = self.request.form
            if reply["next"] == "previous":
                next = aq_parent(aq_inner(context)).absolute_url()
                self.response.redirect(next)
                return

            if isinstance(account, model.Account) and \
                    account.getUserName() == reply.get("__ac_name", '').lower():

                self.transferGuestSession(reply.get('guest_session_id'))
                self.login(account, bool(self.request.form.get('remember')))
                v_url = urlparse.urlsplit(self.url()+'/success').path
                trigger_extra_pageview(self.request, v_url)

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
        self.tryout_url = "%s/@@tryout?%s" % (context.absolute_url(),
                urllib.urlencode({'came_from': came_from}))


class LoginForm(Login):
    """View name: @@login_form"""
    grok.layer(IClientSkinLayer)
    grok.name("login_form")
    grok.template("login_form")


class Tryout(Login):
    """Create a guest account

    View name: @@tryout
    """
    grok.context(Interface)
    grok.require("zope2.Public")
    grok.layer(IClientSkinLayer)
    grok.name("tryout")

    def createGuestAccount(self):
        account = model.Account(
            loginname="guest-%s" % datetime.datetime.now().isoformat(),
            account_type=config.GUEST_ACCOUNT
        )
        Session().add(account)
        return account

    def update(self):
        came_from = self.request.form.get("came_from")
        if not came_from:
            return self.request.response.redirect(api.portal.get().absolute_url())
        account = self.createGuestAccount()
        self.login(account, False)
        client_url = self.request.client.absolute_url()
        came_from = came_from.replace(client_url, '')
        if came_from.startswith('/'):
            came_from = came_from[1:]
        try:
            survey = self.context.restrictedTraverse(came_from)
        except KeyError:
            survey = None
        if not ISurvey.providedBy(survey):
            return self.request.response.redirect(came_from)
        title = survey.Title()
        SessionManager.start(title=title, survey=survey, account=account)
        survey_url = survey.absolute_url()
        v_url = urlparse.urlsplit(survey_url + '/resume').path
        trigger_extra_pageview(self.request, v_url)
        self.request.response.redirect("%s/start" % survey_url)


class CreateTestSession(CountryView, Tryout):
    """Create a guest session

    View name: @@new-session-test.html
    """
    grok.context(Interface)
    grok.require("zope2.View")
    grok.name("new-session-test.html")
    grok.template("new-session-test")

    def update(self):
        appconfig = component.getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.allow_guest_accounts = settings.get('allow_guest_accounts', False)
        context = aq_inner(self.context)
        came_from = self.request.form.get("came_from")
        if came_from:
            if isinstance(came_from, list):
                # If came_from is both in the querystring and the form data
                came_from = came_from[0]
        else:
            came_from = context.absolute_url()
        self.register_url = "%s/@@register?%s" % (
            context.absolute_url(), urllib.urlencode({'came_from': came_from}))
        setLanguage(self.request, self.context)
        if self.request.environ["REQUEST_METHOD"] == "POST":
            if not self.allow_guest_accounts:
                flash = IStatusMessage(self.request).addStatusMessage
                flash(_(u"Starting a test session is not available in this OiRA "
                      u"application."), "error")
                self.request.response.redirect(came_from)
            else:
                reply = self.request.form
                if reply["action"] == "new":
                    account = self.createGuestAccount()
                    self.login(account, False)
                    self._NewSurvey(reply, account)
        self._updateSurveys()


class Reminder(grok.View):
    """Send a password reminder by email
    """
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

        account = Session.query(model.Account)\
                .filter(model.Account.loginname == loginname).first()
        if not account:
            self.error = _(u"Unknown email address")
            return False

        site = component.getUtility(ISiteRoot)
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
        except MailHostError as e:
            log.error("MailHost error sending password reminder to %s: %s",
                    account.email, e)
            self.error = _(
                    u"An error occured while sending the password reminder")
            return False
        except smtplib.SMTPException as e:
            log.error("smtplib error sending password reminder to %s: %s",
                    account.email, e)
            self.error = _(
                    u"An error occured while sending the password reminder")
            return False
        except socket.error as e:
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
            if self.request.form.get('cancel', ''):
                self.request.response.redirect(self.back_url)
            if self._sendReminder():
                flash = IStatusMessage(self.request).addStatusMessage
                flash(_(u"An email with a password reminder has been "
                        u"sent to your address."), "notice")
                redir_url = self.back_url
                if not redir_url.endswith("login"):
                    redir_url = "{0}/@@login?{1}".format(
                        redir_url, urllib.urlencode({"came_from": redir_url}))
                self.request.response.redirect(redir_url)


class Register(grok.View):
    """Register a new account or convert an existing guest account
    """
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
        account = session.query(model.Account)\
                .filter(model.Account.loginname == loginname).count()
        if account:
            self.errors["email"] = _("error_email_in_use",
                default=u"An account with this email address already exists.")
            return False

        pm = getToolByName(self.context, "portal_membership")
        if pm.getMemberById(loginname) is not None:
            self.errors["email"] = _("error_email_in_use",
                default=u"An account with this email address already exists.")
            return False

        guest_session_id = self.request.form.get('guest_session_id')
        if guest_session_id:
            account = getSecurityManager().getUser()
            account.loginname = loginname
            account.password = reply.get("password1")
            account.account_type = config.CONVERTED_ACCOUNT
        else:
            account = model.Account(
                loginname=loginname,
                password=reply.get("password1")
            )
        Session().add(account)
        log.info("Registered new account %s", loginname)
        v_url = urlparse.urlsplit(self.url()+'/success').path
        trigger_extra_pageview(self.request, v_url)
        return account

    def update(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        self.email_message = translate(_(
            u"invalid_email",
            default=u"Please enter a valid email address."),
            target_language=lang)
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

    def get_image_version(self, name):
        """" Needed on the reports overview show to the guest user """
        fdir = os.path.join(
            os.path.dirname(__file__), os.path.join('templates', 'media'))
        lang = getattr(self.request, 'LANGUAGE', 'en')
        fname = "{0}_{1}".format(name, lang)
        if os.path.isfile(os.path.join(fdir, fname + '.png')):
            return fname
        return name


class Logout(grok.View):
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
