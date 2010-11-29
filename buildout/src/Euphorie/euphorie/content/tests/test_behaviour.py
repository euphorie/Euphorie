import unittest
import Acquisition
from zope.interface import alsoProvides
from zope.annotation.interfaces import IAttributeAnnotatable
from euphorie.content.behaviour.uniqueid import UniqueNameChooser
from euphorie.content.behaviour.uniqueid import IIdGenerationRoot
from euphorie.content.behaviour.uniqueid import INameFromUniqueId
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



class MockContainer(dict):
    def __init__(self, **kwargs):
        for (key,value) in kwargs.items():
            setattr(self, key, value)


class HandleWorkflowTransitionTests(unittest.TestCase):
    def handleWorklowTransition(self, obj, event):
        from euphorie.content.behaviour.publish import handleWorklowTransition
        handleWorklowTransition(obj, event)

    def testPublishTransitionNoFlagPresent(self):
        survey=Mock()
        event=Mock()
        event.action="publish"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, True)

    def testPublishTransitionFlagPresent(self):
        survey=Mock()
        survey.published=False
        event=Mock()
        event.action="publish"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, True)

    def testDoNothingOnOtherTransition(self):
        survey=Mock()
        survey.published=False
        event=Mock()
        event.action="update"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, False)

    def testRetract(self):
        survey=Mock()
        survey.published=True
        event=Mock()
        event.action="retract"
        self.handleWorklowTransition(survey, event)
        self.assertEqual(survey.published, False)



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
