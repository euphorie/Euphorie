# coding=utf-8
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm
from Products.Five import BrowserView

import markdown


class SolutionView(BrowserView):
    def render_md(self, text):
        return markdown.markdown(text)


class AddForm(DefaultAddForm):

    portal_type = "euphorie.solution"

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets["action_plan"].mode = "hidden"
        self.widgets["prevention_plan"].mode = "hidden"
        self.widgets["action"].rows = 15


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        self.widgets["action_plan"].mode = "hidden"
        self.widgets["prevention_plan"].mode = "hidden"
        self.widgets["action"].rows = 15
