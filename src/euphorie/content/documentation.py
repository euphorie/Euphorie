from five import grok
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from euphorie.content.interfaces import IEuphorieContentSkinLayer

grok.templatedir("templates")


class IDocumentationFolder(form.Schema, IBasic):
    """A folder for all documentation for a specific language
    """


class View(grok.View):
    grok.context(IDocumentationFolder)
    grok.require("zope2.View")
    grok.layer(IEuphorieContentSkinLayer)
    grok.template("documentation_view")
    grok.name("nuplone-view")
