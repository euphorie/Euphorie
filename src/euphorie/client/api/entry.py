import pkg_resources
from five import grok
from zope.interface import directlyProvides
from euphorie.ghost import PathGhost
from . import JsonView
from .interfaces import IClientAPISkinLayer
from .users import Users
from .surveys import Surveys


class API(PathGhost):
    """Entry point for API access.

    This API object acts as a demarcation-point: its only purpose is
    to setup interfaces on the request.
    """

    entry_points = {
            'surveys': Surveys,
            'users': Users,
            }

    def __getitem__(self, key):
        return self.entry_points[key](key, self.request).__of__(self)


class View(JsonView):
    grok.context(API)
    grok.require('zope2.Public')
    grok.name('index_html')

    def do_GET(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        euphorie = pkg_resources.get_distribution('Euphorie')
        return {'api-version': [1, 0],
                'euphorie-version': euphorie.version}


def access_api(request):
    """Utility method to create an API instance.

    :param request: request object
    :rtype: :py:class:`API` instance

    This function is intended to be used in a traversal hook (specifically
    :py:class:`ClientPublishTraverser
    <euphorie.client.client.ClientPublishTraverser>`). It will configure the
    request for API access and return an :py:class:`API` instance.
    """
    # Inform the publisher that we will never see WebDAV clients. This
    # makes sure that we get acquisition during traversal even for
    # request methods other than GET and POST.
    request.maybe_webdav_client = False
    directlyProvides(request, IClientAPISkinLayer, [])
    return API('api', request)
