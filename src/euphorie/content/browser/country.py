# coding=utf-8

from euphorie.content.sector import ISector
from euphorie.content.utils import CUSTOM_COUNTRY_NAMES
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
