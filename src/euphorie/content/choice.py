from .behaviour.richdescription import IRichDescription
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.supermodel import model


class IChoice(model.Schema, IRichDescription, IBasic):
    """ """
