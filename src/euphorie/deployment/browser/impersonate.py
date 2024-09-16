from AccessControl import Unauthorized
from AccessControl.SecurityManagement import noSecurityManager
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import Account
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.saconfig import Session
from zope.interface import alsoProvides


class Impersonate(BrowserView):
    """@@impersonate view."""

    template = ViewPageTemplateFile("templates/impersonate.pt")

    def __call__(self):
        self.actions()
        return self.template()

    def actions(self):
        """Login the user"""
        if "username" in list(self.request.keys()):
            self.errors = {}
            alsoProvides(self.request, IClientSkinLayer)
            username = self.request["username"].strip()

            try:
                self.context.acl_users.logout(self.request)
            except Unauthorized:
                pass
            noSecurityManager()

            account = (
                Session.query(Account).filter(Account.loginname == username).first()
            )
            if account is None:
                self.errors[username] = username
                return
            self.context.acl_users.session._setupSession(
                account.loginname,
                self.request.RESPONSE,
            )

            self.request.RESPONSE.redirect(api.portal.get().client.absolute_url())
