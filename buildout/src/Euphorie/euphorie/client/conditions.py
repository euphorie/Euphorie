from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from AccessControl import getSecurityManager
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client import CONDITIONS_VERSION

grok.templatedir("templates")


def approvedTermsAndConditions(account=None):
    return True

    if account is None:
        account=getSecurityManager().getUser()
    return account.tc_approved is not None and account.tc_approved==CONDITIONS_VERSION



class TermsAndConditions(grok.View):
    grok.name("terms-and-conditions")
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("conditions")

    def terms_changed(self):
        return self.account.tc_approved is not None


    def update(self):
        self.came_from=self.request.form.get("came_from")
        if isinstance(self.came_from, list):
            # If came_from is both in the querystring and the form data
            self.came_from=self.came_from[0]

        self.account=getSecurityManager().getUser()
        if self.request.environ["REQUEST_METHOD"]=="POST":
            self.account.tc_approved=CONDITIONS_VERSION

            if self.came_from:
                self.request.response.redirect(self.came_from)
            else:
                self.request.response.redirect(
                        aq_inner(self.context).absolute_url())

