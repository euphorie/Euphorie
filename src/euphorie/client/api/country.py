from five import grok
from euphorie.client.api import JsonView
from euphorie.client.country import IClientCountry
from euphorie.client.sector import IClientSector
from euphorie.client.api.sector import View as SectorView


class View(JsonView):
    grok.context(IClientCountry)
    grok.name('index_html')
    grok.require('zope2.Public')

    def do_GET(self):
        info = {'id': self.context.id,
                'title': self.context.title,
                'type': self.context.country_type,
                }
        sectors = [sector for sector in self.context.values()
                   if IClientSector.providedBy(sector)]
        if 'details' in self.request.form:
            info['sectors'] = [SectorView(sector, self.request).do_GET()
                               for sector in sectors]
        else:
            info['sectors'] = [{'id': sector.id,
                                'title': sector.title}
                               for sector in sectors]
        return info
