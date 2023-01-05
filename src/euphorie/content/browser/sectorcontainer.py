from Acquisition import aq_inner
from euphorie.content.utils import summarizeCountries
from Products.Five import BrowserView


class SectorContainerView(BrowserView):
    @property
    def countries(self):
        return summarizeCountries(aq_inner(self.context), self.request)
