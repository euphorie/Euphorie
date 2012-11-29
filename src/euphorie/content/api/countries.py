from Acquisition import aq_parent
from five import grok
from euphorie.ghost import PathGhost
from ..country import ICountry
from .country import country_info
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

    def do_GET(self):
        site = aq_parent(aq_parent(self.context))
        return {'countries': [country_info(country)
                              for country in site.sectors.values()
                              if ICountry.providedBy(country)]}
