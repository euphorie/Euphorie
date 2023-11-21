from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Impersonate(BrowserView):
    """@@impersonate view."""

    template = ViewPageTemplateFile("templates/impersonate.pt")

    def __call__(self):
        __import__("pdb").set_trace()
        self.actions()
        return self.template()

    def actions(self):
        """Login the user"""
        if "username" in list(self.request.keys()):
            self.errors = {}
            username = self.request["username"].strip()

            self.context.acl_users.session._setupSession(
                username, self.context.REQUEST.RESPONSE
            )

            self.request.RESPONSE.redirect(api.portal.get().absolute_url())
