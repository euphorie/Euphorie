from five import grok
from zope.interface import implements
from zope import schema
from zope.component import getMultiAdapter
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from euphorie.content import MessageFactory as _
from htmllaundry.z3cform import HtmlText
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content.risk import IRisk
from euphorie.content.utils import StripMarkup
from euphorie.content.module import IModule
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.z3cform.form import FieldWidgetFactory
from plone.indexer import indexer

grok.templatedir("templates")

TextSpan7 = FieldWidgetFactory("z3c.form.browser.text.TextFieldWidget", klass="span-7")

class IProfileQuestion(form.Schema, IRichDescription, IBasic):
    """Survey Profile question.

    A profile question is used to determine if parts of a survey should
    be skipped, or repeated multiple times.
    """
    form.widget(title="euphorie.content.profilequestion.TextSpan7")

    question = schema.TextLine(
            title = _("label_profilequestion_question", default=u"Question"),
            description = _("help_profilequestion_question",
                default=u"If this is to be an \"optional\" profile question, "
                        u"it must be formulated as a question and be answerable "
                        u"with YES or NO. If this is to be a \"repeatable\" profile "
                        u"question (statement), it must be formulated as a prompt "
                        u"to fill in multiple values."),
            required = True)
    form.widget(question="euphorie.content.profilequestion.TextSpan7")
    form.order_after(question="title")

    description = HtmlText(
            title = _("label_module_description", u"Description"),
            description = _("help_module_description",
                default=u"Include any relevant information that may be "
                        u"helpful for users."))
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="question")

    type = schema.Choice(
            title = _("label_profile_type", default=u"Type"),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(u"optional", title=_("profile_optional", default=u"Optional")),
                            SimpleTerm(u"repeat", title=_("profile_repeat", default=u"Repeatable")),
                            ]),
            default = u"optional",
            required = True)



class ProfileQuestion(dexterity.Container):
    implements(IProfileQuestion, IQuestionContainer)

    optional = False
    question = None
    image = None



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
        state=getMultiAdapter((child, self.request), name="plone_context_state")
        return dict(id=child.id,
                    title=child.title,
                    url=state.view_url())

    def update(self):
        self.modules=[self._morph(child) for child in self.context.values()
                      if IModule.providedBy(child)]
        self.risks=[self._morph(child) for child in self.context.values()
                    if IRisk.providedBy(child)]

