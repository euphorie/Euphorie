from plone import api
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from Products.Five import BrowserView

import markdown


class SolutionView(BrowserView):
    def render_md(self, text):
        md_text = markdown.markdown(text)
        transforms = api.portal.get_tool("portal_transforms")
        data = transforms.convertTo("text/x-html-safe", md_text, mimetype="text/html")
        return data.getData()


class AddForm(DefaultAddForm):
    portal_type = "euphorie.solution"

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["action_plan"].mode = "hidden"
        self.widgets["prevention_plan"].mode = "hidden"
        self.widgets["action"].rows = 15


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["action_plan"].mode = "hidden"
        self.widgets["prevention_plan"].mode = "hidden"
        self.widgets["action"].rows = 15
