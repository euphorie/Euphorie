from Acquisition import aq_inner
from euphorie.client import CONDITIONS_VERSION
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import get_current_account
from five import grok
from z3c.appconfig.interfaces import IAppConfig
from z3c.appconfig.utils import asBool
from zope.component import getUtility
from zope.interface import Interface

import logging


log = logging.getLogger(__name__)

grok.templatedir("templates")


def checkTermsAndConditions():
    appconfig = getUtility(IAppConfig)
    try:
        return asBool(appconfig["euphorie"]["terms-and-conditions"])
    except KeyError:
        return True
    except ValueError:
        log.error("Invalid value for terms-and-conditions flag "
                  "in site configuration.")
        return False


def approvedTermsAndConditions(account=None):
    if account is None:
        account = get_current_account()
    return account.tc_approved is not None and \
            account.tc_approved == CONDITIONS_VERSION


class TermsAndConditions(grok.View):
    grok.name("terms-and-conditions")
    grok.context(Interface)
    grok.require("zope2.Public")
    grok.layer(IClientSkinLayer)
    grok.template("conditions")

    def terms_changed(self):
        return getattr(self.account, 'tc_approved', None) is not None

    def update(self):
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
                self.request.response.redirect(
                        aq_inner(self.context).absolute_url())
