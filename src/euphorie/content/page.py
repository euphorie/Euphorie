# coding=utf-8
from .. import MessageFactory as _
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content.utils import StripMarkup
from htmllaundry.z3cform import HtmlText
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.directives import form
from plone.indexer import indexer


class IPage(form.Schema, IRichDescription, IBasic):
    """A basic page."""

    description = HtmlText(
        title=_("label_module_description", u"Description"),
        description=_(
            "help_module_description",
            default=u"Include any relevant information that may be "
            u"helpful for the end-user.",
        ),
        required=True,
    )
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    body = HtmlText(title=_("label_body", u"Page content"), required=True)
    form.widget(body=WysiwygFieldWidget)


@indexer(IPage)
def SearchableTextIndexer(obj):
    return " ".join([obj.title, StripMarkup(obj.description), StripMarkup(obj.body)])
