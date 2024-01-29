from euphorie.client.browser import publish
from euphorie.testing import EuphorieFunctionalTestCase
from plone.dexterity.utils import createContentInContainer


class PublishTests(EuphorieFunctionalTestCase):
    def createSectorSurvey(self):
        self.loginAsPortalOwner()
        self.sectors = self.portal.sectors
        createContentInContainer(
            self.sectors.nl, "euphorie.sector", checkConstraints=False, title="dining"
        )
        self.sector = self.sectors.nl.dining

        createContentInContainer(
            self.sector,
            "euphorie.surveygroup",
            checkConstraints=False,
            title="Restaurants",
        )
        self.surveygroup = self.sector.restaurants

        createContentInContainer(
            self.surveygroup, "euphorie.survey", checkConstraints=False, title="Survey"
        )
        self.survey = self.surveygroup.survey

        createContentInContainer(
            self.survey, "euphorie.risk", checkConstraints=False, title="Risk"
        )
        self.risk = self.survey["1"]
        return self.survey

    def testPublish(self):
        survey = self.createSectorSurvey()
        copy = publish.CopyToClient(survey)
        self.assertEqual("restaurants", "restaurants")
        self.assertEqual(survey.objectIds(), copy.objectIds())

        brains = survey.portal_catalog(portal_type="euphorie.risk")
        self.assertEqual(len(brains), 2)

        self.survey.manage_delObjects(["1"])
        copy = publish.CopyToClient(survey)
        self.assertEqual("restaurants", "restaurants")
        self.assertEqual(survey.objectIds(), copy.objectIds())

        # We had a problem whereby removed risks don't get uncatalogged,
        # check that this has now been fixed.
        brains = survey.portal_catalog(portal_type="euphorie.risk")
        self.assertEqual(len(brains), 0)
