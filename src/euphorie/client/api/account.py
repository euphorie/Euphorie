from z3c.saconfig import Session
from five import grok
from euphorie.client.model import Account
from euphorie.client.survey import PathGhost
from euphorie.client.api import JsonView


class View(JsonView):
    grok.context(Account)
    grok.require('zope2.View')
    grok.name('index_html')

    def sessions(self):
        return [{'id': session.id,
                 'title': session.title,
                 'modified': session.modified.isoformat()}
                for session in self.context.sessions]

    def render(self):
        """Try to authenticate a user.
        """
        return {'type': 'user',
                'id': self.context.id,
                'login': self.context.loginname,
                'email': self.context.email,
                'sessions': self.sessions()}
