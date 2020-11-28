# coding=utf-8
from ..sector import getSurveys
from ..sector import ISector
from Acquisition import aq_inner
from plone import api
from plone.dexterity.browser.edit import DefaultEditForm
from Products.Five import BrowserView

import logging


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
    formErrorsMessage = u"Please correct the indicated errors."

    def extractData(self):
        self.fields = self.fields.omit("title", "login")
        if "title" in self.widgets:
            del self.widgets["title"]
        if "login" in self.widgets:
            del self.widgets["login"]
        return super(EditForm, self).extractData()


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
