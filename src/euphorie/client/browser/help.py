# coding=utf-8
"""
Help
----

The @@help view.
Obsolete, since we now serve help content from client/resources/oira/help,
maintained via the prototype.
"""

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getUtility

import logging


log = logging.getLogger(__name__)


class HelpView(BrowserView):
    """View name: @@help"""

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

    @property
    def help(self):
        return self.findHelp()
