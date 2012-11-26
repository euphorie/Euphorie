from euphorie.deployment.tests.functional import EuphorieTestCase


class DirtyTreeTests(EuphorieTestCase):
    def create(self):
        from euphorie.content.tests.utils import createSector
        from euphorie.content.tests.utils import addSurvey
        from euphorie.content.tests.utils import EMPTY_SURVEY
        sector = createSector(self.portal)
        return addSurvey(sector, EMPTY_SURVEY)

    def testStartClean(self):
        from euphorie.content.behaviour.dirtytree import isDirty
        self.loginAsPortalOwner()
        survey = self.create()
        self.assertEqual(isDirty(survey), False)

    def testAddObjectMakesDirty(self):
        from euphorie.content.behaviour.dirtytree import isDirty
        self.loginAsPortalOwner()
        survey = self.create()
        survey.invokeFactory("euphorie.module", "module")
        self.assertEqual(isDirty(survey), True)

    def testDeleteObjetMakesDiry(self):
        from euphorie.content.behaviour.dirtytree import isDirty
        from euphorie.content.behaviour.dirtytree import clearDirty
        self.loginAsPortalOwner()
        survey = self.create()
        survey.invokeFactory("euphorie.module", "module")
        clearDirty(survey)
        del survey["module"]
        self.assertEqual(isDirty(survey), True)

    def testModifyObjectMakesDirty(self):
        from euphorie.content.behaviour.dirtytree import isDirty
        from euphorie.content.behaviour.dirtytree import clearDirty
        from zope.event import notify
        from zope.lifecycleevent import ObjectModifiedEvent
        self.loginAsPortalOwner()
        survey = self.create()
        survey.invokeFactory("euphorie.module", "module")
        clearDirty(survey)
        notify(ObjectModifiedEvent(survey["module"]))
        self.assertEqual(isDirty(survey), True)


class RichDescriptionTests(EuphorieTestCase):
    def _create(self, container, *args, **kwargs):
        newid = container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        self.country = self.portal.sectors.nl
        self.sector = self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup = self._create(self.sector,
                "euphorie.surveygroup", "group")
        self.survey = self._create(self.surveygroup,
                "euphorie.survey", "survey")
        self.module = self._create(self.survey, "euphorie.module", "module")
        return self.module

    def testNoMarkup(self):
        self.setRoles(["Manager"])
        module = self.createModule()
        module.description = u"Raw text"
        module.indexObject()
        brain = self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, u"Raw text")

    def testStrayBracket(self):
        self.setRoles(["Manager"])
        module = self.createModule()
        module.description = u"Test <em>me</em> >"
        module.indexObject()
        brain = self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, u"Test me >")

    def testNone(self):
        self.setRoles(["Manager"])
        module = self.createModule()
        module.description = None
        module.indexObject()
        brain = self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, None)
