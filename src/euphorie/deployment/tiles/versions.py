from Acquisition import aq_chain
from Acquisition import aq_inner
from plone.tiles import Tile
from euphorie.content.sector import ISector
from euphorie.content.sector import getSurveys
from plonetheme.nuplone.utils import checkPermission


class SurveyVersions(Tile):
    def update(self):
        for sector in aq_chain(aq_inner(self.context)):
            if ISector.providedBy(sector):
                break
        else:
            sector = aq_inner(self.context)

        self.action_url = "%s/@@version-command" % sector.absolute_url()
        self.surveys = getSurveys(self.context)

    def __call__(self):
        if not checkPermission(self.context,
                "CMFEditions: Access previous versions"):
            return None

        self.update()
        return self.index()
