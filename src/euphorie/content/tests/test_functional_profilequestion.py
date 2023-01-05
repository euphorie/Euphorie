from Acquisition import aq_parent
from euphorie.testing import EuphorieIntegrationTestCase


class ProfileQuestionTests(EuphorieIntegrationTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createProfileQuestion(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        pq = self._create(survey, "euphorie.profilequestion", "profilequestion")
        return pq

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.assertTrue("euphorie.profilequestion" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        pq = self.createProfileQuestion()
        types = [fti.id for fti in pq.allowedContentTypes()]
        self.assertEqual(set(types), {"euphorie.module", "euphorie.risk"})

    def testCanBeCopied(self):
        self.loginAsPortalOwner()
        pq = self.createProfileQuestion()
        self.assertTrue(pq.cb_isCopyable())

    def test_verifyObjectPaste_acceptablePaste(self):
        self.loginAsPortalOwner()
        target = self.createProfileQuestion()
        survey = aq_parent(target)
        source = self._create(survey, "euphorie.module", "other")
        target._verifyObjectPaste(source)

    def test_verifyObjectPaste_block_if_result_too_deep(self):
        self.loginAsPortalOwner()
        target = self.createProfileQuestion()
        survey = aq_parent(target)
        source = self._create(survey, "euphorie.module", "other")
        other = self._create(source, "euphorie.module", "other")
        self._create(other, "euphorie.module", "other")
        self.assertRaises(ValueError, target._verifyObjectPaste, source)
