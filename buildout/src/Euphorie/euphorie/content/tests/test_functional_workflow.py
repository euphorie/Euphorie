import unittest
from Acquisition import aq_inner
from euphorie.content.tests.functional import EuphorieContentTestCase
from euphorie.content.module import Module


class DepercationWorkflowTests(EuphorieContentTestCase):
    def createModule(self):
        module=Module("module")
        module.portal_type="euphorie.module"
        self.portal._setObject("module", module)
        return self.portal.module

    def transitionsFor(self, object):
        wt=self.portal.portal_workflow
        transitions=wt.listActionInfos(object=aq_inner(object))
        return set([trans["id"] for trans in transitions
                    if trans["category"]=="workflow"])

    def testInitialStateIsCurrent(self):
        module=self.createModule()
        self.assertEqual(self.portal.portal_workflow.getInfoFor(module, "review_state"),
                         "current")

    def testTransitionsFromCurrent(self):
        module=self.createModule()
        self.assertEqual(self.transitionsFor(module), set(["deprecate"]))

    def testTransitions(self):
        module=self.createModule()
        wt=self.portal.portal_workflow
        wt.doActionFor(module, "deprecate")
        self.assertEqual(wt.getInfoFor(module, "review_state"), "deprecated")
        wt.doActionFor(module, "reinstate")
        self.assertEqual(wt.getInfoFor(module, "review_state"), "current")

    def testTransitionsFromDeprecated(self):
        module=self.createModule()
        wt=self.portal.portal_workflow
        wt.doActionFor(module, "deprecate")
        self.assertEqual(self.transitionsFor(module), set(["reinstate"]))

    def testCanAddContentWhenCurrent(self):
        self.loginAsPortalOwner()
        module=self.createModule()
        types=[fti.id for fti in module.allowedContentTypes()]
        self.failUnless(len(types)>0)

    def testCanAddContentWhenDeprecated(self):
        self.loginAsPortalOwner()
        module=self.createModule()
        wt=self.portal.portal_workflow
        wt.doActionFor(module, "deprecate")
        types=[fti.id for fti in module.allowedContentTypes()]
        self.failUnless(len(types)==0)



def test_suite():
        return unittest.defaultTestLoader.loadTestsFromName(__name__)

