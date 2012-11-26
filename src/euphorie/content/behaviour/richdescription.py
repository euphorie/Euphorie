"""
Rich description
----------------

Several content types in euphorie use a rich text description. This
requires a little bit of special interaction for Plone, which is implemented
in this behaviour.

Enabling this behaviour for a content type does two things: it replaces
the standard description field with a rich text version, and registers
a catalog indexer which returns a plain text version of the description.
"""

import HTMLParser
from zope import schema
from plone.indexer import indexer
from plone.directives import form
from euphorie.content import MessageFactory as _
from euphorie.content.utils import StripMarkup
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget


class IRichDescription(form.Schema):
    """Simple behaviour for content types with a HTML description.
    Replaces the standard description field with a rich text version.
    """
    description = schema.Text(
            title=_(u"Summary"),
            description=_(u'A short summary of the content.'),
            required=False)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")


@indexer(IRichDescription)
def Description(obj):
    """Indexer for rich text descriptions fields. Return a plain text
    version of the description for use in the Plone catalog.
    """
    d = getattr(obj, "description", u"")
    if d is None:
        return None

    h = HTMLParser.HTMLParser()
    return h.unescape(StripMarkup(d))
