from euphorie.deployment.tests.functional import EuphorieTestCase


class ProfileQuestionTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createProfileQuestion(self):
        country=self.portal.sectors.nl
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
        pq=self.createProfileQuestion()
        types=[fti.id for fti in pq.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.module",
                                          "euphorie.risk"]))

    def testCanBeCopied(self):
        self.loginAsPortalOwner()
        pq=self.createProfileQuestion()
        self.assertTrue(pq.cb_isCopyable())
