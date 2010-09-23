from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.membrane.interfaces.user import IMembraneUser
from euphorie.content.countrymanager import ICountryManager
from five import grok

class Frontpage(grok.View):
    grok.context(IPloneSiteRoot)
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.require("zope2.View")

    def render(self):
        user=getSecurityManager().getUser()
        if IMembraneUser.providedBy(user):
            mt=getToolByName(self.context, "membrane_tool")
            obj=mt.getUserObject(user_id=user.getUserId())
            if ICountryManager.providedBy(obj):
                self.request.response.redirect(aq_parent(obj).absolute_url())
            else:
                self.request.response.redirect(obj.absolute_url())
        else:
            portal=aq_inner(self.context)
            self.request.response.redirect("%s/sectors/" % portal.absolute_url())



