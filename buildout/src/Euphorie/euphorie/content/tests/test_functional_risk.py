from euphorie.content.tests.functional import EuphorieContentTestCase


class RiskTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createRisk(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
        sector=self._create(country, "euphorie.sector", "sector")
        surveygroup=self._create(sector, "euphorie.surveygroup", "group")
        survey=self._create(surveygroup, "euphorie.survey", "survey")
        module=self._create(survey, "euphorie.module", "module")
        risk=self._create(module, "euphorie.risk", "risk")
        return risk

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types=[fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.risk" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        risk=self.createRisk()
        types=[fti.id for fti in risk.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.solution"]))

    def testConditionalFtiUsed(self):
        from euphorie.content.fti import ConditionalDexterityFTI
        fti=getattr(self.portal.portal_types, "euphorie.risk")
        self.failUnless(isinstance(fti, ConditionalDexterityFTI))


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)



