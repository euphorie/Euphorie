"""
Sector Container
----------------

A Sector Container provides the overview of all countries.

https://admin.oiraproject.eu/sectors
"""
from euphorie.content.behaviour.richdescription import IRichDescription
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from zope.interface import implements


class ISectorContainer(form.Schema, IRichDescription, IBasic):
    """Container for all sectors."""


class SectorContainer(dexterity.Container):
    implements(ISectorContainer)

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False
