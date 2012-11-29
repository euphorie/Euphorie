from Acquisition import aq_base
from five import grok
from euphorie.ghost import PathGhost
from ..sector import ISector
from . import JsonView


def list_sectors(country):
    return [{'id': sector.id,
             'title': sector.title,
             'login': sector.login,
             'locked': sector.locked,
            } for sector in country.values()
            if ISector.providedBy(sector)]


class Sectors(PathGhost):
    def __init__(self, id, request, country):
        super(Sectors, self).__init__(id, request)
        self.country = country

    def __getitem__(self, key):
        sector = self.country[key]
        if ISector.providedBy(sector):
            return aq_base(sector).__of__(self)
        raise KeyError(key)


class View(JsonView):
    grok.context(Sectors)
    grok.require('zope2.View')
    grok.name('index_html')

    def do_GET(self):
        return {'sectors': list_sectors(self.context)}
