from zope.component import adapts
from five import grok
from z3c.saconfig import Session
from euphorie.client.model import Account
from euphorie.client.api import JsonView
from euphorie.client.api.interfaces import IClientAPISkinLayer
from euphorie.client.api.session import get_survey
from euphorie.client.api.sessions import Sessions
from ZPublisher.BaseRequest import DefaultPublishTraverse


def login_available(login):
    """Check if a login name is still available.

    This assumes that the login name has already been lowercased.
    """
    others = Session.query(Account)\
            .filter(Account.loginname == login)\
            .count()
    return others == 0


class View(JsonView):
    grok.context(Account)
    grok.require('zope2.View')
    grok.name('index_html')

    def do_PUT(self):
        changes = {}
        for (key, value) in self.input.items():
            if not value:
                return {'type': 'error',
                        'message': 'Empty value not allowed.'}
            if key == 'password':
                changes['password'] = value
            elif key == 'login':
                value = value.lower()
                if value == self.context.loginname:
                    continue
                if not login_available(value):
                    return {'type': 'error',
                            'message': 'Loginname already in use.'}
                changes['loginname'] = value
        for (key, value) in changes.items():
            setattr(self.context, key, value)
        return self.do_GET()

    def sessions(self):
        return [{'id': session.id,
                 'survey': session.zodb_path,
                 'title': session.title,
                 'created': session.created.isoformat(),
                 'modified': session.modified.isoformat()}
                for session in self.context.sessions
                if get_survey(self.request, session.zodb_path) is not None]

    def do_GET(self):
        return {'type': 'user',
                'id': self.context.id,
                'login': self.context.loginname,
                'email': self.context.email,
                'sessions': self.sessions()}


class AccountPublishTraverse(DefaultPublishTraverse):
    """Publish traverser for accounts.
    """
    adapts(Account, IClientAPISkinLayer)

    def publishTraverse(self, request, name):
        if name == 'sessions':
            return Sessions(name, request, self.context).__of__(self.context)
        else:
            return super(AccountPublishTraverse, self).publishTraverse(
                    request, name)
