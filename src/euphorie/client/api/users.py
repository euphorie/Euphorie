from five import grok
from euphorie.client.authentication import authenticate
from euphorie.client.survey import PathGhost
from euphorie.client.api import JsonView


class Users(PathGhost):
    """Entry point for the users."""


class Authenticate(JsonView):
    grok.context(Users)
    grok.name('authenticate')
    grok.require('zope2.Public')

    def sessions(self, account):
        return [{'id': session.id,
                 'title': session.title,
                 'modified': session.modified.isoformat()}
                for session in account.sessions]

    def render(self):
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

        return {'type': 'user',
                'id': account.id,
                'login': account.loginname,
                'email': account.email,
                'token': 'token',
                'sessions': self.sessions(account)}
