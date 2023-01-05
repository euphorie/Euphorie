from Acquisition import aq_inner
from euphorie.client import CONDITIONS_VERSION
from euphorie.client.model import get_current_account
from plone import api
from Products.Five import BrowserView

import logging


log = logging.getLogger(__name__)


def approvedTermsAndConditions(account=None):
    if account is None:
        account = get_current_account()
    return account.tc_approved is not None and account.tc_approved == CONDITIONS_VERSION


class TermsAndConditions(BrowserView):
    def terms_changed(self):
        return getattr(self.account, "tc_approved", None) is not None

    def __call__(self):
        webhelpers = api.content.get_view(
            name="webhelpers", context=self.context, request=self.request
        )
        self.came_from = webhelpers.get_came_from(
            default=aq_inner(self.context).absolute_url()
        )

        self.account = get_current_account()
        if self.request.environ["REQUEST_METHOD"] == "POST":
            self.account.tc_approved = CONDITIONS_VERSION

            self.request.response.redirect(self.came_from)
        return self.index()
