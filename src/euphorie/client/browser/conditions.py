# coding=utf-8
from Acquisition import aq_inner
from euphorie.client import CONDITIONS_VERSION
from euphorie.client.model import get_current_account
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
        self.came_from = self.request.form.get("came_from")
        if isinstance(self.came_from, list):
            # If came_from is both in the querystring and the form data
            self.came_from = self.came_from[0]

        self.account = get_current_account()
        if self.request.environ["REQUEST_METHOD"] == "POST":
            self.account.tc_approved = CONDITIONS_VERSION

            if self.came_from:
                self.request.response.redirect(self.came_from)
            else:
                self.request.response.redirect(aq_inner(self.context).absolute_url())
        return self.index()
