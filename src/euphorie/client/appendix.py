"""
Appendix
--------

The @@appendix and @@about views.
"""

import logging
from zExceptions import NotFound
from zope.interface import Interface
from zope.component import getUtility
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from euphorie.client.interfaces import IClientSkinLayer

log = logging.getLogger(__name__)

grok.templatedir("templates")


class About(grok.View):
    """View name: @@about
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("about")
    grok.template("about")


class AppendixView(grok.View):
    """View name: @@appendix
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("appendix")
    grok.template("appendix")

    document = None

    def _getLanguages(self):
        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        if "-" in lang:
            return [lang, lang.split("-")[0], "en"]
        else:
            return [lang, "en"]

    def publishTraverse(self, request, name):
        """Catch the appendix document the user wants to see. This uses
        little trick: browser views implement `IPublishTraverse`, which
        allows us to catch traversal steps.
        """
        if self.document is not None:
            raise NotFound(self, name, request)

        documents = getUtility(ISiteRoot).documents
        for lang in self._getLanguages():
            docs = documents.get(lang, None)
            app = docs.get("appendix", None)
            if app is None:
                continue
            self.document = app.get(name, None)
            if self.document is not None:
                break
        else:
            raise NotFound(self, name, request)

        return self
