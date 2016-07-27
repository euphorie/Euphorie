from five import grok
from htmllaundry.z3cform import HtmlText
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from euphorie.content.behaviour.richdescription import IRichDescription
from .. import MessageFactory as _
from euphorie.content.utils import StripMarkup
from plone.indexer import indexer

grok.templatedir("templates")


class IPage(form.Schema, IRichDescription, IBasic):
    """A basic page.
    """
    description = HtmlText(
            title=_("label_module_description", u"Description"),
            description=_("help_module_description",
                default=u"Include any relevant information that may be "
                    u"helpful for the end-user."),
            required=True)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    body = HtmlText(
            title=_("label_body", u"Page content"),
            required=True)
    form.widget(body=WysiwygFieldWidget)


@indexer(IPage)
def SearchableTextIndexer(obj):
    return " ".join([obj.title,
                     StripMarkup(obj.description),
                     StripMarkup(obj.body)])


class View(grok.View):
    grok.context(IPage)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("page_view")
    grok.name("nuplone-view")
