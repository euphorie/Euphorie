from . import JsonView
from ..authentication import authenticate
from ..model import Account
from .account import View as AccountView
from .account import login_available
from .authentication import authenticate_token
from .authentication import generate_token
from AccessControl.SecurityManagement import newSecurityManager
from euphorie.ghost import PathGhost
from five import grok
from plone.protect.interfaces import IDisableCSRFProtection
from z3c.saconfig import Session
from zope.interface import alsoProvides


def user_info(account, request):
    view = AccountView(account, request)
    return view.do_GET()


class Users(PathGhost):
    """Virtual container for all user data."""

    def __getitem__(self, key):
        token = self.request.getHeader('X-Euphorie-Token')
        uid_and_login = authenticate_token(token)
        if uid_and_login is None or key != uid_and_login[0]:
            raise KeyError(key)
        account = Session().query(Account).get(int(uid_and_login[0]))
        account.getId = lambda: key
        newSecurityManager(None, account)
        return account.__of__(self)


class View(JsonView):
    grok.context(Users)
    grok.name('index_html')
    grok.require('zope2.Public')

    def do_POST(self):
        try:
            login = self.input['login'].strip().lower()
            if not login_available(login):
                return {'type': 'error',
                        'message': 'Loginname already in use.'}
            password = self.input.get('password', '\x00')
        except KeyError:
            return {'type': 'error',
                    'message': 'Required data missing'}

        account = Account(loginname=login, password=password)
        session = Session()
        session.add(account)
        session.flush()

        info = user_info(account, self.request)
        info['token'] = generate_token(account)
        alsoProvides(self.request, IDisableCSRFProtection)
        return info


class Authenticate(JsonView):
    grok.context(Users)
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

        account = authenticate(login, password)
        if account is None:
            self.request.response.setStatus(403)
            return {'type': 'error',
                    'message': 'Invalid credentials'}

        info = user_info(account, self.request)
        info['token'] = generate_token(account)
        alsoProvides(self.request, IDisableCSRFProtection)
        return info
