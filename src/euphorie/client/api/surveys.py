from Acquisition import aq_base
from five import grok
from euphorie.ghost import PathGhost
from ..country import IClientCountry
from . import JsonView
from .country import View as CountryView


class Surveys(PathGhost):
    """Virtual container for all survey data."""

    def __getitem__(self, key):
        country = self.request.client[key]
        if not IClientCountry.providedBy(country):
            raise KeyError(key)
        return aq_base(country).__of__(self)


class View(JsonView):
    grok.context(Surveys)
    grok.name('index_html')
    grok.require('zope2.Public')

    def country_info(self, country):
        view = CountryView(country, self.request)
        return view.do_GET()

    def do_GET(self):
        countries = [{'id': country.id,
                      'title': country.title,
                      'type': country.country_type}
                     for country in self.context.values()
                     if IClientCountry.providedBy(country)]
        return {'countries': countries}
