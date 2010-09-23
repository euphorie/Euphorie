from zope.interface import implements
from zope import schema
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.namedfile import field as filefield
from euphorie.content import MessageFactory as _
from htmllaundry.z3cform import HtmlText
from euphorie.content.behaviour.richdescription import IRichDescription


class ISolution(form.Schema, IRichDescription, IBasic):
    """A standard solution for a risk.

    Risk questions can have standard solutions that can be applied in
    most environments.
    """

    form.omitted("title")

    description = HtmlText(
            title = _(u"Description"),
            description = _(u"Describe the solution. Include any relevant "
                            u"information that may be helpful for users."),
            required = True)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    action_plan = schema.Text(
            title = _(u"Action plan"),
            description = _(u"Describe the action that can be taken to "
                            u"remove this risk. This information will be "
                            u"copied to the measure."),
            required = True)

    prevention_plan = schema.Text(
            title = _(u"Prevention plan"),
            description = _(u"Describe what can be done to prevent this risk "
                            u"from (re)occuring. This information will be "
                            u"copied to the measure."),
            required = False)

    requirements = schema.Text(
            title = _(u"Requirements"),
            description = _(u"Describe the standard requirements for the "
                            u"action plan and prevention plan. This "
                            u"information will be copied to the measure."),
            required = False)

    logo = filefield.NamedImage(
            title = _(u"Image"),
            description = _(u"A small image shown next to the solution."),
            required = False)


class Solution(dexterity.Item):
    implements(ISolution)

    title = _(u"Common solution")

