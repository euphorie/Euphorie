"""
Client
------

The view for the frontpage of the client site and some adapters to provide a
client user.
"""

from borg.localrole.interfaces import ILocalRoleProvider
from euphorie.client.interfaces import IClientSkinLayer
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.membrane.interfaces.user import IMembraneUserObject
from zope.component import adapter
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserSkinType
from ZPublisher.BaseRequest import DefaultPublishTraverse


class IClient(model.Schema, IBasic):
    """The online client.

    The online client is implemented as a container with all available
    surveys. The default view for all survey elements inside this
    container is changed to the client user interface. This is done
    using a simple traversal adapter.
    """


@implementer(IClient)
class Client(Container):
    exclude_from_nav = True


@adapter(IClient)
@implementer(IMembraneUserObject)
class ClientUserProvider:
    """Expose the client as a user to the system.

    This is used as ownership for all client data.
    """

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        return self.context.id

    def getUserName(self):
        return self.context.id


@adapter(IClient)
@implementer(ILocalRoleProvider)
class ClientLocalRolesProvider:
    """`borg.localrole` provider for :obj:`IClient` instances.

    This local role provider gives the client user itself the
    `CountryManager` local role. This allows publication of surveys
    inside the client since the publication machinery always runs under
    the client user.
    """

    def __init__(self, client):
        self.context = client

    def getRoles(self, principal_id):
        if principal_id == self.context.getId():
            return ("CountryManager",)
        return ()

    def getAllRoles(self):
        return [(self.context.getId(), ("CountryManager",))]


@adapter(IClient, Interface)
class ClientPublishTraverser(DefaultPublishTraverse):
    """Publish traverser to setup the skin layer.

    This traverser marks the request with IClientSkinLayer. We can not
    use BeforeTraverseEvent since in Zope 2 that is only fired for site
    objects.
    """

    skin_layer = IClientSkinLayer

    def publishTraverse(self, request, name):
        from euphorie.client.utils import setRequest

        setRequest(request)
        request.client = self.context  # XXX: remove me

        ifaces = [
            iface
            for iface in directlyProvidedBy(request)
            if not IBrowserSkinType.providedBy(iface)
        ]
        directlyProvides(request, self.skin_layer, ifaces)
        return super().publishTraverse(request, name)
