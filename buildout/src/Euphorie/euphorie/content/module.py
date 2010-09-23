from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from zope import schema
from five import grok
from plone.directives import form
from plone.directives import dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from htmllaundry.z3cform import HtmlText
from euphorie.content.behaviour.richdescription import IRichDescription
from euphorie.content.interfaces import IQuestionContainer
from euphorie.content import MessageFactory as _
from euphorie.content.risk import IRisk
from plone.namedfile import field as filefield


class IModule(form.Schema, IRichDescription, IBasic):
    """RIE Module.

    A module is (hierarchical) grouping in a RIE.
    """

    description = HtmlText(
            title = _(u"Description"),
            description = _(u"Describe the risk. Include any relevant "
                            u"information that may be helpful for users."),
            required = True)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    optional = schema.Bool(
            title = _(u"This module is optional"),
            description = _(u"Allow users to skip this module and "
                            u"everything inside it."),
            default = False)

    question = schema.TextLine(
            title = _(u"Question"),
            description = _(u"The question to ask users if this module is "
                            u"optional. This has to be a yes/no question."),
            required = False)

    image = filefield.NamedImage(
            title = _(u"Image"),
            description = _(u"This image will be shown along with the "
                            u"description"),
            required = False)

    solution_direction = HtmlText(
            title = _(u"Solution direction"),
            description = _(u"This information will be shown to users when "
                            u"they enter this module while working on the "
                            u"action plan."),
            required = False)
    form.widget(solution_direction=WysiwygFieldWidget)



class Module(dexterity.Container):
    implements(IModule, IQuestionContainer)



class View(grok.View):
    grok.context(IModule)
    grok.require("zope2.View")

    def _morph(self, child):
        state=getMultiAdapter((child, self.request), name="plone_context_state")
        return dict(id=child.id,
                    title=child.title,
                    url=state.view_url())

    def add_risk_url(self):
        return "%s/++add++euphorie.risk" % \
                aq_inner(self.context).absolute_url()

    def add_module_url(self):
        return "%s/++add++euphorie.module" % \
                aq_inner(self.context).absolute_url()

    def modules(self):
        return [self._morph(child) for child in self.context.values()
                if IModule.providedBy(child)]

    def risks(self):
        return [self._morph(child) for child in self.context.values()
                if IRisk.providedBy(child)]

