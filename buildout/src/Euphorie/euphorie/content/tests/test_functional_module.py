import unittest
from euphorie.content.tests.functional import EuphorieContentTestCase


class ModuleTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        country=self._create(container, "euphorie.country", "nl")
        sector=self._create(country, "euphorie.sector", "sector")
        surveygroup=self._create(sector, "euphorie.surveygroup", "group")
        survey=self._create(surveygroup, "euphorie.survey", "survey")
        module=self._create(survey, "euphorie.module", "module")
        return module

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types=[fti.id for fti in self.portal.allowedContentTypes()]
        self.failUnless("euphorie.module" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        module=self.createModule()
        types=[fti.id for fti in module.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.module",
                                          "euphorie.risk"]))

    def testConditionalFtiUsed(self):
        from euphorie.content.fti import ConditionalDexterityFTI
        fti=getattr(self.portal.portal_types, "euphorie.module")
        self.failUnless(isinstance(fti, ConditionalDexterityFTI))


def test_suite():
        return unittest.defaultTestLoader.loadTestsFromName(__name__)

