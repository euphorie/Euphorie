from euphorie.content import MessageFactory as _
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from zope.interface import Interface

grok.templatedir("templates")

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

SEARCHED_TYPES = TYPES_MAP.keys()


class Search(grok.View):
    grok.context(Interface)
    grok.name("search")
    grok.require("zope2.View")
    grok.template("search")
    grok.layer(NuPloneSkin)

    def update(self):
        qs = self.request.form.get("q", None)
        self.did_search = (qs is not None)
        if not qs:
            self.results = None
            return

        query = dict(
            SearchableText=qs, portal_type=SEARCHED_TYPES)
        ct = getToolByName(self.context, "portal_catalog")
        self.results = ct.searchResults(**query)


class ContextSearch(grok.View):
    grok.context(Interface)
    grok.name("context-search")
    grok.require("zope2.View")
    grok.template("context_search")
    grok.layer(NuPloneSkin)

    def update(self):
        qs = self.request.form.get("q", None)
        self.did_search = (qs is not None and qs.strip() != '')
        if not qs:
            self.results = None
            return

        qs = u'"{}*"'.format(safe_unicode(qs))
        path = '/'.join(self.context.getPhysicalPath())
        query = dict(
            SearchableText=qs, portal_type=SEARCHED_TYPES, path=path)

        ct = getToolByName(self.context, "portal_catalog")
        brains = ct.searchResults(**query)

        results = [
            dict(
                url=b.getURL(), title=b.Title,
                typ=TYPES_MAP.get(b.portal_type, 'unknown'))
            for b in brains]
        self.results = results
