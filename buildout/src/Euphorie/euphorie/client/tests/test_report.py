import unittest
from euphorie.content.risk import Risk
from euphorie.client import model

class ShowNegateWarningTests(unittest.TestCase):
    def _call(self, node, zodbnode):
        from euphorie.client.report import IdentificationReport
        report=IdentificationReport(None, None)
        return report.show_negate_warning(node, zodbnode)

    def test_show_Unanswered(self):
        # https//code.simplon.biz/tracker/tno-euphorie/ticket/75
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_RiskNotPresent(self):
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk", identification="yes")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_RiskNotApplicable(self):
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk", identification="n/a")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_Present(self):
        zodbnode=Risk()
        zodbnode.problem_description=None
        node=model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), True)

    def test_HasProblemDescription(self):
        zodbnode=Risk()
        zodbnode.problem_description=u"Negative"
        node=model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), False)

    def test_HasEmptyProblemDescription(self):
        zodbnode=Risk()
        zodbnode.problem_description=u"   "
        node=model.Risk(type="risk", identification="no")
        self.assertEqual(self._call(node, zodbnode), True)


class HtmlToRtfTests(unittest.TestCase):
    def HtmlToRtf(self, *a, **kw):
        from euphorie.client.report import HtmlToRtf
        return HtmlToRtf(*a, **kw)

    def render(self, output):
        from cStringIO import StringIO
        from rtfng.Elements import Document
        from rtfng.document.section import Section
        from rtfng.Renderer import Renderer
        document=Document()
        section=Section()
        section.append(*output)
        document.Sections.append(section)
        renderer=Renderer()
        renderer.Write(document, StringIO()) # Setup instance variables
        renderer._doc=document
        renderer._fout=StringIO()
        renderer._CurrentStyle = ""
        renderer._WriteSection(section, True, False)
        return renderer._fout.getvalue()

    def testEmptyInput(self):
        self.assertEqual(self.HtmlToRtf(u"", u"<stylesheet>"), [])

    def testInvalidHtmlFallback(self):
        self.assertTrue(
                "text\\par" in 
                self.render(self.HtmlToRtf(u"<p>text</p>", u"<stylesheet>")))

    def testBasicParagraph(self):
        self.assertTrue(
                "Simple text\\par" in 
                self.render(self.HtmlToRtf(u"<p>Simple text</p>", u"<stylesheet>")), [])

    def testItalicInText(self):
        self.assertTrue(
                "Simple {\\i text}\\par" in 
                self.render(self.HtmlToRtf(u"<p>Simple <em>text</em></p>", u"<stylesheet>")))

    def testBoldAndItalicText(self):
        self.assertTrue(
                "Very {\\i very }{\\b\\i bold}\\par" in 
                self.render(self.HtmlToRtf(u"<p>Very <em>very <strong>bold</strong></em></p>", u"<stylesheet>")))

    def testInlineEntity(self):
        self.assertTrue(
                "Simple & clean\\par" in 
                self.render(self.HtmlToRtf(u"<p>Simple &amp; clean</p>", u"<stylesheet>")))

    def testInlineEntityDigit(self):
        self.assertTrue(
                "Simple \r clean\\par" in 
                self.render(self.HtmlToRtf(u"<p>Simple &#13; clean</p>", u"<stylesheet>")))

