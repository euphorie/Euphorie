# coding=utf-8
from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.content import MessageFactory as _
from euphorie.content.country import ICountry
from plone import api
from plone.memoize.view import memoize_contextless
from plonetheme.nuplone.tiles.tabs import TabsTile

import re


class SiteRootTabsTile(TabsTile):
    current_map = [
        (re.compile(r"/sectors/[a-z]+/*@@manage-users"), "usermgmt"),
        (re.compile(r"/sectors/[a-z]+/help"), "help"),
        (re.compile(r"/sectors"), "sectors"),
        (re.compile(r"/documents"), "documents"),
    ]

    @property
    @memoize_contextless
    def portal(self):
        return api.portal.get()

    @property
    @memoize_contextless
    def user(self):
        return api.user.get_current()

    def get_current_country(self):
        for obj in aq_chain(aq_inner(self.context)):
            if ICountry.providedBy(obj):
                return obj

    def is_country_manager(self):
        ''' Check if we are in the context of a country and
        if we have enough permissions to manage it
        '''
        country = self.get_current_country()
        if not country:
            return False
        if api.user.has_permission('Euphorie: Manage country', obj=country):
            return True

    def get_current_url(self):
        currentUrl = self.request.getURL()[len(self.portal.absolute_url()):]
        for (test, id) in self.current_map:
            if test.match(currentUrl):
                return id

    def update(self):
        current = self.get_current_url()
        self.tabs = [{
            "id": "sectors",
            "title": _("nav_surveys", default=u"OiRA Tools"),
            "url": self.portal.sectors.absolute_url(),
            "class": "current" if current == "sectors" else None,
        }]
        is_country_manager = self.is_country_manager()
        if is_country_manager:
            country = self.get_current_country()
            country_url = country.absolute_url()
            self.tabs.append({
                "id": "usermgmt",
                "title": _("nav_usermanagement", default=u"User management"),
                "url": '%s/@@manage-users' % country_url,
                "class": "current" if current == "usermgmt" else None,
            })

        if api.user.has_permission('Manage portal', user=self.user):
            self.tabs.append({
                "id": "documents",
                "title": _("nav_documents", default=u"Documents"),
                "url": self.portal.documents.absolute_url(),
                "class": "current" if current == "documents" else None,
            })

        if is_country_manager:
            self.tabs.append({
                "id": "help",
                "title": _("nav_help", default=u"Help"),
                "url": "%s/help" % country.absolute_url(),
                "class": "current" if current == "help" else None,
            })

        self.home_url = self.portal.absolute_url()
