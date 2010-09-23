import unittest
from euphorie.content.tests.functional import EuphorieContentTestCase


class ProfileQuestionTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createProfileQuestion(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
        sector=self._create(country, "euphorie.sector", "sector")
        surveygroup=self._create(sector, "euphorie.surveygroup", "group")
        survey=self._create(surveygroup, "euphorie.survey", "survey")
        pq=self._create(survey, "euphorie.profilequestion", "profilequestion")
        return pq

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types=[fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.profilequestion" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        model=self.createProfileQuestion()
        types=[fti.id for fti in model.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.module",
                                          "euphorie.risk"]))


def test_suite():
        return unittest.defaultTestLoader.loadTestsFromName(__name__)


