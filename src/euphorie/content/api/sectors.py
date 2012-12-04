from zExceptions import Unauthorized
from Acquisition import aq_base
from five import grok
from plone.dexterity.utils import createContent
from plone.dexterity.utils import addContentToContainer
from euphorie.ghost import PathGhost
from euphorie.json import get_json_unicode
from ..sector import ISector
from .sector import View as SectorView
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

    attributes = SectorView.attributes + [
            ('login', 'login', get_json_unicode),
            ]

    def do_GET(self):
        return {'sectors': list_sectors(self.context)}

    def do_POST(self):
        if not self.has_permission('Euphorie: Manage country'):
            raise Unauthorized()

        sector = createContent('euphorie.sector')
        # Assign a temporary id. Without this security caching logic breaks due to use of
        # getPhysicalPath() as cache id. This calls getId() to get the id,
        # which uses __name__ if no id is set, but __name__ is a computer attribute which
        # calls getId. BOOM!
        sector.id = str(id(sector))
        try:
            self.update_object(self.attributes, ISector,
                    sector.__of__(self.context))
        except ValueError as e:
            return {'type': 'error',
                    'message': str(e)}
        del sector.id
        sector = addContentToContainer(self.context.country, sector, False)
        view = SectorView(sector, self.request)
        return view.do_GET()
