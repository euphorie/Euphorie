from zope.interface import Interface
from five import grok
from Products.CMFCore.utils import getToolByName
from plonetheme.nuplone.skin.interfaces import NuPloneSkin

grok.templatedir("templates")

SEARCHED_TYPES = ["euphorie.documentation",
                  "euphorie.help",
                  "euphorie.sector",
                  "euphorie.module",
                  "euphorie.profilequestion",
                  "euphorie.risk",
                  "euphorie.survey",
                  "euphorie.surveygroup",
                  "euphorie.page",
                  ]


class Search(grok.View):
    grok.context(Interface)
    grok.name("search")
    grok.require("zope2.View")
    grok.template("search")
    grok.layer(NuPloneSkin)

    def update(self):
        query = self.request.form.get("q", None)
        self.did_search = (query is not None)
        if not query:
            self.results = None
            return

        ct = getToolByName(self.context, "portal_catalog")
        self.results = ct.searchResults(SearchableText=query,
                portal_type=SEARCHED_TYPES)
