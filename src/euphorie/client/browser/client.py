# coding=utf-8

from Acquisition import aq_base
from euphorie.client.country import IClientCountry
from euphorie.client.browser.webhelpers import WebHelpers


class ClientView(WebHelpers):

    def __call__(self):
        """ The frontpage has been disbanded. We redirect to the country that
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
            return self
        self.request.RESPONSE.redirect("{}{}".format(
            target.absolute_url(), url_param))
