# coding=utf-8
from euphorie import MessageFactory as _
from euphorie.client.model import Account
from euphorie.client.utils import CreateEmailTo
from logging import getLogger
from p01.widget.password.widget import PasswordComparsionError
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.memoize.view import memoize_contextless
from plone.schema import Email
from plone.supermodel import model
from Products.CMFPlone.PasswordResetTool import InvalidRequestError
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from z3c.form import button
from z3c.form.form import EditForm
from z3c.saconfig import Session
from zope import schema
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import smtplib
import socket
import urllib


logger = getLogger(__name__)


class ResetPasswordFormSchema(model.Schema):
    new_password = schema.Password(
        title=_(u'label_new_password', default=u'Desired password'),
    )


class ResetPasswordRequestSchema(model.Schema):
    email = Email(title=_(u'label_email', default=u'Email address'), )


class BaseForm(AutoExtensibleForm, EditForm):
    ''' Base class for password the reset forms
    '''
    title = ''
    description = ''

    @property
    def template(self):
        return self.index

    def redirect(self, target, msg='', msg_type='notice'):
        ''' Redirect the user to a meaningfull place and add a status message
        '''
        if msg:
            api.portal.show_message(msg, self.request, msg_type)
        self.request.response.redirect(target)

    def updateActions(self):
        ''' Fix the button classes
        '''
        super(BaseForm, self).updateActions()
        for action in self.actions.values():
            action.klass = 'pat-button'


class ResetPasswordRequest(BaseForm):
    ''' Request a link to reset the password
    '''
    ignoreContext = True
    schema = ResetPasswordRequestSchema

    label = _(
        u'title_reset_password_request',
        default=u'Password recovery',
    )
    description = _(
        'description_reset_password_request', (
            u'We will send you an email '
            u'with the instructions to reset your password.'
        )
    )

    email_template = ViewPageTemplateFile(
        'templates/password_recovery_email.pt'
    )

    @property
    def email_from_name(self):
        return api.portal.get_registry_record('plone.email_from_name')

    @property
    def email_from_address(self):
        return api.portal.get_registry_record('plone.email_from_address')

    def log_error(self, msg):
        ''' Log an error message, set the view error attribute and return False
        '''
        logger.error(msg)
        self.error = _(
            u'An error occured while sending the password reset instructions',
        )
        return False

    def send_mail(self, email):
        account = (
            Session.query(Account).filter(Account.loginname == email).first()
        )
        if not account:
            # We returned True even if the account
            # does not exist to not leak any information
            return True

        ppr = api.portal.get_tool('portal_password_reset')
        reset_info = ppr.requestReset(account.id)
        mailhost = api.portal.get_tool('MailHost')
        body = self.email_template(**reset_info)
        subject = translate(
            _(u'OiRA password reset instructions'),
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
                'Sent password reset instructions to %s',
                account.email,
            )
        except MailHostError as e:
            msg = (
                'MailHost error sending password reset instructions to {}: {}'
            ).format(account.email, e)
            return self.log_error(msg)
        except smtplib.SMTPException as e:
            msg = (
                'smtplib error sending password reset instructions to {}: {}'
            ).format(account.email, e)
            return self.log_error(msg)
        except socket.error as e:
            msg = (
                'Socket error sending password reset instructions to {}: {}'
            ).format(account.email, e[1])
            return self.log_error(msg)
        return True

    def do_next(self):
        data, error = self.extractData()
        if error:
            return
        if not self.send_mail(data['email']):
            return
        msg = _(
            u'An email will be sent '
            u'if we can find an account for the inserted email address'
        )
        redir_url = (
            self.request.get('came_from') or self.context.absolute_url()
        )
        if not redir_url.endswith('login'):
            redir_url = '{0}/@@login?{1}'.format(
                redir_url, urllib.urlencode({
                    'came_from': redir_url
                })
            )
        self.redirect(redir_url, msg)

    @button.buttonAndHandler(_(u'Save'))
    def next_handler(self, action):
        ''' Check if the security token is correct and if it is
        change the account password with the provided value
        '''
        self.do_next()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self.redirect(self.context.absolute_url())


@implementer(IPublishTraverse)
class ResetPasswordForm(BaseForm):
    ignoreContext = True
    schema = ResetPasswordFormSchema

    label = _(
        u'title_reset_password_form',
        default=u'Reset password',
    )
    description = _(
        u'description_reset_password_form',
        default=u'',
    )

    def publishTraverse(self, request, name):
        return self

    @property
    @memoize_contextless
    def key(self):
        ''' Extract the key from the URL
        '''
        return self.request.getURL().rpartition('/')[-1]

    def do_save(self):
        ''' Execute the save action
        '''
        (data, errors) = self.extractData()
        if errors:
            for err in errors:
                if isinstance(err.error, PasswordComparsionError):
                    err.message = _(
                        "error_password_mismatch",
                        default=u"Passwords do not match")
            return

        key = self.key
        ppr = api.portal.get_tool('portal_password_reset')

        try:
            ppr.verifyKey(key)
        except InvalidRequestError:
            return self.redirect(
                self.context.absolute_url() + '/@@reset_password_request',
                msg=_('Invalid security token, try to request a new one'),
                msg_type='error',
            )

        account_id = ppr._requests.get(key)[0]
        account = (
            Session().query(Account).filter(Account.id == account_id).one()
        )
        account.password = data['new_password']
        current_url = self.context.absolute_url()
        return self.redirect(
            '{}/@@login_form?{}'.format(
                current_url,
                urllib.urlencode(dict(came_from=current_url))
            ),
            msg=_('Your password was successfully changed.'),
        )

    @button.buttonAndHandler(_(u'Save changes'))
    def save_handler(self, action):
        ''' Check if the security token is correct and if it is
        change the account password with the provided value
        '''
        self.do_save()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self.redirect(self.context.absolute_url())
