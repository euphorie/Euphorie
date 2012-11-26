import unittest


class StripMarkupTests(unittest.TestCase):
    def StripMarkup(self, *a, **kw):
        from euphorie.content.utils import StripMarkup
        return StripMarkup(*a, **kw)

    def testEmpty(self):
        obj = Mock()
        obj.description = u""
        self.assertEqual(self.StripMarkup(u""), u"")

    def testNoMarkup(self):
        self.assertEqual(self.StripMarkup(u"Test"), u"Test")

    def testSingleTag(self):
        self.assertEqual(self.StripMarkup(u"Test <em>me</me>"), u"Test me")

    def testMultipleTags(self):
        self.assertEqual(
                self.StripMarkup(u"Test <em>me</me> <strong>now</strong>"),
                u"Test me now")

    def testStrayBracket(self):
        self.assertEqual(
                self.StripMarkup(u"Test <em>me</em> >"),
                u"Test me >")


class getTermTitleByValueTests(unittest.TestCase):
    def getTermTitleByValue(self, *a, **kw):
        from euphorie.content.utils import getTermTitleByValue
        return getTermTitleByValue(*a, **kw)

    def testUnknownValue(self):
        self.assertEqual(
                self.getTermTitleByValue(make_field([]), "dummy"),
                "dummy")

    def testKnownValue(self):
        field = make_field([(1, "token", u"Title")])
        self.assertEqual(self.getTermTitleByValue(field, 1), u"Title")


class getTermTitleByToken(unittest.TestCase):
    def getTermTitleByToken(self, *a, **kw):
        from euphorie.content.utils import getTermTitleByToken
        return getTermTitleByToken(*a, **kw)

    def testUnknownToken(self):
        self.assertEqual(
                self.getTermTitleByToken(make_field([]), "dummy"),
                "dummy")

    def testKnownToken(self):
        field = make_field([(1, "token", u"Title")])
        self.assertEqual(self.getTermTitleByToken(field, "token"), u"Title")


class Mock:
    pass


def make_field(terms):
    from zope.schema.vocabulary import SimpleVocabulary
    from zope.schema.vocabulary import SimpleTerm
    terms = [SimpleTerm(value, token, title=title)
             for (value, token, title) in terms]
    field = Mock()
    field.vocabulary = SimpleVocabulary(terms)
    return field
