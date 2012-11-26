import unittest
import Acquisition
from zope.component.testing import PlacelessSetup
from zope.interface import alsoProvides
from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable
from euphorie.content.behaviour.uniqueid import INameFromUniqueId
from euphorie.content.behaviour.uniqueid import UniqueNameChooser
from euphorie.content.behaviour.uniqueid import IIdGenerationRoot


class Mock(Acquisition.Implicit):
    implements(INameFromUniqueId)


class IdGenerationTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        super(IdGenerationTests, self).setUp()
        from zope.component import provideAdapter
        from zope.annotation.attribute import AttributeAnnotations
        provideAdapter(AttributeAnnotations)

    def makeRoot(self):
        root = Mock()
        alsoProvides(root, IAttributeAnnotatable, IIdGenerationRoot)
        return root

    def test_ValueErrorIfNoRoot(self):
        chooser = UniqueNameChooser(Mock())
        self.assertRaises(ValueError, chooser.chooseName, None, Mock())

    def testValueErrorIfRootNotAnnotatable(self):
        root = Mock()
        alsoProvides(root, IIdGenerationRoot)
        chooser = UniqueNameChooser(root)
        self.assertRaises(ValueError, chooser.chooseName, None, Mock())

    def testFirstIdIsOne(self):
        root = self.makeRoot()
        obj = Mock()
        UniqueNameChooser(root).chooseName(None, obj)
        self.assertEqual(obj.id, "1")

    def testSecondIdIsTwo(self):
        root = self.makeRoot()
        obj = Mock()
        chooser = UniqueNameChooser(root)
        chooser.chooseName(None, obj)
        del obj.id
        chooser.chooseName(None, obj)
        self.assertEqual(obj.id, "2")

    def testUseExitingIdIfPresent(self):
        root = self.makeRoot()
        obj = Mock()
        obj.id = "mock"
        UniqueNameChooser(root).chooseName(None, obj)
        self.assertEqual(obj.id, "mock")

    def testExtraDepth(self):
        root = self.makeRoot()
        folder = Mock().__of__(root)
        obj = Mock()
        UniqueNameChooser(folder).chooseName(None, obj)
        self.assertEqual(obj.id, "1")
