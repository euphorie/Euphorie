from zope.component import adapts
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from ZPublisher.BaseRequest import DefaultPublishTraverse
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.membrane.interfaces.user import IMembraneUser
from euphorie.content.countrymanager import ICountryManager
from euphorie.content.api.entry import access_api
from five import grok


class Frontpage(grok.View):
    grok.context(IPloneSiteRoot)
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.require("zope2.View")

    def render(self):
        user = getSecurityManager().getUser()
        if IMembraneUser.providedBy(user):
            mt = getToolByName(self.context, "membrane_tool")
            obj = mt.getUserObject(user_id=user.getUserId())
            if ICountryManager.providedBy(obj):
                self.request.response.redirect(aq_parent(obj).absolute_url())
            else:
                self.request.response.redirect(obj.absolute_url())
        else:
            portal = aq_inner(self.context)
            self.request.response.redirect(
                    "%s/sectors/" % portal.absolute_url())


class SitePublishTraverser(DefaultPublishTraverse):
    """Publish traverser to manage access to the CMS API.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent since in Zope 2 that is only fired for site objects.
    """
    adapts(IPloneSiteRoot, NuPloneSkin)

    def publishTraverse(self, request, name):
        if name == 'api':
            return access_api(request).__of__(self.context)
        return super(SitePublishTraverser, self)\
                .publishTraverse(request, name)
