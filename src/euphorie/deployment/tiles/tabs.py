import re
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces.user import IMembraneUser
from plonetheme.nuplone.tiles.tabs import TabsTile
from plonetheme.nuplone.utils import getPortal
from plonetheme.nuplone.utils import checkPermission
from euphorie.content import MessageFactory as _
from euphorie.content.countrymanager import ICountryManager
from euphorie.content.country import ICountry


class SiteRootTabsTile(TabsTile):
    current_map = [
            (re.compile(r"/sectors/[a-z]+/*@@manage-users"), "usermgmt"),
            (re.compile(r"/sectors/[a-z]+/help"), "help"),
            (re.compile(r"/sectors"), "sectors"),
            (re.compile(r"/documents"), "documents")]

    def update(self):
        context = aq_inner(self.context)
        portal = getPortal(context)
        currentUrl = self.request.getURL()[len(portal.absolute_url()):]
        user = getSecurityManager().getUser()

        if IMembraneUser.providedBy(user):
            mt = getToolByName(self.context, "membrane_tool")
            user_object = mt.getUserObject(user_id=user.getUserId())
        else:
            user_object = None

        for (test, id) in self.current_map:
            if test.match(currentUrl):
                current = id
                break
        else:
            current = None

        results = [{"id": "sectors",
                    "title": _("nav_surveys", default=u"OiRA Tools"),
                    "url": portal.sectors.absolute_url(),
                    "class": "current" if current == "sectors" else None}]

        if checkPermission(portal, "Manage portal"):
            for country in aq_chain(context):
                if ICountry.providedBy(country):
                    url = "%s/@@manage-users" % country.absolute_url()
                    break
            else:
                countries = sorted(portal.sectors.keys())
                url = "%s/@@manage-users" % \
                        portal.sectors[countries[0]].absolute_url()
            results.append({"id": "usermgmt",
                            "title": _("nav_usermanagement",
                                        default=u"User management"),
                            "url": url,
                            "class": "current" if current == "usermgmt"
                                                else None})
            results.append({"id": "documents",
                            "title": _("nav_documents", default=u"Documents"),
                            "url": portal.documents.absolute_url(),
                            "class": "current" if current == "documents"
                                                else None})
        elif ICountryManager.providedBy(user_object):
            country = aq_parent(user_object)
            results.append({"id": "usermgmt",
                            "title": _("nav_usermanagement",
                                        default=u"User management"),
                            "url": "%s/@@manage-users" %
                                        country.absolute_url(),
                            "class": "current" if current == "usermgmt"
                                                else None})

        if user_object is not None:
            country = aq_parent(user_object)
            results.append({"id": "help",
                            "title": _("nav_help", default=u"Help"),
                            "url": "%s/help" % country.absolute_url(),
                            "class": "current" if current == "help"
                                                else None})

        self.tabs = results
        self.home_url = portal.absolute_url()
