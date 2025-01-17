"""
Sector Container
----------------

A Sector Container provides the overview of all countries.

https://admin.oiraproject.eu/sectors
"""

from euphorie.content.behaviour.richdescription import IRichDescription
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ISectorContainer(model.Schema, IRichDescription, IBasic):
    """Container for all sectors."""


@implementer(ISectorContainer)
class SectorContainer(Container):
    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False
