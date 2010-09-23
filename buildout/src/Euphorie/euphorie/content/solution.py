from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import implements
from zope import schema
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from euphorie.content import MessageFactory as _
from htmllaundry.z3cform import HtmlText
from euphorie.content.behaviour.richdescription import IRichDescription


class ISolution(form.Schema, IRichDescription):
    """A standard solution for a risk.

    Risk questions can have standard solutions that can be applied in
    most environments.
    """

    description = HtmlText(
            title = _("label_module_description", u"Description"),
            description = _("help_module_description",
                default=u"Include any relevant information that may be "
                        u"helpful for users."),
            required = True)
    form.widget(description=WysiwygFieldWidget)
    form.order_after(description="title")

    action_plan = schema.Text(
            title = _("label_measure_action_plan", default=u"Action plan"),
            description = _("help_measure_action_plan",
                default=u"Describe the action that can be taken to "
                        u"remove this risk. This information will be "
                        u"copied to the measure."),
            required = True)

    prevention_plan = schema.Text(
            title = _("label_measure_prevention_plan", default=u"Prevention plan"),
            description = _("help_measure_prevention_plan",
                default=u"Describe what can be done to prevent this risk "
                        u"from (re)occuring. This information will be "
                        u"copied to the measure."),
            required = False)

    requirements = schema.Text(
            title = _("label_measure_requirements", default=u"Requirements"),
            description = _("help_measure_requirements",
                default=u"Describe the standard requirements for the "
                        u"action plan and prevention plan. This "
                        u"information will be copied to the measure."),
            required = False)



class Solution(dexterity.Item):
    implements(ISolution)

    title = _("title_common_solution", default=u"Common solution")



class View(grok.View):
    grok.context(ISolution)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")

    def render(self):
        risk=aq_parent(aq_inner(self.context))
        self.request.response.redirect("%s#solution-%s" % (risk.absolute_url(), self.context.id))

