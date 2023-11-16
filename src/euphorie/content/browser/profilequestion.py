from .survey import SurveyBase
from euphorie.content import MessageFactory as _
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ProfileQuestionView(SurveyBase):
    """View name: @@nuplone-view."""


class AddForm(DefaultAddForm):
    """View name: euphorie.profilequestion."""

    template = ViewPageTemplateFile("templates/profilequestion_add.pt")

    @property
    def label(self):
        return _("Add Profile question")


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    template = ViewPageTemplateFile("templates/profilequestion_edit.pt")

    @property
    def label(self):
        return _("Edit Profile question")

    @property
    @memoize
    def portal_transforms(self):
        return api.portal.get_tool("portal_transforms")

    def get_safe_html(self, text):
        if not text:
            return ""
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()

    def updateWidgets(self):
        super().updateWidgets()
        for fname in ("description",):
            value = self.widgets[fname].value or ""
            safe_value = self.get_safe_html(value)
            if value != safe_value:
                self.widgets[fname].value = safe_value
