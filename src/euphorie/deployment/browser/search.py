from euphorie.content import MessageFactory as _
from plone import api
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView


TYPES_MAP = {
    "euphorie.documentation": u"Documentation",
    "euphorie.help": u"Help",
    "euphorie.sector": _(u"Sector"),
    "euphorie.module": _(u"Module"),
    "euphorie.profilequestion": _(u"Profile question"),
    "euphorie.risk": _(u"Risk"),
    "euphorie.survey": _(u"OiRA Tool version"),
    "euphorie.surveygroup": _(u"OiRA Tool"),
    "euphorie.page": u"Page",
}

SEARCHED_TYPES = list(TYPES_MAP.keys())


class Search(BrowserView):
    @property
    @memoize_contextless
    def did_search(self):
        qs = self.request.form.get("q", None)
        return qs is not None

    @property
    @memoize_contextless
    def results(self):
        qs = self.request.form.get("q", None)
        if not qs:
            return

        query = {"SearchableText": qs, "portal_type": SEARCHED_TYPES}
        ct = api.portal.get_tool("portal_catalog")
        return ct.searchResults(**query)


class ContextSearch(BrowserView):
    @property
    @memoize
    def did_search(self):
        qs = self.request.form.get("q", None)
        return qs is not None and qs.strip() != ""

    @property
    @memoize
    def results(self):
        qs = self.request.form.get("q", None)
        if not qs:
            return

        qs = u'"{}*"'.format(safe_unicode(qs))
        path = "/".join(self.context.getPhysicalPath())
        query = {"SearchableText": qs, "portal_type": SEARCHED_TYPES, "path": path}

        ct = api.portal.get_tool("portal_catalog")
        brains = ct.searchResults(**query)

        return [
            {
                "url": brain.getURL(),
                "title": brain.Title,
                "typ": TYPES_MAP.get(brain.portal_type, "unknown"),
            }
            for brain in brains
        ]
