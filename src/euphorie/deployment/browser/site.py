# coding=utf-8
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.content.api.entry import access_api
from euphorie.content.countrymanager import ICountryManager
from euphorie.content.risk import EnsureInterface
from euphorie.content.risk import IRisk
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
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


import logging
import six

log = logging.getLogger(__name__)


class Frontpage(BrowserView):
    def __call__(self):
        user = getSecurityManager().getUser()
        if IMembraneUser.providedBy(user):
            mt = getToolByName(self.context, "membrane_tool")
            obj = mt.getUserObject(user_id=user.getUserId())
            if ICountryManager.providedBy(obj):
                return self.request.response.redirect(aq_parent(obj).absolute_url())
            return self.request.response.redirect(obj.absolute_url())
        portal = aq_inner(self.context)
        return self.request.response.redirect("%s/sectors/" % portal.absolute_url())


@adapter(IPloneSiteRoot, NuPloneSkin)
class SitePublishTraverser(DefaultPublishTraverse):
    """Publish traverser to manage access to the CMS API.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent since in Zope 2 that is only fired for site objects.
    """

    def publishTraverse(self, request, name):
        if name == "api":
            return access_api(request).__of__(self.context)
        return super(SitePublishTraverser, self).publishTraverse(request, name)


class EuphorieRefreshResourcesTimestamp(BrowserView):
    @property
    @memoize_contextless
    def resources_timestamp(self):
        return api.portal.get_registry_record(
            "euphorie.deployment.resources_timestamp", default=""
        )

    def refresh_timestamp(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        api.portal.set_registry_record(
            "euphorie.deployment.resources_timestamp", six.text_type(int(time()))
        )

    def __call__(self):
        """ Refresh the registry record that adds a timestamp
        to the resources urls
        """
        self.refresh_timestamp()
        return "OK"


class ManageEnsureInterface(BrowserView):
    def set_evaluation_method_interfaces(self):
        def walk(node):
            for idx, sub_node in node.ZopeFind(node, search_sub=0):
                if IRisk.providedBy(sub_node):
                    yield sub_node
                if IDexterityContainer.providedBy(sub_node):
                    for sub_sub_node in walk(sub_node):
                        yield sub_sub_node

        count = 0
        walker = walk(self.context)
        for risk in walker:
            log.debug("Ensure interface for %s", "/".join(risk.getPhysicalPath()))
            EnsureInterface(risk)
            count += 1
        log.info("Ensured interface for %d risks", count)
        return count

    def __call__(self):
        """ Iterate over all risks in the current context and ensure that they have the
        correct interface
        """
        count = self.set_evaluation_method_interfaces()
        return "Handled %d risks" % count


class UpdateCompletionPercentage(WebHelpers):
    """ Utility view to fill in missing values for completion_percentage """

    flush_threshold = 50

    def log(self, entry):
        log.info(entry)
        self._log = "\n".join((getattr(self, "_log", ""), entry))

    def get_log(self):
        return getattr(self, "_log", "")

    def next_b_start(self):
        if "overwrite" in self.request.form:
            return self.request.get("b_start", 0) + self.request.get("b_size", 1000)
        else:
            return 0

    def __call__(self):
        if self.request.method == "POST":
            self.log("Updating completion_percentage")
            b_size = self.request.get("b_size", 1000)
            b_start = self.request.get("b_start", 0)
            self.log("Limiting to {} sessions; starting at {}".format(b_size, b_start))
            query = Session.query(SurveySession)
            if "overwrite" not in self.request.form:
                query = query.filter(SurveySession.completion_percentage == None)
                self.log("Ignoring sessions with existing non-null values")
            else:
                self.log("Overwriting existing non-null values")
            query = (
                query
                .order_by(SurveySession.modified.desc())
                .offset(b_start)
                .limit(b_size)
            )
            total = query.count()
            self.log("Found {} sessions".format(total))
            cnt = 0
            for session in query:
                self.update_completion_percentage(session)
                cnt += 1
                if cnt % self.flush_threshold == 0:
                    self.log("Handled {0} out of {1} sessions".format(cnt, total))
            self.log("Done")
        return self.index()
