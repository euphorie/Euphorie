from euphorie.content.utils import getTermTitleByToken
from euphorie.content.utils import getTermTitleByValue
from euphorie.content.utils import StripMarkup
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import unittest


class StripMarkupTests(unittest.TestCase):
    def StripMarkup(self, *a, **kw):
        return StripMarkup(*a, **kw)

    def testEmpty(self):
        obj = Mock()
        obj.description = ""
        self.assertEqual(self.StripMarkup(""), "")

    def testNoMarkup(self):
        self.assertEqual(self.StripMarkup("Test"), "Test")

    def testSingleTag(self):
        self.assertEqual(self.StripMarkup("Test <em>me</me>"), "Test me")

    def testMultipleTags(self):
        self.assertEqual(
            self.StripMarkup("Test <em>me</me> <strong>now</strong>"), "Test me now"
        )

    def testStrayBracket(self):
        self.assertEqual(self.StripMarkup("Test <em>me</em> >"), "Test me >")


class getTermTitleByValueTests(unittest.TestCase):
    def getTermTitleByValue(self, *a, **kw):
        return getTermTitleByValue(*a, **kw)

    def testUnknownValue(self):
        self.assertEqual(self.getTermTitleByValue(make_field([]), "dummy"), "dummy")

    def testKnownValue(self):
        field = make_field([(1, "token", "Title")])
        self.assertEqual(self.getTermTitleByValue(field, 1), "Title")


class TestGetTermTitleByToken(unittest.TestCase):
    def testUnknownToken(self):
        self.assertEqual(getTermTitleByToken(make_field([]), "dummy"), "dummy")

    def testKnownToken(self):
        field = make_field([(1, "token", "Title")])
        self.assertEqual(getTermTitleByToken(field, "token"), "Title")


class Mock:
    pass


def make_field(terms):
    terms = [SimpleTerm(value, token, title=title) for (value, token, title) in terms]
    field = Mock()
    field.vocabulary = SimpleVocabulary(terms)
    return field
