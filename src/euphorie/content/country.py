"""
Country
-------

Is the container for sectors of that country, plus the country manager user
accounts.

https://admin.oiraproject.eu/sectors/eu
"""
from .. import MessageFactory as _
from Acquisition import aq_inner
from euphorie.content.sector import ISector
from euphorie.content.utils import CUSTOM_COUNTRY_NAMES
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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

    form.widget(risk_default_collapsible_sections=CheckBoxFieldWidget)
    risk_default_collapsible_sections = schema.List(
        title=_(
            "label__risk_default_collapsible_sections",
            u"Open sections on risk page"
        ),
        description=_(
            "help__risk_default_collapsible_sections",
            u"Define, which information sections should be open by "
            u"default on a risk identification page. Sections not checked "
            u"will be shown intially in collapsed mode, but the user can always "
            u"open those sections with a click."
        ),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"collapsible_section_information", title=_(u"Information")),
                SimpleTerm(u"collapsible_section_resources", title=_(u"Resources: Legal references and attachments")),
                SimpleTerm(u"collapsible_section_comments", title=_(u"Comments")),
            ])
        ),
        default=["collapsible_section_information"],
        required=False,
    )

    form.widget(default_reports=CheckBoxFieldWidget)
    default_reports = schema.List(
        title=_(
            "label__default_reports",
            u"Available reports"
        ),
        description=_(
            "help__default_reports",
            u"Define, which reports are offered to the user on the Report page."
        ),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary([
                SimpleTerm(u"report_full", title=_(u"Full report (Word document)")),
                SimpleTerm(u"report_action_plan", title=_(u"Action plan (Excel spreadsheet)")),
                SimpleTerm(u"report_overview_risks", title=_(u"Overview of risks (PDF)")),
                SimpleTerm(u"report_overview_measures", title=_(u"Overview of measures (PDF)")),
            ])
        ),
        default=["report_full", "report_action_plan", "report_overview_risks"],
        required=False,
    )


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
