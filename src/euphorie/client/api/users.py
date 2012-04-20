from five import grok
from euphorie.client.api.interfaces import IClientAPISkinLayer
from euphorie.client.survey import PathGhost


class Users(PathGhost):
    """Entry point for the users."""


class Authenticate(grok.View):
    grok.context(Users)
    grok.layer(IClientAPISkinLayer)
    grok.name('authenticate')

    def render(self):
        """Try to authenticate a user.
        """
        return 'ok!'
