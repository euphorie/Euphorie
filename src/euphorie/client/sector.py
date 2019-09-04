"""
Sector
------

The client proxy for displaying sector information.
"""

from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client.interfaces import IClientSkinLayer
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements


class IClientSector(form.Schema, IBasic):
    """Sector information in the online client.

    This object proxies the title and logo from the main sector object.

    The online client is implemented as a cantainer with all available surveys.
    The default view for all survey elements inside this container is changed
    to the client user interface. This is done using a simple traversal
    adapter.
    """


class ClientSector(dexterity.Container):
    implements(IClientSector)

    def _sector(self):
        sectors = getUtility(ISiteRoot).sectors
        country = getattr(sectors, aq_parent(self).id)
        return getattr(country, self.id)

    def Title(self):
        title = getattr(aq_base(self), "title", None)
        if title is not None:
            return title
        else:
            return self._sector().title


grok.templatedir("templates")


class View(grok.View):
    grok.context(IClientSector)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)

    def render(self):
        self.request.response.redirect(
                aq_parent(aq_inner(self.context)).absolute_url())
