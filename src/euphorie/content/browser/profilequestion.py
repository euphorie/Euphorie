# coding=utf-8
from ..module import IModule
from ..risk import IRisk
from euphorie.content import MessageFactory as _
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.memoize.instance import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class ProfileQuestionView(BrowserView):
    """View name: @@nuplone-view"""

    def _morph(self, child):
        state = getMultiAdapter((child, self.request), name="plone_context_state")
        return {"id": child.id, "title": child.title, "url": state.view_url()}

    @property
    def risks(self):
        """List risks in current context"""
        return [
            self._morph(child)
            for child in self.context.values()
            if IRisk.providedBy(child)
        ]

    @property
    def modules(self):
        """List modules in current context"""
        return [
            self._morph(child)
            for child in self.context.values()
            if IModule.providedBy(child)
        ]

    @property
    @memoize
    def portal_transforms(self):
        return api.portal.get_tool("portal_transforms")

    def get_safe_html(self, text):
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()


class AddForm(DefaultAddForm):
    """View name: euphorie.profilequestion"""

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
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        for fname in ("description",):
            value = self.widgets[fname].value or ""
            safe_value = self.get_safe_html(value)
            if value != safe_value:
                self.widgets[fname].value = safe_value
