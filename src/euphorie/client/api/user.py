from euphorie.client.survey import PathGhost
from five import grok
from euphorie.client.api import JsonView


class User(PathGhost):
    """A minimal wrapper around a user to expose it to the publisher.
    """

    def __init__(self, id, request, account):
        super(User, self).__init__(id, request)
        self.account = account


class View(JsonView):
    grok.context(User)
    grok.require('zope2.Public')  # XXX should be zope2.View
    grok.name('index_html')

    def sessions(self):
        return [{'id': session.id,
                 'title': session.title,
                 'modified': session.modified.isoformat()}
                for session in self.context.account.sessions]

    def render(self):
        """Try to authenticate a user.
        """
        account = self.context.account
        return {'type': 'user',
                'id': self.context.id,
                'login': account.loginname,
                'email': account.email,
                'sessions': self.sessions()}
