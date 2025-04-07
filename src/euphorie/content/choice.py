from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.supermodel import model
from zope import schema


class IChoice(model.Schema, IRichDescription, IBasic):
    """ """

    allow_multiple_options = schema.Bool(
        title=_(
            "label_allow_multiple_options", default="Allow multiple options"
        ),
        description=_(
            "help_allow_multiple_options",
            default="If active, checkboxes are shown to allow selecting more than one "
            "option. Otherwise, radio buttons are used to force a single selection.",
        ),
        default=True,
    )
