"""
Module
------

A module is a grouping for risks in a survey. It can be set to optional, in
which case all risks in it can be skipped. A module can contain other modules.

portal_type: euphorie.module
"""

from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from .behaviour.uniqueid import get_next_id
from .behaviour.uniqueid import INameFromUniqueId
from .fti import check_fti_paste_allowed
from .fti import ConditionalDexterityFTI
from .fti import IConstructionFilter
from .interfaces import IQuestionContainer
from .utils import StripMarkup
from Acquisition import aq_chain
from euphorie.content.dependency import ConditionalTextLine
from euphorie.content.utils import ensure_image_size
from euphorie.htmllaundry.z3cform import HtmlText
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.namedfile import field as filefield
from plone.namedfile.interfaces import INamedBlobImageField
from plone.supermodel import model
from plonetheme.nuplone.z3cform.directives import depends
from plonetheme.nuplone.z3cform.widget import WysiwygFieldWidget
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import validator
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid

import sys


class IModule(model.Schema, IRichDescription, IBasic):
    """Survey Module.

    A module is (hierarchical) grouping in a survey.
    """

    description = HtmlText(
        title=_("label_module_description", "Description"),
        description=_(
            "help_module_description",
            default="Include any relevant information that may be "
            "helpful for the end-user.",
        ),
        required=False,
    )
    directives.widget(description=WysiwygFieldWidget)
    directives.order_after(description="title")

    optional = schema.Bool(
        title=_("label_module_optional", default="This module is optional"),
        description=_(
            "help_module_optional",
            default="Allows the end-user to skip this module and "
            "everything inside it.",
        ),
        required=False,
        default=False,
    )

    depends("question", "optional", "on")
    question = ConditionalTextLine(
        title=_("label_module_question", default="Question"),
        description=_(
            "help_module_question",
            default="The question to ask the end-user if this module is "
            "optional. It must be formulated so that it is answerable "
            "with YES (the end-user will have to tick a box) or NO",
        ),
        required=True,
    )

    image = filefield.NamedBlobImage(
        title=_("label_image", default="Image file"),
        description=_(
            "help_image_upload",
            default="Upload an image. Make sure your image is of format "
            "png, jpg or gif and does not contain any special "
            "characters. The minimum size is 1000 (width) x 430 (height) pixels.",
        ),
        required=False,
    )
    caption = schema.TextLine(
        title=_("label_caption", default="Image caption"), required=False
    )

    solution_direction = HtmlText(
        title=_("label_solution_direction", default="Solution"),
        description=_(
            "help_solution_direction",
            default="This information will appear in the Action plan step "
            "and should include an overview of general solution(s) "
            "related to this module.",
        ),
        required=False,
    )
    directives.widget(solution_direction=WysiwygFieldWidget)

    model.fieldset(
        "additional_content",
        label=_("header_additional_content", default="Additional content"),
        description=_(
            "intro_additional_content",
            default="Attach any additional content you consider helpful "
            "for the user",
        ),
        fields=[
            "file1",
            "file1_caption",
            "file2",
            "file2_caption",
            "file3",
            "file3_caption",
            "file4",
            "file4_caption",
        ],
    )

    file1 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file1_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )

    file2 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file2_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )

    file3 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file3_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )

    file4 = filefield.NamedBlobFile(
        title=_("label_file", default="Content file"),
        description=_(
            "help_content_upload",
            default="Upload a file that contains additional information, "
            "like a PDF, Word document or spreadsheet. Optionally provide "
            "a descriptive caption for your file.",
        ),
        required=False,
    )
    file4_caption = schema.TextLine(
        title=_("label_file_caption", default="Content caption"), required=False
    )


class ImageSizeValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        try:
            previous_value = self.field.get(self.context)
        except AttributeError:
            previous_value = None
        if previous_value == value:
            try:
                ensure_image_size(value)
            except Invalid as invalid:
                IStatusMessage(self.context.REQUEST).add(invalid, "warn")
        else:
            ensure_image_size(value)


validator.WidgetValidatorDiscriminators(
    ImageSizeValidator, context=IModule, field=INamedBlobImageField
)


@implementer(IModule, IQuestionContainer)
class Module(Container):
    image = None
    caption = None
    file1 = None
    file1_caption = None
    file2 = None
    file2_caption = None
    file3 = None
    file3_caption = None
    file4 = None
    file4_caption = None

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


@indexer(IModule)
def SearchableTextIndexer(obj):
    """Index title, description and solution_direction."""
    return " ".join(
        [obj.title, StripMarkup(obj.description), StripMarkup(obj.solution_direction)]
    )


def tree_depth(obj):
    """Determine how deeply nested a module structure is.

    This is the opposite of item_depth.
    """
    submodules = [v for v in obj.values() if IQuestionContainer.providedBy(v)]
    if not submodules:
        return 1
    else:
        return 1 + max(tree_depth(m) for m in submodules)


def item_depth(item):
    """Return the survey depth of an item."""
    from euphorie.content.survey import ISurvey

    depth = 0
    for position in aq_chain(item):
        if ISurvey.providedBy(position):
            break
        depth += 1
    else:
        return None  # Not in a survey
    return depth


@adapter(ConditionalDexterityFTI, Interface)
@implementer(IConstructionFilter)
class ConstructionFilter:
    """FTI construction filter for :py:class:`Module` objects. This filter does
    two things: it restricts the maximum depth at which a module can be
    created, and it prevents creating of modules if the current container
    already contains a risk.

    This multi adapter requires the use of the conditional FTI as implemented
    by :py:class:`euphorie.content.fti.ConditionalDexterityFTI`.
    """

    maxdepth = 3

    def __init__(self, fti, container):
        self.fti = fti
        self.container = container

    def checkDepth(self):
        """Check if creating a new module would create a too deeply nested
        structure.

        :rtype: bool
        """
        depth = item_depth(self.container)
        if depth is None:
            return True
        return (depth + 1) <= self.maxdepth

    def checkForRisks(self):
        """Check if the container already contains a risk. If so refuse to
        allow creation of a module.

        :rtype: bool
        """
        for key in self.container:
            pt = self.container[key].portal_type
            if pt == "euphorie.risk":
                return False
        else:
            return True

    def allowed(self):
        """A module is allowed to be created providing :obj:`checkDepth` and
        :obj:`checkForRisks` are True

        :rtype: bool
        """
        return self.checkDepth() and self.checkForRisks()
