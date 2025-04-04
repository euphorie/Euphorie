from ..option import IOption
from ..utils import DragDropHelper
from Acquisition import aq_inner
from plone.dexterity.browser.view import DefaultView
from plone.memoize.instance import memoize
from Products.Five import BrowserView


class ChoiceView(DefaultView, DragDropHelper):
    @property
    @memoize
    def my_context(self):
        return aq_inner(self.context)

    @property
    def options(self):
        return [
            {
                "id": option.id,
                "url": option.absolute_url(),
                "title": option.title,
            }
            for option in self.my_context.values()
            if IOption.providedBy(option)
        ]
