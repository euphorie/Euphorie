# coding=utf-8
from ..sector import getSurveys
from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView


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
