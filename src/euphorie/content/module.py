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
from .risk import IRisk
from .utils import DragDropHelper
from .utils import StripMarkup
from Acquisition import aq_chain
from five import grok
from htmllaundry.z3cform import HtmlText
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.dexterity.interfaces import IDexterityFTI
from plone.directives import dexterity
from plone.directives import form
from plone.indexer import indexer
from plone.namedfile import field as filefield
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.directives import depends
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface
import sys

grok.templatedir("templates")


class IModule(form.Schema, IRichDescription, IBasic):
    """Survey Module.

    A module is (hierarchical) grouping in a survey.
    """
    description = HtmlText(
            title=_("label_module_description", u"Description"),
            description=_("help_module_description",
                default=u"Include any relevant information that may be "
                    u"helpful for the end-user."),
            required=False)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    optional = schema.Bool(
            title=_("label_module_optional",
                default=u"This module is optional"),
            description=_("help_module_optional",
                default=u"Allows the end-user to skip this module and "
                    u"everything inside it."),
            required=False,
            default=False)

    depends("question", "optional", "on")
    question = schema.TextLine(
            title=_("label_module_question", default=u"Question"),
            description=_("help_module_question",
                default=u"The question to ask the end-user if this module is "
                    u"optional. It must be formulated so that it is answerable "
                    u"with YES (the end-user will have to tick a box) or NO"),
            required=False)

    image = filefield.NamedBlobImage(
            title=_("label_image", default=u"Image file"),
            description=_("help_image_upload",
                default=u"Upload an image. Make sure your image is of format "
                        u"png, jpg or gif and does not contain any special "
                        u"characters."),
            required=False)
    caption = schema.TextLine(
            title=_("label_caption", default=u"Image caption"),
            required=False)

    solution_direction = HtmlText(
            title=_("label_solution_direction",
                default=u"Solution"),
            description=_("help_solution_direction",
                default=u"This information will appear in the Action plan step "
                    u"and should include an overview of general solution(s) "
                    u"related to this module."),
            required=False)
    form.widget(solution_direction=WysiwygFieldWidget)

    form.fieldset(
        "additional_content",
        label=_("header_additional_content", default=u"Additional content"),
        description=_(
            "intro_additional_content",
            default=u"Attach any additional content you consider helpful "
            "for the user"),
        fields=[
            "file1", "file1_caption", "file2", "file2_caption",
            "file3", "file3_caption", "file4", "file4_caption"])

    file1 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file1_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)

    file2 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file2_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)

    file3 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file3_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)

    file4 = filefield.NamedBlobFile(
        title=_("label_file", default=u"Content file"),
        description=_(
            "help_content_upload",
            default=u"Upload a file that contains additional information, "
            u"like a PDF, Word document or spreadsheet. Optionally provide "
            u"a descriptive caption for your file."),
        required=False)
    file4_caption = schema.TextLine(
        title=_("label_file_caption", default=u"Content caption"),
        required=False)


class Module(dexterity.Container):
    implements(IModule, IQuestionContainer)

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
        ob = frame.f_locals.get('ob')
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super(Module, self)._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super(Module, self)._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)
            if IQuestionContainer.providedBy(object):
                my_depth = item_depth(self)
                paste_depth = tree_depth(object)
                if my_depth + paste_depth > ConstructionFilter.maxdepth:
                    raise ValueError('Pasting would create a too deep structure.')


@indexer(IModule)
def SearchableTextIndexer(obj):
    """ Index the problem_description, question and solution_direction
    """
    return " ".join([obj.title,
                     StripMarkup(obj.problem_description),
                     StripMarkup(obj.question),
                     StripMarkup(obj.solution_direction)])


class View(grok.View, DragDropHelper):
    """ View name: @@nuplone-view
    """
    grok.context(IModule)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("module_view")
    grok.name("nuplone-view")

    def _morph(self, child):
        state = getMultiAdapter((child, self.request),
                name="plone_context_state")
        return {'id': child.id,
                'title': child.title,
                'url': state.view_url()}

    def update(self):
        """ Set view attributes which list modules and risks in the current
        context.
        """
        self.modules = [self._morph(child) for child in self.context.values()
                        if IModule.providedBy(child)]
        self.risks = [self._morph(child) for child in self.context.values()
                      if IRisk.providedBy(child)]

    @property
    def portal_type(self):
        if self.context.aq_parent.portal_type == 'euphorie.module':
            return _('Submodule')
        else:
            portal_type = self.context.portal_type
            fti = getUtility(IDexterityFTI, name=portal_type)
            return fti.Title()


class Edit(form.SchemaEditForm):
    """Override for the standard edit form so we can change the form title
    for submodules.

    View name: @@edit
    """
    grok.context(IModule)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("edit")

    @property
    def label(self):
        if self.context.aq_parent.portal_type == 'euphorie.module':
            type_name = _('Submodule')
        else:
            portal_type = self.context.portal_type
            fti = getUtility(IDexterityFTI, name=portal_type)
            type_name = fti.Title()
        return _(u"Edit ${name}", mapping={'name': type_name})

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        self.widgets["title"].addClass("span-7")


class Add(dexterity.AddForm):
    grok.name('euphorie.module')
    grok.context(IModule)

    @property
    def label(self):
        if self.context.portal_type == 'euphorie.module':
            type_name = _('Submodule')
        else:
            portal_type = self.portal_type
            fti = getUtility(IDexterityFTI, name=portal_type)
            type_name = fti.Title()
        return _(u"Add %s" % type_name)


def tree_depth(obj):
    """Determine how deeply nested a module structure is. This is the opposite
    of item_depth.
    """
    submodules = [v for v in obj.values() if IQuestionContainer.providedBy(v)]
    if not submodules:
        return 1
    else:
        return 1 + max(tree_depth(m) for m in submodules)


def item_depth(item):
    """Return the survey depth of an item.
    """
    from euphorie.content.survey import ISurvey
    depth = 0
    for position in aq_chain(item):
        if ISurvey.providedBy(position):
            break
        depth += 1
    else:
        return None  # Not in a survey
    return depth


class ConstructionFilter(grok.MultiAdapter):
    """FTI construction filter for :py:class:`Module` objects. This filter
    does two things: it restricts the maximum depth at which a module can
    be created, and it prevents creating of modules if the current container
    already contains a risk.

    This multi adapter requires the use of the conditional FTI as implemented
    by :py:class:`euphorie.content.fti.ConditionalDexterityFTI`.
    """

    grok.adapts(ConditionalDexterityFTI, Interface)
    grok.implements(IConstructionFilter)
    grok.name("euphorie.module")

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
        """ A module is allowed to be created providing :obj:`checkDepth` and
        :obj:`checkForRisks` are True

        :rtype: bool
        """
        return self.checkDepth() and self.checkForRisks()
