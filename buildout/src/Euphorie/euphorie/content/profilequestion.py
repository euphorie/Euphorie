from zope.interface import implements
from zope import schema
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

class IProfileQuestion(form.Schema, IRichDescription, IBasic):
    """RIE Profile question.

    A profile question is used to determine if parts of a RIE should
    be skipped, or repeated multiple times.
    """
    description = HtmlText(
            title = _(u"Description"),
            description = _(u"Describe the risk. Include any relevant "
                            u"information that may be helpful for users."),
            required = True)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    solution_direction = HtmlText(
            title = _(u"Solution direction"),
            description = _(u"This information will be shown to users when "
                            u"they enter this module while working on the "
                            u"action plan."),
            required = False)
    form.widget(solutions=WysiwygFieldWidget)

    type = schema.Choice(
            title = _(u"Type"),
            description = _(u"Select the profile type"),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(u"optional", u"Optional"),
                            SimpleTerm(u"repeat", u"Repeatable"),
                            ]),
            default = u"optional",
            required = True)


class ProfileQuestion(dexterity.Container):
    implements(IProfileQuestion, IQuestionContainer)

    optional = False


