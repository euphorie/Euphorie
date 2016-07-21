"""
Documentation
-------------

A folder that contains documentation for a language.

https://admin.oiraproject.eu/documents/en

portal_type: euphorie.documentation
"""

from five import grok
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from plonetheme.nuplone.skin.interfaces import NuPloneSkin

grok.templatedir("templates")


class IDocumentationFolder(form.Schema, IBasic):
    """A folder for all documentation for a specific language
    """


class View(grok.View):
    """ View name: @@nuplone-view
    """
    grok.context(IDocumentationFolder)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("documentation_view")
    grok.name("nuplone-view")
