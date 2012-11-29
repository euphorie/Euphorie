from five import grok
from ..country import ICountry
from ..countrymanager import ICountryManager
from ..sector import ISector
from . import JsonView


def country_info(country):
    return {'id': country.id,
            'title': country.title,
            'country-type': country.country_type,
           }


class View(JsonView):
    grok.context(ICountry)
    grok.require('zope2.View')
    grok.name('index_html')

    def list_managers(self):
        return [{'id': manager.id,
                 'title': manager.title,
                 'login': manager.login,
                 'email': manager.contact_email,
                 'locked': manager.locked,
                } for manager in self.context.values()
                if ICountryManager.providedBy(manager)]

    def list_sectors(self):
        return [{'id': sector.id,
                 'title': sector.title,
                 'login': sector.login,
                 'locked': sector.locked,
                } for sector in self.context.values()
                if ISector.providedBy(sector)]

    def do_GET(self):
        info = country_info(self.context)
        info['type'] = 'country'
        if 'details' in self.request.form:
            info['managers'] = self.list_managers()
            info['sectors'] = self.list_sectors()
        return info
