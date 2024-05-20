import unittest


class Mock:
    pass


class strip_markup_tests(unittest.TestCase):
    def strip_markup(self, *a, **kw):
        from euphorie.htmllaundry.utils import strip_markup

        return strip_markup(*a, **kw)

    def testEmpty(self):
        obj = Mock()
        obj.description = ""
        self.assertEqual(self.strip_markup(""), "")

    def testNoMarkup(self):
        self.assertEqual(self.strip_markup("Test"), "Test")

    def testSingleTag(self):
        self.assertEqual(self.strip_markup("Test <em>me</me>"), "Test me")

    def testMultipleTags(self):
        self.assertEqual(
            self.strip_markup("Test <em>me</me> <strong>now</strong>"), "Test me now"
        )

    def testStrayBracket(self):
        self.assertEqual(self.strip_markup("Test <em>me</em> >"), "Test me >")


class remove_empty_tags_tests(unittest.TestCase):
    def _remove(self, str, extra_tags=[]):
        from euphorie.htmllaundry.utils import remove_empty_tags

        import lxml.etree

        fragment = lxml.etree.fromstring(str)
        fragment = remove_empty_tags(fragment, extra_tags)
        return lxml.etree.tostring(fragment, encoding="utf8").decode()

    def testRemoveEmptyParagraphElement(self):
        self.assertEqual(self._remove("<div><p/></div>"), "<div/>")

    def testRemoveEmptyParagraph(self):
        self.assertEqual(self._remove("<div><p></p></div>"), "<div/>")

    def testRemoveParagraphWithWhitespace(self):
        self.assertEqual(self._remove("<div><p>  </p></div>"), "<div/>")

    def testRemoveParagraphWithUnicodeWhitespace(self):
        self.assertEqual(self._remove("<div><p> \xa0 </p></div>"), "<div/>")

    def testKeepEmptyImageElement(self):
        self.assertEqual(
            self._remove('<div><img src="image"/></div>'),
            '<div><img src="image"/></div>',
        )

    def testCollapseBreaks(self):
        self.assertEqual(
            self._remove("<body><p>one<br/><br/>two</p></body>"),
            "<body><p>one<br/>two</p></body>",
        )

    def testNestedData(self):
        self.assertEqual(
            self._remove("<div><h3><bad/></h3><p>Test</p></div>"),
            "<div><p>Test</p></div>",
        )

    def testKeepElementsWithTail(self):
        self.assertEqual(
            self._remove("<body>One<br/> two<br/> three</body>"),
            "<body>One<br/> two<br/> three</body>",
        )

    def testTrailingBreak(self):
        self.assertEqual(self._remove("<div>Test <br/></div>"), "<div>Test </div>")

    def testLeadingBreak(self):
        self.assertEqual(self._remove("<div><br/>Test</div>"), "<div>Test</div>")

    def testDoNotRemoveEmptyAnchorElement(self):
        # Should not remove empty <a> tag because it's used as an anchor:
        self.assertEqual(
            self._remove('<p><a id="anchor"></a></p>'), '<p><a id="anchor"/></p>'
        )
        self.assertEqual(
            self._remove('<p><a name="anchor" /></p>'), '<p><a name="anchor"/></p>'
        )
        self.assertEqual(
            self._remove('<p><a href="blah" id="anchor"/></p>'),
            '<p><a href="blah" id="anchor"/></p>',
        )
        self.assertEqual(
            self._remove('<p><a href="blah" name="anchor"/></p>'),
            '<p><a href="blah" name="anchor"/></p>',
        )

        # Should not remove <a> tag because it's non-empty:
        self.assertEqual(
            self._remove('<p><a href="blah" name="anchor">Link</a></p>'),
            '<p><a href="blah" name="anchor">Link</a></p>',
        )
        self.assertEqual(
            self._remove('<p><a name="anchor">Link</a></p>'),
            '<p><a name="anchor">Link</a></p>',
        )
        self.assertEqual(
            self._remove('<p><a href="anchor">Link</a></p>'),
            '<p><a href="anchor">Link</a></p>',
        )

        # Should remove because it's an useless empty tag.
        self.assertEqual(
            self._remove('<p><a href="blah"/>Content</p>'), "<p>Content</p>"
        )
        self.assertEqual(
            self._remove('<p><a href="blah"></a>Content</p>'), "<p>Content</p>"
        )

    def testExtraAllowedEmptyTags(self):
        self.assertEqual(
            self._remove("<table><tr><td>Test</td><td></td></tr></table>", ["td"]),
            "<table><tr><td>Test</td><td/></tr></table>",
        )


class ForceLinkTargetTests(unittest.TestCase):
    def force_link_target(self, str, target="_blank"):
        from euphorie.htmllaundry.cleaners import LaundryCleaner

        import lxml.etree

        fragment = lxml.etree.fromstring(str)
        cleaner = LaundryCleaner()
        cleaner.force_link_target(fragment, target)
        return lxml.etree.tostring(fragment, encoding="utf8").decode()

    def testNoAnchor(self):
        self.assertEqual(self.force_link_target("<div><p/></div>"), "<div><p/></div>")

    def testAddTarget(self):
        self.assertEqual(
            self.force_link_target(
                '<div><a href="http://example.com"/></div>', "_blank"
            ),
            '<div><a href="http://example.com" target="_blank"/></div>',
        )

    def testRemoveTarget(self):
        self.assertEqual(
            self.force_link_target(
                '<div><a target="_blank" href="http://example.com"/></div>', None
            ),
            '<div><a href="http://example.com"/></div>',
        )


class strip_outer_breaks_tests(unittest.TestCase):
    def _strip(self, str):
        from euphorie.htmllaundry.utils import strip_outer_breaks

        import lxml.etree

        fragment = lxml.etree.fromstring(str)
        strip_outer_breaks(fragment)
        return lxml.etree.tostring(fragment, encoding="utf8").decode()

    def testNoBreak(self):
        self.assertEqual(
            self._strip("<body>Dummy text</body>"), "<body>Dummy text</body>"
        )

    def testTrailingBreak(self):
        self.assertEqual(
            self._strip("<body>Dummy text<br/></body>"), "<body>Dummy text</body>"
        )

    def testLeadingBreak(self):
        self.assertEqual(
            self._strip("<body><br/>Dummy text</body>"), "<body>Dummy text</body>"
        )

    def testBreakAfterElement(self):
        self.assertEqual(
            self._strip("<body><p>Dummy</p><br/>text</body>"),
            "<body><p>Dummy</p>text</body>",
        )


class SanizeTests(unittest.TestCase):
    def sanitize(self, *a, **kw):
        from euphorie.htmllaundry.utils import sanitize

        return sanitize(*a, **kw)

    def testEmpty(self):
        self.assertEqual(self.sanitize(""), "")

    def testParagraph(self):
        self.assertEqual(self.sanitize("<p>Test</p>"), "<p>Test</p>")

    def test_link_in_unwrapped_text(self):
        self.assertEqual(
            self.sanitize('There is a <a href="#">link</a> in here.'),
            '<p>There is a <a href="#">link</a> in here.</p>',
        )

    def testParagraphCustomWrapperNotUsedIfAlreadyWrapped(self):
        self.assertEqual(self.sanitize("<p>Test</p>", wrap="span"), "<p>Test</p>")

    def testParagraphWithWhitespace(self):
        self.assertEqual(self.sanitize("<p>Test</p>\n<p>\xa0</p>\n"), "<p>Test</p>\n\n")

    def testLeadingBreak(self):
        self.assertEqual(self.sanitize("<br/><p>Test</p>"), "<p>Test</p>")

    def testHeaderAndText(self):
        self.assertEqual(
            self.sanitize("<h3>Title</h3><p>Test</p>"), "<h3>Title</h3><p>Test</p>"
        )

    def testUnwrappedText(self):
        self.assertEqual(self.sanitize("Hello, World"), "<p>Hello, World</p>")

    def testUnwrappedTextWithCustomWrapper(self):
        self.assertEqual(
            self.sanitize("Hello, World", wrap="strong"),
            "<strong>Hello, World</strong>",
        )

    def testTrailingUnwrappedText(self):
        self.assertEqual(
            self.sanitize("<p>Hello,</p> World"), "<p>Hello,</p><p> World</p>"
        )

    def testTrailingUnwrappedTextWithCustomWrapper(self):
        self.assertEqual(
            self.sanitize("<p>Hello,</p> World", wrap="b"), "<p>Hello,</p><b> World</b>"
        )

    def testUnwrappedTextEverywhere(self):
        self.assertEqual(
            self.sanitize(
                "Hello, <p>you</p> nice and <strong>decent</strong> <em>person</em>."
            ),
            "<p>Hello, </p><p>you</p><p> nice and <strong>decent</strong> "
            + "<em>person</em>.</p>",
        )

    def testUnwrappedTextEverywhereWithCustomWrapper(self):
        self.assertEqual(
            self.sanitize("Hello, <p>you</p> nice <em>person</em>.", wrap="div"),
            "<div>Hello, </div><p>you</p><div> nice " + "<em>person</em>.</div>",
        )

    def testStripStyleAttributes(self):
        self.assertEqual(
            self.sanitize('<p style="text-weight: bold">Hello</p>'), "<p>Hello</p>"
        )

    def testJavascriptLink(self):
        self.assertEqual(
            self.sanitize(
                "<p><a href=\"javascript:alert('I am evil')\">" + "click me</a></p>"
            ),
            '<p><a href="">click me</a></p>',
        )

    def testSkipWrapping(self):
        self.assertEqual(
            self.sanitize("Hello, <em>you</em> nice <em>person</em>.", wrap=None),
            "Hello, <em>you</em> nice <em>person</em>.",
        )

    def testRejectBadWrapElement(self):
        self.assertRaises(ValueError, self.sanitize, "<p>Hello,</p> World", wrap="xxx")
        self.assertRaises(
            ValueError,
            self.sanitize,
            "Hello, <em>you</em> nice <em>person</em>.",
            wrap="",
        )
