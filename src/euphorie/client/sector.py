"""
Sector
------

The client proxy for displaying sector information.
"""

from Acquisition import aq_base
from Acquisition import aq_parent
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
from zope.interface import implementer


class IClientSector(model.Schema, IBasic):
    """Sector information in the online client.

    This object proxies the title and logo from the main sector object.

    The online client is implemented as a cantainer with all available surveys.
    The default view for all survey elements inside this container is changed
    to the client user interface. This is done using a simple traversal
    adapter.
    """


@implementer(IClientSector)
class ClientSector(Container):
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
