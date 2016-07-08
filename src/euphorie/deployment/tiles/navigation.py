from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.tiles.navigation import INavtreeFactory
from plonetheme.nuplone.tiles.navigation import CatalogNavTree
from plone.tiles import Tile
from euphorie.content.country import ICountry
from euphorie.content.utils import summarizeCountries


class _DummyBrain:
    portal_type = None

DummyBrain = _DummyBrain()


class EuphorieNavtreeFactory(grok.MultiAdapter):
    """Special navigation tree for the Euphorie surveys. This navtree
    factory modifies the navtree data to remove the survey level from
    the navtree and making the survey contents appear directly underneath
    the surveygroup. This hides versioning implementation from the user.
    """
    grok.adapts(Interface, NuPloneSkin)
    grok.implements(INavtreeFactory)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        tree = CatalogNavTree(self.context, self.request)
        walker = tree.iter()
        node = walker.next()

        try:
            while True:
                pt = node.get("brain", DummyBrain).portal_type
                if pt == "euphorie.surveygroup":
                    if not node["ancestor"]:
                        node = walker.send("prune")
                        continue

                    # Cut out the middle man
                    survey = [child for child in node["children"]
                              if child["ancestor"] or child["current"]]
                    node["children"] = survey[0]["children"]
                node = walker.next()
        except StopIteration:
            pass
        return tree


class UserManagementNavtree(Tile):
    """Special navigation tree for the usermanagement page. This tree
    uses the locale to get the proper names for the countries instead
    of using the titles of the country objects.
    """
    def update(self):
        country_id = self.context.id
        container = aq_parent(aq_inner(self.context))
        self.countries = summarizeCountries(container, self.request,
                country_id, "Euphorie: Manage country")

    def __call__(self):
        if not ICountry.providedBy(self.context):
            return None

        self.update()
        if len(self.countries) < 2:
            return None
        else:
            return self.index()
