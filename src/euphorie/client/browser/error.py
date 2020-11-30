# coding=utf-8
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Five import BrowserView

import logging


log = logging.getLogger(__name__)


class ErrorView(BrowserView):
    def __call__(self):
        self.exception = aq_inner(self.context)
        self.context = aq_parent(self)
        log.exception("Error at %r", self.context)
        return self.index()


class NotFound(ErrorView):

    pass
