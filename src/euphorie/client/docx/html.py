# coding=utf-8
from lxml import etree

import docx
import htmllaundry
import lxml.html


def add_hyperlink(paragraph, url, text, style):
    """
    A function that places a hyperlink within a paragraph object.

    :param paragraph: The paragraph we are adding the hyperlink to.
    :param url: A string containing the required url
    :param text: The text displayed for the url
    :return: The hyperlink object
    """

    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(
        url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True
    )

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement("w:hyperlink")
    hyperlink.set(
        docx.oxml.shared.qn("r:id"),
        r_id,
    )

    # Create a w:r element
    new_run = docx.oxml.shared.OxmlElement("w:r")

    # Create a new w:rPr element
    rPr = docx.oxml.shared.OxmlElement("w:rPr")

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    new_run.style = style
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink


class _HtmlToWord(object):
    def handleInlineText(self, node, p):
        """Handler for elements which can only contain inline text (p, li)"""
        run = p.add_run()
        font = run.font
        if node.tag in ["strong", "b"]:
            font.bold = True
        elif node.tag in ["em", "i"]:
            font.italic = True
        elif node.tag == "u":
            font.underline = True

        if node.text and node.text.strip():
            if node.tag == "a":
                href = node.get("href")
                href = href and href.strip()
                if href and href != node.text.strip():
                    add_hyperlink(p, href, node.text, "Hyperlink")
                else:
                    run.text = node.text
            else:
                run.text = node.text

        for sub in node:
            p = self.handleInlineText(sub, p)
        if node.tail and node.tail.strip():
            run = p.add_run()
            run.text = node.tail
        return p

    def handleElement(self, node, doc, style=None):
        if node.tag in ["p", "li", "strong", "b", "em", "i", "u", "a"]:
            p = doc.add_paragraph(style=style)
            p = self.handleInlineText(node, p)
        elif node.tag in ["ul", "ol"]:

            if node.tag == "ul":
                style = "List Bullet"
            else:
                style = "List Number"
            for sub in node:
                if sub.tag == "li":
                    p = doc.add_paragraph(style=style)
                    p = self.handleInlineText(sub, p)

        tail = node.tail
        # Prevent unwanted empty lines inside listings and paragraphs that come
        # from newlines in the markup
        # if node.tag in ['li', 'p', 'strong', 'em', 'b', 'i']:
        tail = tail and tail.strip()
        if tail:
            doc.add_paragraph(tail)
        return doc

    def __call__(self, markup, doc, style=None):
        if not markup or not markup.strip():
            return doc
        try:
            markup_doc = lxml.html.document_fromstring(markup)
        except etree.XMLSyntaxError:
            text = htmllaundry.StripMarkup(markup)
            text = text.replace("&#13", "\n")
            doc.add_paragraph(text)
            return doc

        for node in markup_doc.find("body"):
            doc = self.handleElement(node, doc, style)

        return doc


HtmlToWord = _HtmlToWord()
