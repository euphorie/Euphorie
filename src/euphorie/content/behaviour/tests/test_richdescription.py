import unittest
from euphorie.content.behaviour.richdescription import Description


class Mock(object):
    pass


class RichDescriptionTests(unittest.TestCase):
    def testMissing(self):
        self.assertEqual(Description(object())(), u"")

    def testEmpty(self):
        obj = Mock()
        obj.description = u""
        self.assertEqual(Description(obj)(), u"")

    def testSimpleText(self):
        obj = Mock()
        obj.description = u"Test"
        self.assertEqual(Description(obj)(), u"Test")

    def testMarkup(self):
        obj = Mock()
        obj.description = u"Test <em>me</me> <strong>now</strong>"
        self.assertEqual(Description(obj)(), u"Test me now")
