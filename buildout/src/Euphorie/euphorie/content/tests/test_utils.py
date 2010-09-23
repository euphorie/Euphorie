import unittest
from euphorie.content.utils import StripMarkup

class Mock:
    pass

class StripMarkupTests(unittest.TestCase):
    def testEmpty(self):
        obj=Mock()
        obj.description=u""
        self.assertEqual(StripMarkup(u""), u"")

    def testNoMarkup(self):
        self.assertEqual(StripMarkup(u"Test"), u"Test")

    def testSingleTag(self):
        self.assertEqual(StripMarkup(u"Test <em>me</me>"), u"Test me")

    def testMultipleTags(self):
        self.assertEqual(StripMarkup(u"Test <em>me</me> <strong>now</strong>"),
                         u"Test me now")

    def testStrayBracket(self):
        self.assertEqual(StripMarkup(u"Test <em>me</em> >") , u"Test me >")
