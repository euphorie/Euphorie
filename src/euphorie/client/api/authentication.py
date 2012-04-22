import binascii
import json
import logging
from zope.component import getUtility
from z3c.saconfig import Session
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from OFS.Cache import Cacheable
from plone.keyring.interfaces import IKeyManager
from Products.CMFCore.utils import getToolByName
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.utils import createViewName
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from euphorie.client.authentication import graceful_recovery
from euphorie.client.api.interfaces import IClientAPISkinLayer
from euphorie.client import model
from plone.session import tktauth


log = logging.getLogger(__name__)


manage_addEuphorieAPIPlugin = PageTemplateFile('templates/addPasPlugin',
        globals(), __name__='manage_addEuphorieAPIPlugin')


def generate_token(context, account):
    """Convenience utility to generate token for the user."""
    pas = getToolByName(context, 'acl_users')
    return pas.euphorie_api.generate_token(account)


def addEuphorieAPIPlugin(self, id, title='', REQUEST=None):
    '''Add an EuphorieAPIPlugin to a Pluggable Authentication Service.
    '''
    p = EuphorieAPIPlugin(id, title)
    self._setObject(p.getId(), p)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace'
                '?manage_tabs_message=API+Authentication+plugin+added.' %
                self.absolute_url())


class EuphorieAPIPlugin(BasePlugin, Cacheable):
    """API authentication PAS plugin.

    This plugin leverages the auth_tkt logic from plone.session: it generates
    an auth ticket which is used as the token, but signed with a local secret
    instead of the plone.session secret.
    """
    meta_type = 'Euphorie API authentication'
    security = ClassSecurityInfo()

    manage_options = BasePlugin.manage_options + Cacheable.manage_options

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePrivate('_getSecret')
    def _getSecret(self):
        manager = getUtility(IKeyManager)
        return manager.secret()

    security.declarePrivate('authenticateCredentials')
    def generate_token(self, account):
        ticket = tktauth.createTicket(self._getSecret(), str(account.id))
        return binascii.b2a_base64(ticket).strip()

    # IAuthenticationPlugin implementation
    security.declarePrivate('authenticateCredentials')
    def extractCredentials(self, request):
        token = request.getHeader('X-Euphorie-Token')
        try:
            return {'api-token': binascii.a2b_base64(token)}
        except (TypeError, binascii.Error):
            return {}

    # IAuthenticationPlugin implementation
    security.declarePrivate('authenticateCredentials')
    @graceful_recovery(log_args=False)
    def authenticateCredentials(self, credentials):
        token = credentials.get('api-token')
        if not token:
            return None
        info = tktauth.validateTicket(self._getSecret(), token)
        if not info:
            return None
        login = self._getLogin(info[1])
        if not login:
            return None
        return (login, login)

    # IChallengePlugin implementation
    def challenge(self, request, response):
        if not IClientAPISkinLayer.providedBy(request):
            return False

        response.setHeader('Content-Type', 'application/json')
        response.setBody(json.dumps({
            'type': 'error',
            'message': 'Authentication required'}))
        return True

    # Utility functiones
    def _getLogin(self, userid):
        '''Utility function to check if a loginname is valid.'''
        viewname = createViewName('_getLogin', userid)
        keywords = {'userid': userid}
        result=self.ZCacheable_get(view_name=viewname, keywords=keywords,
                default=None)
        if result is not None:
            return result

        account = Session().query(model.Account).get(int(userid))
        result = account.loginname if account is not None else None
        self.ZCacheable_set(result, view_name=viewname, keywords=keywords)
        return result


classImplements(
    EuphorieAPIPlugin,
    IAuthenticationPlugin,
    IExtractionPlugin,
    IChallengePlugin)

InitializeClass(EuphorieAPIPlugin)
