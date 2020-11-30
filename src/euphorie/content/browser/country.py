# coding=utf-8
from Acquisition import aq_inner
from euphorie.content.countrymanager import ICountryManager
from euphorie.content.sector import ISector
from euphorie.content.utils import CUSTOM_COUNTRY_NAMES
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.memoize.instance import memoize
from Products.Five import BrowserView


class CountryView(BrowserView):
    @property
    def title(self):
        names = self.request.locale.displayNames.territories
        # Hook in potential custom country names
        names.update(CUSTOM_COUNTRY_NAMES)
        return names.get(self.context.id.upper(), self.context.title)

    @property
    def sectors(self):
        sectors_dict = [
            {"id": sector.id, "title": sector.title, "url": sector.absolute_url()}
            for sector in self.context.values()
            if ISector.providedBy(sector)
        ]
        try:
            sectors_dict.sort(key=lambda s: s["title"].lower())
        except UnicodeDecodeError:
            sectors_dict.sort(key=lambda s: s["title"].lower().decode("utf-8"))
        return sectors_dict


class AddForm(DefaultAddForm):
    portal_type = "euphorie.country"

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets["country_type"].mode = "hidden"


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets["country_type"].mode = "hidden"


class ManageUsers(BrowserView):
    @property
    @memoize
    def country(self):
        return aq_inner(self.context)

    @property
    def title(self):
        names = self.request.locale.displayNames.territories
        return names.get(self.country.id.upper(), self.country.title)

    @property
    def sectors(self):
        sectors_dict = [
            {
                "id": sector.id,
                "login": sector.login,
                "password": sector.password,
                "title": sector.title,
                "url": sector.absolute_url(),
                "locked": sector.locked,
            }
            for sector in self.country.values()
            if ISector.providedBy(sector)
        ]
        sectors_dict.sort(key=lambda s: s["title"].lower())
        return sectors_dict

    @property
    def managers(self):
        managers_dict = [
            {
                "id": manager.id,
                "login": manager.login,
                "title": manager.title,
                "url": manager.absolute_url(),
                "locked": manager.locked,
            }
            for manager in self.country.values()
            if ICountryManager.providedBy(manager)
        ]
        managers_dict.sort(key=lambda s: s["title"].lower())
        return managers_dict
