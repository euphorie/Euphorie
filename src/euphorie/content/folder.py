from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from five import grok
from plonetheme.nuplone.skin.interfaces import NuPloneSkin

grok.templatedir("templates")


class IFolder(form.Schema, IBasic):
    pass


class View(grok.View):
    grok.context(IFolder)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("folder_view")
