"""
Sector
------

The client proxy for displaying sector information.
"""

from Acquisition import aq_base
from Acquisition import aq_parent
from Acquisition import aq_inner
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface import implements
from five import grok
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from Products.CMFCore.interfaces import ISiteRoot
from euphorie.client.interfaces import IClientSkinLayer


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


class Style(grok.View):
    """View name: @@sector.css
    """
    grok.context(IClientSector)
    grok.require("zope2.View")
    grok.layer(IClientSkinLayer)
    grok.template("sector_style")
    grok.name("sector.css")

    def update(self):
        sector = aq_inner(self.context)
        images = getMultiAdapter((sector, self.request), name="images")
        self.logo = images.scale("logo", height=100, direction="up")

        main_background = getattr(sector, "main_background_colour", None)
        main_foreground = getattr(sector, "main_foreground_colour", None)
        support_background = getattr(sector, "support_background_colour", None)
        support_foreground = getattr(sector, "support_foreground_colour", None)
        if main_background and main_foreground and \
                support_background and support_foreground:
            self.colours = {'main_background': main_background,
                            'main_foreground': main_foreground,
                            'support_background': support_background,
                            'support_foreground': support_foreground}
        else:
            self.colours = None

        self.response.setHeader("Content-Type", "text/css")
