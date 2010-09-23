from Acquisition import aq_inner
from zope.interface import implements
from five import grok
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content.country import ICountry
from plonetheme.nuplone.skin.interfaces import NuPloneSkin

grok.templatedir("templates")


class ISectorContainer(form.Schema, IRichDescription, IBasic):
    """Container for all sectors."""



class SectorContainer(dexterity.Container):
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
        container=aq_inner(self.context)
        names=self.request.locale.displayNames.territories
        countries=[dict(id=country.id,
                        title=names.get(country.id.upper(), country.title),
                        url=country.absolute_url())
                   for country in container.values()
                   if ICountry.providedBy(country)]
        countries.sort(key=lambda c: c["title"])
        self.countries=countries


