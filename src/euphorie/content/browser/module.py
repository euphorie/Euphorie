from ..utils import DragDropHelper
from .survey import SurveyBase
from euphorie.content import MessageFactory as _
from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize.instance import memoize
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getUtility


class ModuleView(SurveyBase, DragDropHelper):
    """View name: @@nuplone-view."""

    @property
    def portal_type(self):
        if self.context.aq_parent.portal_type == "euphorie.module":
            return _("Submodule")
        else:
            portal_type = self.context.portal_type
            fti = getUtility(IDexterityFTI, name=portal_type)
            return fti.Title()


class AddForm(DefaultAddForm):
    portal_type = "euphorie.module"

    @property
    def label(self):
        if self.context.portal_type == "euphorie.module":
            type_name = _("Submodule")
        else:
            portal_type = self.portal_type
            fti = getUtility(IDexterityFTI, name=portal_type)
            type_name = fti.Title()
        return _("Add %s" % type_name)


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    """Override for the standard edit form so we can change the form title for
    submodules.

    View name: @@edit
    """

    @property
    def label(self):
        if self.context.aq_parent.portal_type == "euphorie.module":
            type_name = _("Submodule")
        else:
            portal_type = self.context.portal_type
            fti = getUtility(IDexterityFTI, name=portal_type)
            type_name = fti.Title()
        return _("Edit ${name}", mapping={"name": type_name})

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
        self.widgets["title"].addClass("span-7")
        for fname in ("description", "solution_direction"):
            value = self.widgets[fname].value or ""
            safe_value = self.get_safe_html(value)
            if value != safe_value:
                self.widgets[fname].value = safe_value

    def extractData(self, setErrors=True):
        data = super().extractData(setErrors)

        # If there is a validation error on the form, consume all status messages,
        # so that they don't appear in the form. We only want to show validation
        # messages directly on the respective field(s) in that case.
        if data[1]:
            status = IStatusMessage(self.request)
            status.show()
        return data
