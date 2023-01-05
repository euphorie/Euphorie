from euphorie.content.behaviour.uniqueid import IIdGenerationRoot
from euphorie.content.behaviour.uniqueid import INameFromUniqueId
from euphorie.content.behaviour.uniqueid import UniqueNameChooser
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component.testing import PlacelessSetup
from zope.interface import alsoProvides
from zope.interface import implementer

import Acquisition
import unittest


@implementer(INameFromUniqueId)
class Mock(Acquisition.Implicit):
    pass


class IdGenerationTests(PlacelessSetup, unittest.TestCase):
    def setUp(self):
        super().setUp()
        from zope.annotation.attribute import AttributeAnnotations
        from zope.component import provideAdapter

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
