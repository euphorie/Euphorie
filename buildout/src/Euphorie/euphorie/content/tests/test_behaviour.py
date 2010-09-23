import unittest
import Acquisition
from zope.interface import alsoProvides
from zope.annotation.interfaces import IAttributeAnnotatable
from euphorie.content.behaviour.uniqueid import UniqueNameChooser
from euphorie.content.behaviour.uniqueid import IIdGenerationRoot
from euphorie.content.behaviour.uniqueid import INameFromUniqueId
from euphorie.content.behaviour.deprecation import WorkflowDeprecatable
from euphorie.content.behaviour.publish import ObjectPublished
from euphorie.content.behaviour.maxdepth import SurveyDepthConstructionFilter
from euphorie.content.behaviour.richdescription import Description
from zope.component.testing import PlacelessSetup
from zope.interface import implements

class Mock(Acquisition.Implicit):
    implements(INameFromUniqueId)


class IdGenerationTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        super(IdGenerationTests, self).setUp()
        from zope.component import provideAdapter
        from zope.annotation.attribute import AttributeAnnotations
        provideAdapter(AttributeAnnotations)

    def makeRoot(self):
        root=Mock()
        alsoProvides(root, IAttributeAnnotatable, IIdGenerationRoot)
        return root

    def test_ValueErrorIfNoRoot(self):
        chooser=UniqueNameChooser(Mock())
        self.assertRaises(ValueError, chooser.chooseName, None, Mock())


    def testValueErrorIfRootNotAnnotatable(self):
        root=Mock()
        alsoProvides(root, IIdGenerationRoot)
        chooser=UniqueNameChooser(root)
        self.assertRaises(ValueError, chooser.chooseName, None, Mock())

    def testFirstIdIsOne(self):
        root=self.makeRoot()
        obj=Mock()
        UniqueNameChooser(root).chooseName(None, obj)
        self.assertEqual(obj.id, "1")

    def testSecondIdIsTwo(self):
        root=self.makeRoot()
        obj=Mock()
        chooser=UniqueNameChooser(root)
        chooser.chooseName(None, obj)
        del obj.id
        chooser.chooseName(None, obj)
        self.assertEqual(obj.id, "2")

    def testUseExitingIdIfPresent(self):
        root=self.makeRoot()
        obj=Mock()
        obj.id="mock"
        UniqueNameChooser(root).chooseName(None, obj)
        self.assertEqual(obj.id, "mock")

    def testExtraDepth(self):
        root=self.makeRoot()
        folder=Mock().__of__(root)
        obj=Mock()
        UniqueNameChooser(folder).chooseName(None, obj)
        self.assertEqual(obj.id, "1")


class MockWorkflowTool(Acquisition.Implicit):
    def __init__(self, result):
        self.result=result
    def getInfoFor(self, obj, var):
        self.params=(obj,var)
        return self.result


class DeprecationTests(unittest.TestCase):
    def testMissingWorkflowTool(self):
        adapter=WorkflowDeprecatable(Mock())
        self.assertEqual(adapter.deprecated, False)

    def testObjectWithoutWorkflow(self):
        root=Mock()
        root.portal_workflow=MockWorkflowTool(None)
        root.obj=Mock()
        adapter=WorkflowDeprecatable(root.obj)
        self.assertEqual(adapter.deprecated, False)
        self.assertEqual(root.portal_workflow.params, (root.obj, "review_state"))

    def testPublishedObject(self):
        root=Mock()
        root.portal_workflow=MockWorkflowTool("published")
        root.obj=Mock()
        adapter=WorkflowDeprecatable(root.obj)
        self.assertEqual(adapter.deprecated, False)

    def testDeprecatedObject(self):
        root=Mock()
        root.portal_workflow=MockWorkflowTool("deprecated")
        root.obj=Mock()
        adapter=WorkflowDeprecatable(root.obj)
        self.assertEqual(adapter.deprecated, True)



class MockContainer(dict):
    def __init__(self, **kwargs):
        for (key,value) in kwargs.items():
            setattr(self, key, value)


class ObjectPublishedTests(unittest.TestCase):
    def testNoPublishedFlag(self):
        survey=Mock()
        ObjectPublished(survey, None)
        self.assertEqual(survey.published, True)

    def testPublishedFlagPresenet(self):
        survey=Mock()
        survey.published=False
        ObjectPublished(survey, None)
        self.assertEqual(survey.published, True)


class SurveyDepthConstructionFilterTests(unittest.TestCase):
    def makeSurvey(self):
        from euphorie.content.survey import ISurvey
        container=Mock()
        alsoProvides(container, ISurvey)
        return container

    def testNotInSurvey(self):
        container=Mock()
        for i in range(5):
            container=container.__of__(Mock())

        filter=SurveyDepthConstructionFilter(None, container)
        self.assertEqual(filter.allowed(), True)

    def testSurveyDirectChild(self):
        container=self.makeSurvey()
        filter=SurveyDepthConstructionFilter(None, container)
        self.assertEqual(filter.allowed(), True)

    def testSurveyDepthThree(self):
        container=self.makeSurvey()
        for i in range(2):
            container=Mock().__of__(container)
        filter=SurveyDepthConstructionFilter(None, container)
        self.assertEqual(filter.allowed(), True)

    def testSurveyDepthFour(self):
        container=self.makeSurvey()
        for i in range(3):
            container=Mock().__of__(container)
        filter=SurveyDepthConstructionFilter(None, container)
        self.assertEqual(filter.allowed(), False)


class RichDescriptionTests(unittest.TestCase):
    def testMissing(self):
        self.assertEqual(Description(object())(), u"")

    def testEmpty(self):
        obj=Mock()
        obj.description=u""
        self.assertEqual(Description(obj)(), u"")

    def testSimpleText(self):
        obj=Mock()
        obj.description=u"Test"
        self.assertEqual(Description(obj)(), u"Test")

    def testMarkup(self):
        obj=Mock()
        obj.description=u"Test <em>me</me> <strong>now</strong>"
        self.assertEqual(Description(obj)(), u"Test me now")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
