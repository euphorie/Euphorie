from zExceptions import Unauthorized
from Acquisition import aq_base
from five import grok
from euphorie.ghost import PathGhost
from plone.dexterity.utils import createContent
from plone.dexterity.utils import addContentToContainer
from euphorie.json import get_json_unicode
from ..countrymanager import ICountryManager
from .countrymanager import View as CountryManagerView
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

    attributes = CountryManagerView.attributes + [
            ('login', 'login', get_json_unicode),
            ]

    def do_GET(self):
        return {'managers': list_managers(self.context)}

    def do_POST(self):
        if not self.has_permission('Euphorie: Manage country'):
            raise Unauthorized()

        manager = createContent('euphorie.countrymanager')
        # Assign a temporary id. Without this security caching logic breaks due to use of
        # getPhysicalPath() as cache id. This calls getId() to get the id,
        # which uses __name__ if no id is set, but __name__ is a computer attribute which
        # calls getId. BOOM!
        manager.id = str(id(manager))
        try:
            self.update_object(self.attributes, ICountryManager,
                    manager.__of__(self.context))
        except ValueError as e:
            return {'type': 'error',
                    'message': str(e)}
        del manager.id
        manager = addContentToContainer(self.context.country, manager, False)
        view = CountryManagerView(manager, self.request)
        return view.do_GET()
