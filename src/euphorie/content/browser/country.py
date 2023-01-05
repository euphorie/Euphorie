from Acquisition import aq_inner
from euphorie.content.countrymanager import ICountryManager
from euphorie.content.sector import getSurveys
from euphorie.content.sector import ISector
from euphorie.content.utils import CUSTOM_COUNTRY_NAMES
from io import StringIO
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.memoize.instance import memoize
from Products.Five import BrowserView

import csv
import datetime


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
        super().updateWidgets()
        self.widgets["country_type"].mode = "hidden"


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    def updateWidgets(self):
        super().updateWidgets()
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


class Tools(CountryView):
    @memoize
    def get_tools(self, sector_id):
        sector = self.context.get(sector_id)
        return getSurveys(sector)

    def download_csv(self):
        fieldnames = [
            "Sector",
            "Tool Title",
            "Version Title",
            "URL",
            "published",
            "obsolete",
        ]
        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()
        for sector in self.sectors:
            for group in self.get_tools(sector["id"]):
                for survey in group["surveys"]:
                    writer.writerow(
                        {
                            "Sector": sector["title"],
                            "Tool Title": group["title"],
                            "Version Title": survey["title"],
                            "URL": survey["url"],
                            "published": "published" if survey["published"] else "",
                            "obsolete": "obsolete" if group["obsolete"] else "",
                        }
                    )
        csv_data = buffer.getvalue()
        buffer.close()
        response = self.request.RESPONSE
        today_iso = datetime.date.today().isoformat()
        response.setHeader(
            "Content-Disposition",
            f"attachment; filename=oira_tools_{self.context.id}_{today_iso}.csv",
        )
        response.setHeader("Content-Type", "text/csv;charset=utf-8")
        return csv_data
