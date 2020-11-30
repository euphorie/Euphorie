# coding=utf-8
from ..module import IModule
from ..risk import IRisk
from ..utils import DragDropHelper
from euphorie.content import MessageFactory as _
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.interfaces import IDexterityFTI
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getMultiAdapter
from zope.component import getUtility


class ModuleView(BrowserView, DragDropHelper):
    """View name: @@nuplone-view"""

    def _morph(self, child):
        state = getMultiAdapter((child, self.request), name="plone_context_state")
        return {"id": child.id, "title": child.title, "url": state.view_url()}

    @property
    def modules(self):
        """List modules in current context"""
        return [
            self._morph(child)
            for child in self.context.values()
            if IModule.providedBy(child)
        ]

    @property
    def risks(self):
        """List risks in current context"""
        return [
            self._morph(child)
            for child in self.context.values()
            if IRisk.providedBy(child)
        ]

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
        return _(u"Add %s" % type_name)


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    """Override for the standard edit form so we can change the form title
    for submodules.

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
        return _(u"Edit ${name}", mapping={"name": type_name})

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets["title"].addClass("span-7")

    def extractData(self, setErrors=True):
        data = super(EditForm, self).extractData(setErrors)

        # If there is a validation error on the form, consume all status messages,
        # so that they don't appear in the form. We only want to show validation
        # messages directly on the respective field(s) in that case.
        if data[1]:
            status = IStatusMessage(self.request)
            status.show()
        return data
