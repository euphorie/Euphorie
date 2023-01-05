from Acquisition import aq_parent
from euphorie.content.risk import EnsureInterface
from euphorie.content.risk import Risk
from euphorie.content.tests.utils import addSurvey
from euphorie.content.tests.utils import createSector
from euphorie.testing import EuphorieFunctionalTestCase
from euphorie.testing import EuphorieIntegrationTestCase
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

import re


class RiskTests(EuphorieIntegrationTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createRisk(self, algorithm="kinney"):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(
            sector, "euphorie.surveygroup", "group", evaluation_algorithm=algorithm
        )
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        module = self._create(survey, "euphorie.module", "module")
        risk = self._create(module, "euphorie.risk", "risk")
        EnsureInterface(risk)
        return risk

    def testNotGloballyAllowed(self):
        self.loginAsPortalOwner()
        types = [fti.id for fti in self.portal.allowedContentTypes()]
        self.assertTrue("euphorie.risk" not in types)

    def testAllowedContentTypes(self):
        self.loginAsPortalOwner()
        risk = self.createRisk()
        types = [fti.id for fti in risk.allowedContentTypes()]
        self.assertEqual(set(types), {"euphorie.solution"})

    def testCanBeCopied(self):
        self.loginAsPortalOwner()
        risk = self.createRisk()
        self.assertTrue(risk.cb_isCopyable())

    def testDefaultEvaluationAlgorithm(self):
        risk = Risk()
        self.assertEqual(risk.evaluation_algorithm(), "kinney")

    def testFrenchEvaluationAlgorithm(self):
        self.loginAsPortalOwner()
        risk = self.createRisk("french")
        self.assertEqual(risk.evaluation_algorithm(), "french")


class RiskFunctionalTests(EuphorieFunctionalTestCase):
    _default_credentials = {
        "username": SITE_OWNER_NAME,
        "password": SITE_OWNER_PASSWORD,
    }

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createRisk(self, algorithm="kinney"):
        country = self.portal.sectors.nl
        sector = self._create(country, "euphorie.sector", "sector")
        surveygroup = self._create(
            sector, "euphorie.surveygroup", "group", evaluation_algorithm=algorithm
        )
        survey = self._create(surveygroup, "euphorie.survey", "survey")
        module = self._create(survey, "euphorie.module", "module")
        risk = self._create(module, "euphorie.risk", "risk")
        EnsureInterface(risk)
        return risk

    def testDescriptionSanitised(self):
        self.loginAsPortalOwner()
        risk = self.createRisk()
        risk.title = "Risk title"
        risk.problem_description = "Problem description"
        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % risk.absolute_url())
        browser.getControl(name="form.widgets.description").value = "Raw text"
        browser.handleErrors = False
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(risk.description, "<p>Raw text</p>")

    def testLegalReferenceSanitised(self):
        self.loginAsPortalOwner()
        risk = self.createRisk()
        risk.title = "Risk title"
        risk.description = "<p>Description</p>"
        risk.problem_description = "Problem description"
        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % risk.absolute_url())
        browser.getControl(name="form.widgets.legal_reference").value = "Raw text"
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(risk.legal_reference, "<p>Raw text</p>")

    def testFrenchEvaluationOptionsShown(self):
        self.loginAsPortalOwner()
        risk = self.createRisk("french")
        risk.default_frequency = 9
        risk.default_severity = 7
        group = aq_parent(aq_parent(aq_parent(risk)))
        self.assertEqual(group.evaluation_algorithm, "french")
        browser = self.get_browser(logged_in=True)
        browser.handleErrors = False
        browser.open(risk.absolute_url())
        self.assertTrue("Severe" in browser.contents)
        self.assertTrue("Very often or regularly" in browser.contents)

    def testImageFromOtherSectorAccount(self):
        # http://code.simplon.biz/tracker/euphorie/ticket/143
        sector = createSector(self.portal, login="sector")
        self.loginAsPortalOwner()
        survey = addSurvey(sector)
        createSector(self.portal, id="sector2", login="sector2", password="sector2")
        self.logout()
        browser = self.get_browser()
        browser.open("%s/@@login" % self.portal.absolute_url())
        browser.getControl(name="__ac_name").value = "sector2"
        browser.getControl(name="__ac_password").value = "sector2"
        browser.getForm(id="loginForm").submit()
        risk = survey["1"]["2"]
        browser.open(risk.absolute_url())
        match = re.search(
            r'<div class="introduction">\s*<img[^>]+src="([^"]+)', browser.contents
        )
        self.assertTrue(match)
        image_url = match.group(1)
        browser.open(image_url)
        self.assertEqual(browser.isHtml, False)
        self.assertEqual(browser.headers.get_content_maintype(), "image")

    def testFixedPriorityForm(self):
        # See https://github.com/euphorie/Euphorie/pull/98
        self.loginAsPortalOwner()
        risk = self.createRisk()
        risk.title = "Risk title"
        risk.description = "<p>Description</p>"
        risk.problem_description = "Problem description"
        browser = self.get_browser(logged_in=True)
        browser.open("%s/@@edit" % risk.absolute_url())
        browser.getControl(name="form.widgets.evaluation_method").value = ["fixed"]
        browser.getControl(name="form.widgets.default_priority").value = ["low"]
        browser.getControl(name="form.widgets.fixed_priority").value = ["high"]
        browser.getControl(name="form.buttons.save").click()
        self.assertEqual(risk.fixed_priority, "high")


class ConstructionFilterTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()

    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createStructure(self):
        self.country = self.portal.sectors.nl
        self.sector = self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup = self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey = self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module = self._create(self.survey, "euphorie.module", "module")

    def testPreventRiskIfModuleExists(self):
        self.createStructure()
        types = [fti.id for fti in self.module.allowedContentTypes()]
        self.assertTrue("euphorie.risk" in types)
        self._create(self.module, "euphorie.module", "module")
        types = [fti.id for fti in self.module.allowedContentTypes()]
        self.assertTrue("euphorie.risk" not in types)
