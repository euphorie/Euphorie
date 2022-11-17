# coding=utf-8

from Acquisition import aq_base
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.country import IClientCountry
from json import dumps
from plone import api
from Products.Five import BrowserView


class ClientView(WebHelpers):
    def __call__(self):
        """The frontpage has been disbanded. We redirect to the country that
        is defined as the default, or pick a random country.
        """
        target = None
        language = self.request.form.get("language")
        url_param = language and "?language=%s" % language or ""
        if self.default_country:
            if getattr(aq_base(self.context), self.default_country, None):
                found = getattr(self.context, self.default_country)
                if IClientCountry.providedBy(found):
                    target = found
        if not target:
            for id, found in self.context.objectItems():
                if IClientCountry.providedBy(found):
                    target = found
                    break
        if not target:
            return "No country was identified"
        self.request.RESPONSE.redirect("{}{}".format(target.absolute_url(), url_param))


class MailingListsJson(BrowserView):
    """Mailing lists (countries, in the future also sectors and tools)"""

    def __call__(self):
        """Json list of mailing list ids/names"""
        lists = []
        catalog = api.portal.get_tool(name="portal_catalog")
        self.request.response.setHeader("Content-type", "application/json")
        # TODO: require query.
        # q = self.request.get("q", "").strip().lower()
        # if not q:
        #     return dumps([])

        all_users = {"id": "all", "text": "All OiRA users"}
        # if q in all_users["id"] or q in all_users["text"].lower():
        lists.append(all_users)

        # FIXME: SearchableText="de*" doesn't return Germany
        countries = catalog(portal_type="euphorie.clientcountry")
        lists.extend(
            [{"id": country["id"], "text": country["Title"]} for country in countries]
        )
        # TODO: add sectors and tools

        return dumps(lists)
