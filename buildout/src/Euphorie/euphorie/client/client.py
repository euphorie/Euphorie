from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from ZPublisher.BaseRequest import DefaultPublishTraverse
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from borg.localrole.interfaces import ILocalRoleProvider
from euphorie.client.interfaces import IClientSkinLayer

class IClient(form.Schema, IBasic):
    """The online client.

    The online client is implemented as a cantainer with all available surveys.
    The default view for all survey elements inside this container is changed
    to the client user interface. This is done using a simple traversal adapter.
    """

class Client(dexterity.Container):
    implements(IClient)

grok.templatedir("templates")


class View(grok.View):
    grok.context(IClient)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("frontpage")




class ClientUserProvider(object):
    """Expose the client as a user to the system.

    This is used as ownership for all client data.
    """
    adapts(IClient)

    def __init__(self, client):
        self.client=client

    def getUserId(self):
        return self.client.id

    def getUserName(self):
        return self.client.id


class ClientLocalRolesProvider(object):
    """`borg.localrole` provider for :obj:`IClient` instances.

    This local role provider gives the client user itself the
    `Support` local role. This allows publication of surveys
    inside the client since the publication machinery always
    runs under the client user.
    """
    adapts(IClient)
    implements(ILocalRoleProvider)

    def __init__(self, client):
        self.client=client

    def getRoles(self, principal_id):
        if principal_id==self.client.getId():
            return ("Support",)
        return ()

    def getAllRoles(self):
        return [(self.client.getId(), ("Support",))]



class ClientPublishTraverser(DefaultPublishTraverse):
    """Publish traverser to setup the skin layer.

    This traverser marks the request with IClientSkinLayer. We can not use
    BeforeTraverseEvent sine in Zope 2 that is only fired for site objects.
    """
    adapts(IClient, Interface)

    def publishTraverse(self, request, name):
        from euphorie.client.utils import setRequest
        setRequest(request)
        request.client=self.context
        directlyProvides(request, IClientSkinLayer, *directlyProvidedBy(request))
        return super(ClientPublishTraverser, self).publishTraverse(request, name)

