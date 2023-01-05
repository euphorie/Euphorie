from ..sector import getSurveys
from ..sector import ISector
from Acquisition import aq_inner
from euphorie.content import MessageFactory as _
from plone import api
from plone.dexterity.browser.edit import DefaultEditForm
from plonetheme.nuplone.skin import actions
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.utils import getPortal
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

import logging
import zExceptions


log = logging.getLogger(__name__)


class SectorView(BrowserView):
    @property
    def add_survey_url(self):
        return "{url}/++add++euphorie.surveygroup".format(
            url=aq_inner(self.context).absolute_url()
        )

    @property
    def surveys(self):
        return getSurveys(self.context)

    @property
    def can_add(self):
        permission = "Euphorie: Add new RIE Content"
        user = api.user.get_current()
        return api.user.has_permission(permission, user=user, obj=self.context)


class EditForm(DefaultEditForm):
    schema = ISector
    default_fieldset_label = None
    formErrorsMessage = "Please correct the indicated errors."

    def extractData(self):
        self.fields = self.fields.omit("title", "login")
        if "title" in self.widgets:
            del self.widgets["title"]
        if "login" in self.widgets:
            del self.widgets["login"]
        return super().extractData()


class VersionCommand(BrowserView):
    def __call__(self):
        action = self.request.get("action")
        if action == "new":
            sector = aq_inner(self.context)
            self.request.response.redirect(
                "%s/++add++euphorie.surveygroup" % sector.absolute_url()
            )
        else:
            log.error("Invalid version command action: %r", action)


class Delete(actions.Delete):
    """Only delete the sector if it doesn't have any published surveys."""

    def verify(self, container, context):
        if not checkPermission(container, "Delete objects"):
            raise zExceptions.Unauthorized

        flash = IStatusMessage(self.request).addStatusMessage
        sector = context
        country = container
        client = getPortal(container).client

        if country.id not in client:
            return True

        cl_country = client[country.id]
        if sector.id not in cl_country:
            return True

        # Look for any published surveys in the client sector, and prevent
        # deletion if any are found
        cl_sector = cl_country[sector.id]
        surveys = [s for s in cl_sector.values() if s.id != "preview"]
        if surveys:
            flash(
                _(
                    "message_not_delete_published_sector",
                    default="You can not delete a sector that contains published "
                    "OiRA Tools.",
                ),
                "error",
            )
            self.request.response.redirect(context.absolute_url())
            return False
        return True
