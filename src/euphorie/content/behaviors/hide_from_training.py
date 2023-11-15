from .. import MessageFactory as _
from plone.autoform.directives import order_after
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IHideFromTraining(model.Schema):
    hide_from_training = schema.Bool(
        title=_("label_hide_from_training", default="Hide from training"),
        description=_(
            "help_hide_from_training",
            default="Do not include this module in the training, for example "
            "if the module does not have any relevance for workers.",
        ),
        required=False,
        default=False,
    )
    order_after(hide_from_training="question")
