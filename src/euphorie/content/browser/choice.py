from ..option import IOption
from ..utils import DragDropHelper
from plone.dexterity.browser.view import DefaultView


class ChoiceView(DefaultView, DragDropHelper):
    @property
    def options(self):
        return [
            {
                "id": option.id,
                "url": option.absolute_url(),
                "title": option.title,
            }
            for option in self.context.values()
            if IOption.providedBy(option)
        ]
