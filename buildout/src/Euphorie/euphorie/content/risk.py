from persistent import Persistent
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from z3c.form.interfaces import IObjectFactory
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from htmllaundry.z3cform import HtmlText
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content import MessageFactory as _
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.namedfile import field as filefield


class IInformationLink(Interface):
    """A link to more information related to a risk."""

    url = schema.URI(
            title = _(u"URL"),
            required = True)
    title = schema.TextLine(
            title = _(u"Description"),
            required = False)


class InformationLink(Persistent):
    """Utility class to store information about a URL."""
    implements(IInformationLink)

    def __init__(self, value):
        self.url=value["url"]
        self.title=value["title"]


class InformationLinkFactory(object):
    """:obj:`IObjectFactory` implementation for :obj:`IInformationLink`
    objects. This is required by :mod:`z3c.form`_.
    """
    adapts(Interface, Interface, Interface, Interface)
    implements(IObjectFactory)

    def __init__(self, context, request, form, widget):
        pass

    def __call__(self, value):
        return InformationLink(value)


class IRisk(form.Schema, IRichDescription, IBasic):
    """A possible risk that can be present in an organisation.
    """

    title = schema.TextLine(
            title = _(u"Statement"),
            description = _(u"This is a short statement about a possible risk."),
            required = True)
    form.order_before(title="*")

    problem_description = schema.TextLine(
            title = _(u"Problem description"),
            description = _(u"This is the inverse of the statement: a "
                            u"short description of current (bad) situation."),
            required = False)
    form.order_after(problem_description="title")

    description = HtmlText(
            title = _(u"Description"),
            description = _(u"Describe the risk. Include any relevant "
                            u"information that may be helpful for users."),
            required = True)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="problem_description")

    type = schema.Choice(
            title = _(u"Type"),
            description = _(u"Select the risk type"),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(u"risk", u"Risk"),
                            SimpleTerm(u"policy", u"Policy"),
                            SimpleTerm(u"top5", u"Top 5 risk"),
                            ]),
            default = u"risk",
            required = True)

    show_notapplicable = schema.Bool(
            title = _(u"Show `not applicable' evaluation option"),
            description = _(u"Offer a `not applicable' option in addition "
                            u"to the standard yes/no/park options."),
            default = False)

    evaluation_method = schema.Choice(
            title = _(u"Evaluation method"),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(u"direct", u"Direct"),
                            SimpleTerm(u"calculated", u"Calculated"),
                            ]),
            default = u"direct",
            required = True)

    default_probability = schema.Choice(
            title = _(u"Default probability"),
            description = _(u"Indicate how likely occurence of this risk "
                            u"is in a normal situation."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(0, "no default"),
                            SimpleTerm(1, "small"),
                            SimpleTerm(3, "medium"),
                            SimpleTerm(5, "big"),
                            ]),
            default = 0)

    default_frequency = schema.Choice(
            title = _(u"Default frequency"),
            description = _(u"Indicate how often this risk occurs in a "
                            u"normal situation."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(0, "no default"),
                            SimpleTerm(1, "almost never"),
                            SimpleTerm(4, "regularly"),
                            SimpleTerm(7, "constantly"),
                            ]),
            default = 0)

    default_effect = schema.Choice(
            title = _(u"Default severity"),
            description = _(u"Indicate the severity of the manage if this risk occurs."),
            vocabulary = SimpleVocabulary([
                            SimpleTerm(0, "no default"),
                            SimpleTerm(1, "weak severity"),
                            SimpleTerm(5, "significant severity"),
                            SimpleTerm(10, "high (very high) severity"),
                            ]),
            default = 0)

    image = filefield.NamedImage(
            title = _(u"Image"),
            description = _(u"This image will be shown along with the "
                            u"description"),
            required = False)

    legal_reference = HtmlText(
            title = _(u"Legal and policy references."),
            description = _(u"Describe, and optionally link to, any relevant "
                            u"laws and policies."),
            required=False)
    form.widget(legal_reference=WysiwygFieldWidget)

    links = schema.List(
            title = _(u"Information links"),
            description = _(u"A list of links to webpages which provide "
                            u"more information on this risk."),
            required = False,
            value_type = schema.Object(
                title = _(u"Link"),
                schema = IInformationLink))



class Risk(dexterity.Container):
    implements(IRisk)

