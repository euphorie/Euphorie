from plone.tiles import Tile
from plonetheme.nuplone.utils import viewType


class SearchTile(Tile):

    def __call__(self):
        view_type = viewType(self.context, self.request)
        if view_type in ["add", "edit"]:
            return None

        self.did_search = self.request.method == 'POST'

        return self.index()
