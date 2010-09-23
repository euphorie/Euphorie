from plone.tiles import Tile
from plonetheme.nuplone.utils import getFactoriesInContext
from plonetheme.nuplone.utils import checkPermission


class AddBarTile(Tile):
    def update(self):
        self.actions=getFactoriesInContext(self.context)
        self.actions.sort(key=lambda x: x.title)
        self.can_edit=checkPermission(self.context, "Modify portal content")

    def __call__(self):
        self.update()
        if not (self.actions or self.can_edit):
            return u""
        return self.index()

