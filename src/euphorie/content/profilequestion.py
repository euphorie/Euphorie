import sys
from five import grok
from zope.interface import implements
from zope import schema
from zope.component import getMultiAdapter
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from plone.indexer import indexer
from .. import MessageFactory as _
from htmllaundry.z3cform import HtmlText
from .behaviour.uniqueid import INameFromUniqueId
from .behaviour.uniqueid import get_next_id
from .behaviour.richdescription import IRichDescription
from .fti import check_fti_paste_allowed
from .interfaces import IQuestionContainer
from .risk import IRisk
from .utils import StripMarkup
from .module import IModule
from .module import item_depth
from .module import tree_depth
from .module import ConstructionFilter


grok.templatedir("templates")

TextSpan7 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget",
        klass="span-7")


class IProfileQuestion(form.Schema, IRichDescription, IBasic):
    """Survey Profile question.

    A profile question is used to determine if parts of a survey should
    be skipped, or repeated multiple times.
    """
    form.widget(title="euphorie.content.profilequestion.TextSpan7")

    question = schema.TextLine(
            title=_("label_profilequestion_question", default=u"Question"),
            description=_("help_profilequestion_question",
                default=u"This is must be formulated as a prompt to fill in "
                        u"multiple values."),
            required=True)
    form.widget(question="euphorie.content.profilequestion.TextSpan7")
    form.order_after(question="title")

    description = HtmlText(
            title=_("label_module_description", u"Description"),
            description=_("help_module_description",
                default=u"Include any relevant information that may be "
                        u"helpful for users."))
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="question")


class ProfileQuestion(dexterity.Container):
    implements(IProfileQuestion, IQuestionContainer)

    question = None
    image = None
    optional = False

    def _get_id(self, orig_id):
        """Pick an id for pasted content."""
        frame = sys._getframe(1)
        ob = frame.f_locals.get('ob')
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super(ProfileQuestion, self)._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super(ProfileQuestion, self)._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)
            if IQuestionContainer.providedBy(object):
                my_depth = item_depth(self)
                paste_depth = tree_depth(object)
                if my_depth + paste_depth > ConstructionFilter.maxdepth:
                    raise ValueError('Pasting would create a too deep structure.')


@indexer(IProfileQuestion)
def SearchableTextIndexer(obj):
    return " ".join([obj.title,
                     StripMarkup(obj.description)])


class View(grok.View):
    grok.context(IProfileQuestion)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("profilequestion_view")
    grok.name("nuplone-view")

    def _morph(self, child):
        state = getMultiAdapter((child, self.request),
                name="plone_context_state")
        return {'id': child.id,
                'title': child.title,
                'url': state.view_url()}

    def update(self):
        self.modules = [self._morph(child)
                        for child in self.context.values()
                        if IModule.providedBy(child)]
        self.risks = [self._morph(child) for child in self.context.values()
                      if IRisk.providedBy(child)]
