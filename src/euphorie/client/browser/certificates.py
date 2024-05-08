from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView


class View(BrowserView):
    """Certificates Overview Page"""

    @property
    @memoize
    def trainings_portlet(self):
        return api.content.get_view(
            name="portlet-my-trainings", context=self.context, request=self.request
        )

    @property
    @memoize
    def my_certificates(self):
        certificates = {}
        for training in self.trainings_portlet.my_certificates:
            year = training.time.year
            link = f"{training.session.absolute_url()}/@@training-certificate-view"
            content = self.trainings_portlet.get_certificate(training.session)
            certificates.setdefault(year, []).append({"link": link, "content": content})
        return certificates.items()
