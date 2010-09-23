import unittest
from euphorie.content.tests.functional import EuphorieContentTestCase


class SurveyTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createSurvey(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
        sector=self._create(country, "euphorie.sector", "sector")
        surveygroup=self._create(sector, "euphorie.surveygroup", "group")
        survey=self._create(surveygroup, "euphorie.survey", "survey")
        return survey

    def testNoWorkflow(self):
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        chain=self.folder.portal_workflow.getChainFor(survey)
        self.assertEqual(chain, ())

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types=[fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.survey" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        survey=self.createSurvey()
        types=[fti.id for fti in survey.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.module",
                                          "euphorie.profilequestion"]))


def test_suite():
        return unittest.defaultTestLoader.loadTestsFromName(__name__)

