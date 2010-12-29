from euphorie.deployment.tests.functional import EuphorieTestCase
from euphorie.deployment.tests.functional import EuphorieFunctionalTestCase


class ModuleTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        country=self.portal.sectors.nl
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

    def testCanBeCopied(self):
        self.loginAsPortalOwner()
        module=self.createModule()
        self.assertTrue(module.cb_isCopyable())



class ConstructionFilterTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createStructure(self):
        self.country=self.portal.sectors.nl
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "module")

    def testValidDepthInModule(self):
        self.setRoles(["Manager"])
        self.createStructure()
        types=[fti.id for fti in self.module.allowedContentTypes()]
        self.failUnless("euphorie.module" in types)

    def testMaxDepthInModule(self):
        self.setRoles(["Manager"])
        self.createStructure()
        submodule=self._create(self.module, "euphorie.module", "module")
        subsubmodule=self._create(submodule, "euphorie.module", "module")
        types=[fti.id for fti in subsubmodule.allowedContentTypes()]
        self.failUnless("euphorie.module" not in types)
    
    def testPreventModuleIfRiskExists(self):
        self.setRoles(["Manager"])
        self.createStructure()
        types=[fti.id for fti in self.module.allowedContentTypes()]
        self.failUnless("euphorie.module" in types)
        self._create(self.module, "euphorie.risk", "risk")
        types=[fti.id for fti in self.module.allowedContentTypes()]
        self.failUnless("euphorie.module" not in types)


class FunctionalTests(EuphorieFunctionalTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createStructure(self):
        self.country=self.portal.sectors.nl
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "module")

    def testEditTitleForModule(self):
        self.setRoles(["Manager"])
        self.createStructure()
        browser=self.adminBrowser()
        browser.open("%s/@@edit" % self.module.absolute_url())
        self.assertTrue("Edit Module" in browser.contents)

    def testEditTitleForSubModule(self):
        self.setRoles(["Manager"])
        self.createStructure()
        submodule=self._create(self.module, "euphorie.module", "module")
        browser=self.adminBrowser()
        browser.open("%s/@@edit" % submodule.absolute_url())
        self.assertTrue("Edit Module" not in browser.contents)
        self.assertTrue("Edit Submodule" in browser.contents)

