"""
Documentation
-------------

A folder that contains documentation for a language.

https://admin.oiraproject.eu/documents/en

portal_type: euphorie.documentation
"""

from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import form


class IDocumentationFolder(form.Schema, IBasic):
    """A folder for all documentation for a specific language
    """
