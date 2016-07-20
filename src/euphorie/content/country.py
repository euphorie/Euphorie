"""
Country
-------

Is the container for sectors of that country, plus the country manager user
accounts.

https://admin.oiraproject.eu/sectors/eu
"""
from Acquisition import aq_inner
from zope.interface import implements
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from euphorie.content.sector import ISector
from euphorie.content.utils import CUSTOM_COUNTRY_NAMES
from .. import MessageFactory as _

grok.templatedir("templates")


class ICountry(form.Schema, IBasic):
    """Country grouping in the online client.
    """

    country_type = schema.Choice(
            title=_("Country grouping"),
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"region", title=_("Region")),
                SimpleTerm(u"eu-member", title=_(u"EU member state")),
                SimpleTerm(u"efta", title=_(u"EFTA country")),
                SimpleTerm(u"candidate-eu", title=_(u"Candidate country")),
                SimpleTerm(u"potential-candidate-eu",
                    title=_(u"Potential candidate country")),
                ]),
            required=True)


class Country(dexterity.Container):
    """A country folder."""
    implements(ICountry)

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False


class View(grok.View):
    grok.context(ICountry)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("country_view")
    grok.name("nuplone-view")

    def update(self):
        super(View, self).update()
        names = self.request.locale.displayNames.territories
        # Hook in potential custom country names
        names.update(CUSTOM_COUNTRY_NAMES)
        self.title = names.get(self.context.id.upper(), self.context.title)
        self.sectors = [{'id': sector.id,
                         'title': sector.title,
                         'url': sector.absolute_url()}
                         for sector in self.context.values()
                         if ISector.providedBy(sector)]
        try:
            self.sectors.sort(key=lambda s: s["title"].lower())
        except UnicodeDecodeError:
            self.sectors.sort(key=lambda s: s["title"].lower().decode('utf-8'))


class ManageUsers(grok.View):
    grok.context(ICountry)
    grok.require("euphorie.content.ManageCountry")
    grok.layer(NuPloneSkin)
    grok.template("user_mgmt")
    grok.name("manage-users")

    def update(self):
        from euphorie.content.countrymanager import ICountryManager
        super(ManageUsers, self).update()
        names = self.request.locale.displayNames.territories
        country = aq_inner(self.context)
        self.title = names.get(country.id.upper(), country.title)
        self.sectors = [{'id': sector.id,
                         'login': sector.login,
                         'password': sector.password,
                         'title': sector.title,
                         'url': sector.absolute_url(),
                         'locked': sector.locked}
                        for sector in country.values()
                        if ISector.providedBy(sector)]
        self.sectors.sort(key=lambda s: s["title"].lower())

        self.managers = [{'id': manager.id,
                          'login': manager.login,
                          'title': manager.title,
                          'url': manager.absolute_url(),
                          'locked': manager.locked}
                         for manager in country.values()
                         if ICountryManager.providedBy(manager)]
        self.managers.sort(key=lambda s: s["title"].lower())
