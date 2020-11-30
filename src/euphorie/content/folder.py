from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import form


class IFolder(form.Schema, IBasic):
    pass
