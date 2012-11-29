from Acquisition import aq_parent
from five import grok
from euphorie.ghost import PathGhost
from ..country import ICountry
from . import JsonView


class Countries(PathGhost):
    """Virtual container for all countries."""

    def __getitem__(self, key):
        site = aq_parent(aq_parent(self))
        return site.sectors[key]


class View(JsonView):
    grok.context(Countries)
    grok.require('zope2.View')
    grok.name('index_html')

    def _morph(self, country):
        return {'id': country.id,
                'title': country.title,
                'country-type': country.country_type,
               }

    def do_GET(self):
        site = aq_parent(aq_parent(self.context))
        return {'countries': [self._morph(country)
                              for country in site.sectors.values()
                              if ICountry.providedBy(country)]}
