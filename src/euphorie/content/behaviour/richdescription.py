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

from euphorie.content import MessageFactory as _
from euphorie.content.utils import StripMarkup
from plone.autoform import directives
from plone.indexer import indexer
from plone.supermodel import model
from plonetheme.nuplone.z3cform.widget import WysiwygFieldWidget
from zope import schema


try:
    from html import unescape
except ImportError:
    # PY2
    import HTMLParser

    unescape = HTMLParser.HTMLParser().unescape


class IRichDescription(model.Schema):
    """Simple behaviour for content types with a HTML description.

    Replaces the standard description field with a rich text version.
    """

    description = schema.Text(
        title=_("Summary"),
        description=_("A short summary of the content."),
        required=False,
    )
    directives.widget(description=WysiwygFieldWidget)
    directives.order_after(description="title")


@indexer(IRichDescription)
def Description(obj):
    """Indexer for rich text descriptions fields.

    Return a plain text version of the description for use in the Plone
    catalog.
    """
    d = getattr(obj, "description", "")
    if d is None:
        return None

    return unescape(StripMarkup(d))
