from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five import BrowserView


class SectorView(BrowserView):
    def __call__(self):
        self.request.response.redirect(aq_parent(aq_inner(self.context)).absolute_url())
