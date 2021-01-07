"""
Sector Container
----------------

A Sector Container provides the overview of all countries.

https://admin.oiraproject.eu/sectors
"""
from Acquisition import aq_inner
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content.utils import summarizeCountries
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.directives import form
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from zope.interface import implements


grok.templatedir("templates")


class ISectorContainer(form.Schema, IRichDescription, IBasic):
    """Container for all sectors."""


class SectorContainer(Container):
    implements(ISectorContainer)

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False


class View(grok.View):
    grok.context(ISectorContainer)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("sectorcontainer_view")
    grok.name("nuplone-view")

    def update(self):
        self.countries = summarizeCountries(aq_inner(self.context), self.request)
