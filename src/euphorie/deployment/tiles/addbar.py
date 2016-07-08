from plone.tiles import Tile
from plonetheme.nuplone.utils import getFactoriesInContext
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.utils import FactoryInfo
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.module import IModule
from euphorie.content import MessageFactory as _


class AddBarTile(Tile):
    def update(self):
        actions = getFactoriesInContext(self.context)
        if IModule.providedBy(self.context):
            for (i, action) in enumerate(actions):
                # To be able to determine what button label to display, we
                # explicitly set the action.id to the fake "euphorie.submodule"
                if action.id == "euphorie.module":
                    actions[i] = FactoryInfo("euphorie.submodule",
                            _(u"Submodule"), *action[2:])
                    break
        self.actions = sorted(actions, key=lambda x: x.title)
        self.can_edit = checkPermission(self.context, "Modify portal content")
        self.library_available = IQuestionContainer.providedBy(self.context)

    def __call__(self):
        self.update()
        if not (self.actions or self.can_edit):
            return u""
        return self.index()
