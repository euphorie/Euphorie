from z3c.saconfig import Session
from five import grok
from euphorie.client.authentication import authenticate
from euphorie.client.api.authentication import generate_token
from euphorie.client.survey import PathGhost
from euphorie.client.api import JsonView
from euphorie.client.model import Account
from euphorie.client.api.user import User
from euphorie.client.api.user import View as UserView


class Users(PathGhost):
    """Entry point for the users."""

    def __getitem__(self, key):
        try:
            userid = int(key)
        except ValueError:
            raise KeyError(key)

        account = Session.query(Account).get(userid)
        if account is None:
            raise KeyError(key)

        return User(key, self.request, account).__of__(self)


class Authenticate(JsonView):
    grok.context(Users)
    grok.name('authenticate')
    grok.require('zope2.Public')

    def user_info(self, account):
        view = UserView(account, self.request)
        return view.render()

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

        info = self.user_info(account)
        info['token'] = generate_token(self.context, account)
        return info
