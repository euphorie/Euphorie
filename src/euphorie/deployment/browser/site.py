# coding=utf-8
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.content.api.entry import access_api
from euphorie.content.countrymanager import ICountryManager
from plone import api
from plone.memoize.view import memoize_contextless
from plone.protect.interfaces import IDisableCSRFProtection
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView
from Products.membrane.interfaces.user import IMembraneUser
from time import time
from zope.component import adapter
from zope.interface import alsoProvides
from ZPublisher.BaseRequest import DefaultPublishTraverse

import six


class Frontpage(BrowserView):

    def __call__(self):
        user = getSecurityManager().getUser()
        if IMembraneUser.providedBy(user):
            mt = getToolByName(self.context, "membrane_tool")
            obj = mt.getUserObject(user_id=user.getUserId())
            if ICountryManager.providedBy(obj):
                return self.request.response.redirect(
                    aq_parent(obj).absolute_url()
                )
            return self.request.response.redirect(obj.absolute_url())
        portal = aq_inner(self.context)
        return self.request.response.redirect(
            "%s/sectors/" % portal.absolute_url()
        )


@adapter(IPloneSiteRoot, NuPloneSkin)
class SitePublishTraverser(DefaultPublishTraverse):
    """Publish traverser to manage access to the CMS API.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent since in Zope 2 that is only fired for site objects.
    """

    def publishTraverse(self, request, name):
        if name == 'api':
            return access_api(request).__of__(self.context)
        return super(SitePublishTraverser, self).publishTraverse(request, name)


class EuphorieRefreshResourcesTimestamp(BrowserView):

    @property
    @memoize_contextless
    def resources_timestamp(self):
        return api.portal.get_registry_record(
            'euphorie.deployment.resources_timestamp',
            default='',
        )

    def refresh_timestamp(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        api.portal.set_registry_record(
            'euphorie.deployment.resources_timestamp',
            six.text_type(int(time())),
        )

    def __call__(self):
        ''' Refresh the registry record that adds a timestamp
        to the resources urls
        '''
        self.refresh_timestamp()
        return 'OK'
