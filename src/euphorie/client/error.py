from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.client.interfaces import IClientSkinLayer
from five import grok

import logging
import zExceptions


log = logging.getLogger(__name__)

grok.templatedir("templates")


class ErrorView(grok.View):
    grok.context(Exception)
    grok.layer(IClientSkinLayer)
    grok.name("index.html")
    grok.template("error")

    def update(self):
        self.exception = aq_inner(self.context)
        self.context = aq_parent(self)
        log.exception("Error at %r", self.context)


class NotFound(ErrorView):
    grok.context(zExceptions.NotFound)
    grok.template("error_notfound")
