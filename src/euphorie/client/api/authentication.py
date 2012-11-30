import hashlib
import hmac
from zope.component import getUtility
from z3c.saconfig import Session
from plone.keyring.interfaces import IKeyManager
from euphorie.client import model


def generate_token(account):
    """Convenience utility to generate token for the user."""
    manager = getUtility(IKeyManager)
    hasher = hmac.new(manager.secret(), digestmod=hashlib.sha256)
    hasher.update(account.loginname)
    if account.password:
        hasher.update(account.password.encode('utf-8'))
    return '%d-%s' % (account.id, hasher.hexdigest())


def authenticate_token(token):
    try:
        (account_id, hash) = token.split('-')
        account_id = int(account_id)
    except ValueError:
        return None

    account = Session().query(model.Account).get(account_id)
    if account is None or generate_token(account) != token:
        return None
    else:
        return (str(account_id), account.loginname)
