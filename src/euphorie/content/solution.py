"""
Solution
--------

A standard Solution that a user can select for a particular risk.
"""

from zope.interface import implements
from zope import schema
from zope.i18n import translate
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from .. import MessageFactory as _
from euphorie.content import utils

grok.templatedir("templates")


class ISolution(form.Schema):
    """A standard solution for a risk.

    Risk questions can have standard solutions that can be applied in
    most environments.
    """

    description = schema.Text(
            title=_("label_module_description", u"Description"),
            description=_("help_module_description",
                default=u"Include any relevant information that may be "
                    u"helpful for the end-user."),
            required=True)
    form.order_after(description="title")

    action_plan = schema.Text(
            title=_("label_measure_action_plan",
                default=u"General approach (to eliminate or reduce the risk)"),
            description=_("help_measure_action_plan",
                default=u"Describe your general approach to eliminate or (if "
                    u"the risk is not avoidable) reduce the risk."),
            required=True)

    prevention_plan = schema.Text(
            title=_("label_measure_prevention_plan",
                default=u"Specific action(s) required to implement this "
                        u"approach"),
            description=_("help_measure_prevention_plan",
                default=u"Describe the specific action(s) required to "
                    u"implement this approach (to eliminate or to reduce the risk)."),
            required=False)

    requirements = schema.Text(
            title=_("label_measure_requirements",
                default=u"Level of expertise and/or requirements needed"),
            description=_("help_measure_requirements",
                default=u'Describe the level of expertise needed to implement '
                    u'the measure, for instance "common sense (no OSH knowledge '
                    u'required)", "no specific OSH expertise, but minimum OSH '
                    u'knowledge or training and/or consultation of OSH guidance '
                    u'required", or "OSH expert". You can also describe here '
                    u'any other additional requirement (if any).'),
            required=False)


class Solution(dexterity.Item):
    implements(ISolution)
    title = _("title_common_solution", default=u"Measure")
    prevention_plan = None
    requirements = None

    def Title(self):
        survey = utils.getSurvey(self)
        return translate(
                    Solution.title,
                    context=self.REQUEST,
                    target_language=survey.language).encode('utf-8')


class View(grok.View):
    """ View name: @@nuplone-view
    """
    grok.context(ISolution)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("solution_view")
