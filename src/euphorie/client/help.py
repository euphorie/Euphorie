"""
Help
----

The @@help view.
"""

import logging
from zope.interface import Interface
from zope.component import getUtility
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from euphorie.client.interfaces import IClientSkinLayer

log = logging.getLogger(__name__)

grok.templatedir("templates")


class HelpView(grok.View):
    """View name: @@help
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name("help")
    grok.template("help")

    def _getLanguages(self):
        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        if "-" in lang:
            return [lang, lang.split("-")[0], "en"]
        else:
            return [lang, "en"]

    def findHelp(self):
        documents = getUtility(ISiteRoot).documents

        help = None
        for lang in self._getLanguages():
            docs = documents.get(lang, None)
            if docs is None:
                continue
            help = docs.get("help", None)
            if help is not None:
                return help

    def update(self):
        self.help = self.findHelp()
