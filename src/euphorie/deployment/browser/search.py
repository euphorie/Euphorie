from euphorie.content import MessageFactory as _
from plone import api
from plone.base.utils import safe_text
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.Five import BrowserView


TYPES_MAP = {
    "euphorie.documentation": "Documentation",
    "euphorie.help": "Help",
    "euphorie.sector": _("Sector"),
    "euphorie.module": _("Module"),
    "euphorie.profilequestion": _("Profile question"),
    "euphorie.risk": _("Risk"),
    "euphorie.survey": _("OiRA Tool version"),
    "euphorie.surveygroup": _("OiRA Tool"),
    "euphorie.page": "Page",
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

        qs = f'"{safe_text(qs)}*"'
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
