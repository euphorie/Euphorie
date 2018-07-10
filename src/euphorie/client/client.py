"""
Client
------

The view for the frontpage of the client site and some adapters to provide a
client user.
"""

from borg.localrole.interfaces import ILocalRoleProvider
from euphorie.client.api.entry import access_api
from euphorie.client.interfaces import IClientSkinLayer
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from Products.membrane.interfaces.user import IMembraneUserObject
from zope.component import adapts
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from zope.interface import implements
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserSkinType
from ZPublisher.BaseRequest import DefaultPublishTraverse


class IClient(form.Schema, IBasic):
    """The online client.

    The online client is implemented as a container with all available surveys.
    The default view for all survey elements inside this container is changed
    to the client user interface. This is done using a simple traversal
    adapter.
    """


class Client(dexterity.Container):
    implements(IClient)

    exclude_from_nav = True


class ClientUserProvider(grok.Adapter):
    """Expose the client as a user to the system.

    This is used as ownership for all client data.
    """
    grok.context(IClient)
    grok.implements(IMembraneUserObject)

    def getUserId(self):
        return self.context.id

    def getUserName(self):
        return self.context.id


class ClientLocalRolesProvider(grok.Adapter):
    """`borg.localrole` provider for :obj:`IClient` instances.

    This local role provider gives the client user itself the
    `CountryManager` local role. This allows publication of surveys
    inside the client since the publication machinery always
    runs under the client user.
    """
    grok.context(IClient)
    grok.implements(ILocalRoleProvider)

    def __init__(self, client):
        self.context = client

    def getRoles(self, principal_id):
        if principal_id == self.context.getId():
            return ("CountryManager",)
        return ()

    def getAllRoles(self):
        return [(self.context.getId(), ("CountryManager",))]


class ClientPublishTraverser(DefaultPublishTraverse):
    """Publish traverser to setup the skin layer.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent since in Zope 2 that is only fired for site objects.
    """
    adapts(IClient, Interface)

    def publishTraverse(self, request, name):
        from euphorie.client.utils import setRequest
        setRequest(request)
        request.client = self.context

        if name == 'api':
            return access_api(request).__of__(self.context)

        ifaces = [iface for iface in directlyProvidedBy(request)
                if not IBrowserSkinType.providedBy(iface)]
        directlyProvides(request, IClientSkinLayer, ifaces)
        return super(ClientPublishTraverser, self)\
                .publishTraverse(request, name)
