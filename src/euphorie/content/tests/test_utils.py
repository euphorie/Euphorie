from euphorie.content.utils import getTermTitleByToken
from euphorie.content.utils import getTermTitleByValue
from euphorie.content.utils import parse_scaled_answers
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


class TestParseScaledAnswers(unittest.TestCase):
    def testEmpty(self):
        self.assertEqual(parse_scaled_answers(""), [])

    def testSimple(self):
        self.assertEqual(
            parse_scaled_answers("a\nb"),
            [{"text": "a", "value": "1"}, {"text": "b", "value": "2"}],
        )
        self.assertEqual(
            parse_scaled_answers("a\nb\nc\nd\ne\nf"),
            [
                {"text": "a", "value": "1"},
                {"text": "b", "value": "2"},
                {"text": "c", "value": "3"},
                {"text": "d", "value": "4"},
                {"text": "e", "value": "5"},
                {"text": "f", "value": "6"},
            ],
        )

    def testExtended(self):
        self.assertEqual(
            parse_scaled_answers("a|7\nb|3"),
            [{"text": "a", "value": "7"}, {"text": "b", "value": "3"}],
        )

    def testMixed(self):
        self.assertEqual(
            parse_scaled_answers("a|7\nb"),
            [{"text": "a", "value": "7"}, {"text": "b", "value": "2"}],
        )
        self.assertEqual(
            parse_scaled_answers("a\nb|42"),
            [{"text": "a", "value": "1"}, {"text": "b", "value": "42"}],
        )

    def testUgly(self):
        self.assertEqual(
            parse_scaled_answers("\n\n hello world |  7\n\n\n  b  \n\n\nc|\n\n\n"),
            [
                {"text": "hello world", "value": "7"},
                {"text": "b", "value": "2"},
                {"text": "c", "value": "3"},
            ],
        )
        # If you really want, an answer can contain a literal pipe.
        self.assertEqual(
            parse_scaled_answers("a|b|7"),
            [{"text": "a|b", "value": "7"}],
        )
        self.assertEqual(
            parse_scaled_answers("a||7"),
            [{"text": "a|", "value": "7"}],
        )


class Mock:
    pass


def make_field(terms):
    terms = [SimpleTerm(value, token, title=title) for (value, token, title) in terms]
    field = Mock()
    field.vocabulary = SimpleVocabulary(terms)
    return field
