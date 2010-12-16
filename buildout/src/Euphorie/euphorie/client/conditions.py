from zope.interface import Interface
from five import grok
from AccessControl import getSecurityManager
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client import CONDITIONS_VERSION

grok.templatedir("templates")

class TermsAndConditions(grok.View):
    grok.name("terms-and-conditions")
    grok.context(Interface)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("conditions")

    def terms_changed(self):
        return self.account.tc_approved is not None


    def update(self):
        self.account=getSecurityManager().getUser()
        if self.request.environ["REQUEST_METHOD"]=="POST":
            self.account.tc_approved=CONDITIONS_VERSION

