from euphorie.content.behaviour.dirtytree import clearDirty
from euphorie.content.behaviour.dirtytree import isDirty
from euphorie.content.tests.utils import addSurvey
from euphorie.content.tests.utils import createSector
from euphorie.content.tests.utils import EMPTY_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class DirtyTreeTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()

    def create(self):
        sector = createSector(self.portal)
        return addSurvey(sector, EMPTY_SURVEY)

    def testStartClean(self):
        survey = self.create()
        self.assertEqual(isDirty(survey), False)

    def testAddObjectMakesDirty(self):
        survey = self.create()
        survey.invokeFactory("euphorie.module", "module")
        self.assertEqual(isDirty(survey), True)

    def testDeleteObjetMakesDiry(self):
        survey = self.create()
        survey.invokeFactory("euphorie.module", "module")
        clearDirty(survey)
        del survey["module"]
        self.assertEqual(isDirty(survey), True)

    def testModifyObjectMakesDirty(self):
        survey = self.create()
        survey.invokeFactory("euphorie.module", "module")
        clearDirty(survey)
        notify(ObjectModifiedEvent(survey["module"]))
        self.assertEqual(isDirty(survey), True)


class RichDescriptionTests(EuphorieIntegrationTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        with api.env.adopt_user("admin"):
            self.country = self.portal.sectors.nl
            self.sector = self._create(self.country, "euphorie.sector", "sector")
            self.surveygroup = self._create(
                self.sector, "euphorie.surveygroup", "group"
            )
            self.survey = self._create(self.surveygroup, "euphorie.survey", "survey")
            self.module = self._create(self.survey, "euphorie.module", "module")
        return self.module

    def testNoMarkup(self):
        module = self.createModule()
        module.description = "Raw text"
        module.indexObject()
        brain = self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, "Raw text")

    def testStrayBracket(self):
        module = self.createModule()
        module.description = "Test <em>me</em> >"
        module.indexObject()
        brain = self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, "Test me >")

    def testNone(self):
        module = self.createModule()
        module.description = None
        module.indexObject()
        brain = self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, None)
