import hashlib
import hmac
from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserAuth
from . import JsonView
from .entry import API
from ..user import IUser


def _get_user(context, login):
    membrane = getToolByName(context, 'membrane_tool')
    user = membrane.getUserObject(login=login)
    if not IUser.providedBy(user):
        return None
    else:
        return user


def generate_token(user):
    """Convenience utility to generate token for the user.
    """
    manager = getUtility(IKeyManager)
    hasher = hmac.new(manager.secret(), digestmod=hashlib.sha256)
    hasher.update(user.login)
    # Note that unlike authenticate_credentials we access the password
    # directly here. This is fine since here we do not care how the password
    # is stored: even if it is hashed the token will be fine.
    hasher.update(user.password.encode('utf-8'))
    return '%s-%s' % (user.login, hasher.hexdigest())


def authenticate_token(context, token):
    try:
        (login, hash) = token.split('-')
    except ValueError:
        return None
    user = _get_user(context, login)
    if user is None or generate_token(user) != token:
        return None
    else:
        return user


def authenticate_credentials(context, login, password):
    user = _get_user(context, login)
    if user is None:
        return None
    # We could check user.password directly, but lets defer to the membrane
    # auth framework so the password checking code is all in one place.
    auth = IMembraneUserAuth(user, None)
    if auth is None:
        return None
    if auth.locked:
        return None
    info = auth.authenticateCredentials(
            {'login': login, 'password': password})
    if info is None:
        return None
    else:
        return user


class Authenticate(JsonView):
    grok.context(API)
    grok.name('authenticate')
    grok.require('zope2.Public')

    def do_POST(self):
        """Try to authenticate a user.
        """
        try:
            login = self.input['login']
            password = self.input['password']
        except (KeyError, TypeError):
            self.request.response.setStatus(403)
            return {'type': 'error',
                    'message': 'Required data missing'}

        user = authenticate_credentials(self.context, login, password)
        if user is None:
            self.request.response.setStatus(403)
            return {'type': 'error',
                    'message': 'Invalid credentials'}

        return {'token': generate_token(user),
                'title': user.title,
                'login': user.login,
                'path': user.absolute_url(),  # XXX Need to be API-ized?
               }
