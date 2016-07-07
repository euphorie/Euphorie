from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from five import grok
from euphorie.content.interfaces import IEuphorieContentSkinLayer

grok.templatedir("templates")


class IFolder(form.Schema, IBasic):
    pass


class View(grok.View):
    grok.context(IFolder)
    grok.require("zope2.View")
    grok.layer(IEuphorieContentSkinLayer)
    grok.name("nuplone-view")
    grok.template("folder_view")
