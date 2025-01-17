"""
Profile Question
----------------

A Profile Question is a container for Modules. A question is used to determine
whether or not a Module should be enabled, or whether it should be repeated.

portal_type: euphorie.profilequestion
"""

from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from .behaviour.uniqueid import get_next_id
from .behaviour.uniqueid import INameFromUniqueId
from .fti import check_fti_paste_allowed
from .interfaces import IQuestionContainer
from .module import ConstructionFilter
from .module import item_depth
from .module import tree_depth
from .utils import StripMarkup
from euphorie.content.dependency import ConditionalTextLine
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.supermodel import model
from plonetheme.nuplone.z3cform.directives import depends
from zope import schema
from zope.interface import implementer

import sys


class IProfileQuestion(model.Schema, IRichDescription, IBasic):
    """Survey Profile question.

    A profile question is used to determine if parts of a survey should
    be skipped, or repeated multiple times.
    """

    question = schema.TextLine(
        title=_("label_profilequestion_question", default="Question"),
        description=_(
            "This question must ask the user if this profile " "applies to them."
        ),
        required=True,
    )
    directives.widget(question="euphorie.content.risk.TextLines4Rows")

    use_location_question = schema.Bool(
        title=_(
            "label_use_location_question",
            default="Ask the user about (multiple) locations?",
        ),
        description=_(
            "description_use_location_question",
            default="If this part is active, the user will be asked to "
            "enter the name of all locations for which this module applies. "
            "This means, the module will be repeated as many times as there "
            "are locations. If you do not need this repeatable behaviour, "
            "untick the checkbox to turn it off.",
        ),
        required=False,
        default=True,
    )

    depends("label_multiple_present", "use_location_question", "on")
    label_multiple_present = ConditionalTextLine(
        title=_("Multiple item question"),
        required=True,
        description=_(
            "This question must ask the user if the service is "
            "offered in more than one location."
        ),
    )
    directives.widget(label_multiple_present="euphorie.content.risk.TextLines4Rows")

    depends("label_single_occurance", "use_location_question", "on")
    label_single_occurance = ConditionalTextLine(
        title=_("Single occurance prompt"),
        description=_(
            "This must ask the user for the name of the " "relevant location."
        ),
        required=True,
    )
    directives.widget(label_single_occurance="euphorie.content.risk.TextLines4Rows")

    depends("label_multiple_occurances", "use_location_question", "on")
    label_multiple_occurances = ConditionalTextLine(
        title=_("Multiple occurance prompt"),
        description=_(
            "This must ask the user for the names of all " "relevant locations."
        ),
        required=True,
    )
    directives.widget(label_multiple_occurances="euphorie.content.risk.TextLines4Rows")


@implementer(IProfileQuestion, IQuestionContainer)
class ProfileQuestion(Container):
    portal_type = "euphorie.profilequestion"

    question = None
    image = None
    optional = False

    def _get_id(self, orig_id):
        """Pick an id for pasted content."""
        frame = sys._getframe(1)
        ob = frame.f_locals.get("ob")
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super()._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super()._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)
            if IQuestionContainer.providedBy(object):
                my_depth = item_depth(self)
                paste_depth = tree_depth(object)
                if my_depth + paste_depth > ConstructionFilter.maxdepth:
                    raise ValueError("Pasting would create a too deep structure.")


@indexer(IProfileQuestion)
def SearchableTextIndexer(obj):
    """Index the title and description."""
    return " ".join([obj.title, StripMarkup(obj.description)])
