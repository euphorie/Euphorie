# coding=utf-8
from ..library import get_library
from Acquisition import aq_inner
from euphorie.content.module import item_depth
from Products.Five import BrowserView
from zExceptions import NotFound


class Library(BrowserView):
    def __call__(self):
        """ Set view attributes to define the current library, depth and
        at_root, which is True when the context is the root of the library.
        """
        self.library = get_library(self.context)
        if not self.library:
            raise NotFound(self, "library", self.request)
        self.depth = item_depth(aq_inner(self.context))
        self.at_root = not self.depth
        return super(Library, self).__call__()
