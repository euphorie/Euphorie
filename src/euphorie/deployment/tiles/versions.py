from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.content.sector import getSurveys
from euphorie.content.sector import ISector
from euphorie.content.utils import survey_client_url
from functools import cached_property
from plone.tiles import Tile
from plonetheme.nuplone.utils import checkPermission


class SurveyVersions(Tile):
    @cached_property
    def published_url(self):
        return survey_client_url(self.context, must_exist=True)

    @cached_property
    def preview_url(self):
        return survey_client_url(self.context, must_exist=True, preview=True)

    def update(self):
        for sector in aq_chain(aq_inner(self.context)):
            if ISector.providedBy(sector):
                break
        else:
            sector = aq_inner(self.context)

        self.action_url = "%s/@@version-command" % sector.absolute_url()
        self.surveys = getSurveys(self.context)

    def __call__(self):
        if not checkPermission(self.context, "CMFEditions: Access previous versions"):
            return None

        self.update()
        return self.index()
