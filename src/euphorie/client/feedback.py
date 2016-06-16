from zope.interface import Interface
from five import grok
from euphorie.client.interfaces import IClientSkinLayer

grok.templatedir("templates")


class UserMenu(grok.View):
    grok.context(Interface)
    grok.name("user-menu.html")
    grok.layer(IClientSkinLayer)
    grok.template("user-menu")
