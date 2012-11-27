from zope.interface import Interface
from five import grok
from euphorie.client.interfaces import IClientSkinLayer

grok.templatedir("templates")


class Layout(grok.View):
    grok.context(Interface)
    grok.name("layout")
    grok.layer(IClientSkinLayer)
    grok.template("layout")
