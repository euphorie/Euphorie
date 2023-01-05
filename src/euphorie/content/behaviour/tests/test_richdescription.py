from euphorie.content.behaviour.richdescription import Description

import unittest


class Mock:
    pass


class RichDescriptionTests(unittest.TestCase):
    def testMissing(self):
        self.assertEqual(Description(object())(), "")

    def testEmpty(self):
        obj = Mock()
        obj.description = ""
        self.assertEqual(Description(obj)(), "")

    def testSimpleText(self):
        obj = Mock()
        obj.description = "Test"
        self.assertEqual(Description(obj)(), "Test")

    def testMarkup(self):
        obj = Mock()
        obj.description = "Test <em>me</me> <strong>now</strong>"
        self.assertEqual(Description(obj)(), "Test me now")
