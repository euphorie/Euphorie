from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from transaction import commit


class ModuleTests(EuphorieIntegrationTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(sector, "euphorie.surveygroup", "group")
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        module = self._create(survey, "euphorie.module", "module")
        return module

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.assertTrue("euphorie.module" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        module = self.createModule()
        types = [fti.id for fti in module.allowedContentTypes()]
        self.assertEqual(set(types), {"euphorie.module", "euphorie.risk"})

    def testConditionalFtiUsed(self):
        from euphorie.content.fti import ConditionalDexterityFTI

        fti = getattr(self.portal.portal_types, "euphorie.module")
        self.assertTrue(isinstance(fti, ConditionalDexterityFTI))

    def testCanBeCopied(self):
        self.loginAsPortalOwner()
        module = self.createModule()
        self.assertTrue(module.cb_isCopyable())

    def test_verifyObjectPaste_acceptablePaste(self):
        from Acquisition import aq_parent

        self.loginAsPortalOwner()
        target = self.createModule()
        survey = aq_parent(target)
        source = self._create(survey, "euphorie.module", "other")
        target._verifyObjectPaste(source)

    def test_verifyObjectPaste_block_if_result_too_deep(self):
        from Acquisition import aq_parent

        self.loginAsPortalOwner()
        target = self.createModule()
        survey = aq_parent(target)
        source = self._create(survey, "euphorie.module", "other")
        other = self._create(source, "euphorie.module", "other")
        self._create(other, "euphorie.module", "other")
        self.assertRaises(ValueError, target._verifyObjectPaste, source)


class ConstructionFilterTests(EuphorieIntegrationTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createStructure(self):
        self.country = self.portal.sectors.nl
        self.sector = self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup = self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey = self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module = self._create(self.survey, "euphorie.module", "module")

    def testValidDepthInModule(self):
        self.loginAsPortalOwner()
        self.createStructure()
        types = [fti.id for fti in self.module.allowedContentTypes()]
        self.assertTrue("euphorie.module" in types)

    def testMaxDepthInModule(self):
        self.loginAsPortalOwner()
        self.createStructure()
        submodule = self._create(self.module, "euphorie.module", "module")
        subsubmodule = self._create(submodule, "euphorie.module", "module")
        types = [fti.id for fti in subsubmodule.allowedContentTypes()]
        self.assertTrue("euphorie.module" not in types)

    def testPreventModuleIfRiskExists(self):
        self.loginAsPortalOwner()
        self.createStructure()
        types = [fti.id for fti in self.module.allowedContentTypes()]
        self.assertTrue("euphorie.module" in types)
        self._create(self.module, "euphorie.risk", "risk")
        types = [fti.id for fti in self.module.allowedContentTypes()]
        self.assertTrue("euphorie.module" not in types)


class FunctionalTests(EuphorieFunctionalTestCase):
    _default_credentials = {
        "username": SITE_OWNER_NAME,
        "password": SITE_OWNER_PASSWORD,
    }

    def _create(self, container, *args, **kwargs):
        with api.env.adopt_user("admin"):
            newid = container.invokeFactory(*args, **kwargs)
            return getattr(container, newid)

    def createStructure(self):
        with api.env.adopt_user("admin"):
            self.country = self.portal.sectors.nl
            self.sector = self._create(self.country, "euphorie.sector", "sector")
            self.surveygroup = self._create(
                self.sector, "euphorie.surveygroup", "group"
            )
            self.survey = self._create(self.surveygroup, "euphorie.survey", "survey")
            self.module = self._create(self.survey, "euphorie.module", "module")
            commit()

    def testEditTitleForModule(self):
        self.createStructure()
        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % self.module.absolute_url())
        self.assertTrue("Edit Module" in browser.contents)

    def testEditTitleForSubModule(self):
        self.createStructure()
        submodule = self._create(self.module, "euphorie.module", "module")
        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % submodule.absolute_url())
        self.assertTrue("Edit Module" not in browser.contents)
        self.assertTrue("Edit Submodule" in browser.contents)

    def testInactiveHideFromTrainingBehavior(self):
        """When `euphorie.hide_from_training` is not activated, the
        `hide_from_training` field should not be visible.
        """
        self.createStructure()

        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % self.module.absolute_url())

        self.assertTrue(
            'name="form.widgets.IHideFromTraining.hide_from_training:list"'
            not in browser.contents
        )

    def testActiveHideFromTrainingBehavior(self):
        """When `euphorie.hide_from_training` is activated, the
        `hide_from_training` field should be visible.
        """
        self.createStructure()

        portal_types = api.portal.get_tool("portal_types")
        fti = portal_types["euphorie.module"]
        fti.behaviors = tuple(list(fti.behaviors) + ["euphorie.hide_from_training"])

        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % self.module.absolute_url())

        self.assertTrue(
            'name="form.widgets.IHideFromTraining.hide_from_training:list"'
            in browser.contents
        )
