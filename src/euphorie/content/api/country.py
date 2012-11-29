from five import grok
from Acquisition.interfaces import IAcquirer
from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserPublisher
from ..country import ICountry
from ..sector import ISector
from .interfaces import ICMSAPISkinLayer
from .managers import list_managers
from .managers import Managers
from .sectors import list_sectors
from .sectors import Sectors
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
            info['managers'] = list_managers(self.context)
            info['sectors'] = list_sectors(self.context)
        return info


class CountryTraverse(object):
    adapts(ICountry, ICMSAPISkinLayer)
    implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if name == 'managers':
            return Managers('managers', request, self.context)\
                    .__of__(self.context)
        elif name == 'sectors':
            return Sectors('sectors', request, self.context)\
                    .__of__(self.context)
        view = queryMultiAdapter((self.context, request), Interface, name)
        if view is not None:
            if IAcquirer.providedBy(view):
                view = view.__of__(self.context)
            return view
        raise KeyError(name)
