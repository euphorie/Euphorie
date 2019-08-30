"""
Layout
------

Serves several helper templates, and the basic shell.pt that glues everything
together.
"""

from zope.interface import Interface
from five import grok
from euphorie.client.interfaces import IClientSkinLayer

grok.templatedir("templates")


class Shell(grok.View):
    """ Based on the _layouts/shell.html layout in Jekyll. In Plone terms it's
        similar to the main_template.pt.
    """
    grok.context(Interface)
    grok.name("shell")
    grok.layer(IClientSkinLayer)
    grok.template("shell")


class Plain(grok.View):
    """ Based on the shell template, but stripped down to a minimum (no
        sidebar, no header). Meant for use in things like pdf reports.
    """
    grok.context(Interface)
    grok.name("plain")
    grok.layer(IClientSkinLayer)
    grok.template("plain")


class Layout(grok.View):
    grok.context(Interface)
    grok.name("layout")
    grok.layer(IClientSkinLayer)
    grok.template("layout")


class Includes(grok.View):
    """ This view's templates contains a collection of macros, corresponding to
        the Jekyll includes under the _includes dir.
    """
    grok.context(Interface)
    grok.name("includes")
    grok.layer(IClientSkinLayer)
    grok.template("includes")


class Tooltips(grok.View):
    """ This view's templates contains a number of <div> element that are used
    for various tooltips.
    In proto, see explanations.html

    """
    grok.context(Interface)
    grok.name("tooltips")
    grok.layer(IClientSkinLayer)
    grok.template("tooltips")
