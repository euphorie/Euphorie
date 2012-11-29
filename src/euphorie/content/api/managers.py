from Acquisition import aq_base
from five import grok
from euphorie.ghost import PathGhost
from ..countrymanager import ICountryManager
from . import JsonView


def list_managers(country):
    return [{'id': manager.id,
             'title': manager.title,
             'login': manager.login,
             'email': manager.contact_email,
             'locked': manager.locked,
            } for manager in country.values()
            if ICountryManager.providedBy(manager)]


class Managers(PathGhost):
    def __init__(self, id, request, country):
        super(Managers, self).__init__(id, request)
        self.country = country

    def __getitem__(self, key):
        manager = self.country[key]
        if ICountryManager.providedBy(manager):
            return aq_base(manager).__of__(self)
        raise KeyError(key)


class View(JsonView):
    grok.context(Managers)
    grok.require('zope2.View')
    grok.name('index_html')

    def do_GET(self):
        return {'managers': list_managers(self.context)}
