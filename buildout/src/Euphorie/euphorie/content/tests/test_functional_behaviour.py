import unittest
from euphorie.content.tests.functional import EuphorieContentTestCase
from euphorie.content.behaviour.publish import ObjectPublishedEvent
from zope.event import notify

class DeprecationTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createRisk(self):
        self.container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        self.country=self._create(self.container, "euphorie.country", "nl")
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "module")
        self.risk=self._create(self.module, "euphorie.risk", "risk")

        return self.risk

class RichDescriptionTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createModule(self):
        self.container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        self.country=self._create(self.container, "euphorie.country", "nl")
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "module")
        return self.module

    def testNoMarkup(self):
        self.setRoles(["Manager"])
        module=self.createModule()
        module.description=u"Raw text"
        module.indexObject()
        brain=self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, u"Raw text")

    def testStrayBracket(self):
        self.setRoles(["Manager"])
        module=self.createModule()
        module.description=u"Test <em>me</em> >"
        module.indexObject()
        brain=self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, u"Test me >")

    def testNone(self):
        self.setRoles(["Manager"])
        module=self.createModule()
        module.description=None
        module.indexObject()
        brain=self.portal.portal_catalog(portal_type="euphorie.module")[0]
        self.assertEqual(brain.Description, None)



class ObjectPublishedTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createRisk(self):
        self.container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        self.country=self._create(self.container, "euphorie.country", "nl")
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "module")
        self.risk=self._create(self.module, "euphorie.risk", "risk")
        return self.risk

    def testPublishedFlagSetOnPublish(self):
        self.setRoles(["Manager"])
        self.createRisk()
        self.assertEqual(getattr(self.risk, "published", False), False)
        notify(ObjectPublishedEvent(self.survey))
        self.assertEqual(self.risk.published, True)

    def testPublishedFlagNotSetOnNonPublishedObject(self):
        self.setRoles(["Manager"])
        self.createRisk()
        solution=self._create(self.risk, "euphorie.solution", "solution")
        notify(ObjectPublishedEvent(self.survey))
        self.failIf(hasattr(solution.aq_base, "published"))

    def testPublishedFlagRecursivelySetOnPublish(self):
        self.setRoles(["Manager"])
        self.createRisk()
        notify(ObjectPublishedEvent(self.survey))
        self.assertEqual(self.module.published, True)
        self.assertEqual(self.risk.published, True)

    def testCanRemoveUnpublishedRisk(self):
        self.setRoles(["Manager"])
        self.createRisk()
        self.setRoles(["Editor"])
        self.module.manage_delObjects([self.risk.id])

    def testCanNotRemovePublishedRisk(self):
        from AccessControl import Unauthorized
        self.setRoles(["Manager"])
        self.createRisk()
        self.risk.published=True
        self.setRoles(["Editor"])
        self.assertRaises(Unauthorized,
                          self.module.manage_delObjects, [self.risk.id])

    def testManagerCanRemovePublishedRisk(self):
        self.setRoles(["Manager"])
        self.createRisk()
        self.risk.published=True
        self.module.manage_delObjects([self.risk.id])


class MaximumDepthTests(EuphorieContentTestCase):
    def _create(self, container, *args, **kwargs):
        newid=container.invokeFactory(*args, **kwargs)
        return getattr(container, newid)

    def createStructure(self):
        self.container=self._create(self.portal, "euphorie.sectorcontainer", "sectors")
        self.country=self._create(self.container, "euphorie.country", "nl")
        self.sector=self._create(self.country, "euphorie.sector", "sector")
        self.surveygroup=self._create(self.sector, "euphorie.surveygroup", "group")
        self.survey=self._create(self.surveygroup, "euphorie.survey", "survey")
        self.module=self._create(self.survey, "euphorie.module", "module")
        self.submodule=self._create(self.module, "euphorie.module", "module")
        self.subsubmodule=self._create(self.submodule, "euphorie.module", "module")

    def testValidDepthInModule(self):
        self.setRoles(["Manager"])
        self.createStructure()
        types=[fti.id for fti in self.module.allowedContentTypes()]
        self.assertEqual(set(types), set(["euphorie.module",
                                          "euphorie.risk"]))

    def testMaxDepthInModule(self):
        self.setRoles(["Manager"])
        self.createStructure()
        types=[fti.id for fti in self.subsubmodule.allowedContentTypes()]
        self.assertEqual(types, [])



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)



