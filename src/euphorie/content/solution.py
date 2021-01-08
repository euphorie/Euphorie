# coding=utf-8
"""
Solution
--------

A standard Solution that a user can select for a particular risk.
"""

from .. import MessageFactory as _
from euphorie.content import utils
from five import grok
from plone.dexterity.content import Item
from plone.directives import dexterity
from plone.directives import form
from plone.indexer import indexer
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from zope import schema
from zope.i18n import translate
from zope.interface import implements

import markdown


grok.templatedir("templates")


class ISolution(form.Schema):
    """A standard solution for a risk.

    Risk questions can have standard solutions that can be applied in
    most environments.
    """

    description = schema.Text(
        title=_("label_module_description", u"Description"),
        description=_(
            "help_module_description",
            default=u"Include any relevant information that may be "
            u"helpful for the end-user.",
        ),
        required=True,
    )
    form.order_after(description="title")

    action_plan = schema.Text(
        title=_(
            "label_measure_action_plan",
            default=u"General approach (to eliminate or reduce the risk)",
        ),
        description=_(
            "help_measure_action_plan",
            default=u"Describe your general approach to eliminate or (if "
            u"the risk is not avoidable) reduce the risk.",
        ),
        required=False,
    )

    prevention_plan = schema.Text(
        title=_(
            "label_measure_prevention_plan",
            default=u"Specific action(s) required to implement this " u"approach",
        ),
        description=_(
            "help_measure_prevention_plan",
            default=u"Describe the specific action(s) required to "
            u"implement this approach (to eliminate or to reduce the risk).",
        ),
        required=False,
    )

    # This replaces action_plan and prevention_plan by concatenating the 2 fields.
    action = schema.Text(
        title=_(
            "label_measure_action",
            default=(
                u"General approach (to eliminate or reduce the risk) + "
                u"Specific action(s) required to implement this approach"
            ),
        ),
        description=_(
            "help_measure_action",
            default=(
                u"Describe your general approach to eliminate or "
                u"(if the risk is not avoidable) "
                u"reduce the risk. + Describe the specific action(s) "
                u"required to implement this approach "
                u"(to eliminate or to reduce the risk)."
            ),
        ),
        required=True,
    )

    requirements = schema.Text(
        title=_(
            "label_measure_requirements",
            default=u"Level of expertise and/or requirements needed",
        ),
        description=_(
            "help_measure_requirements",
            default=u"Describe the level of expertise needed to implement "
            u'the measure, for instance "common sense (no OSH knowledge '
            u'required)", "no specific OSH expertise, but minimum OSH '
            u"knowledge or training and/or consultation of OSH guidance "
            u'required", or "OSH expert". You can also describe here '
            u"any other additional requirement (if any).",
        ),
        required=False,
    )

    # show_in_identification = schema.Bool(
    #     title=_(
    #         "label_show_in_identification",
    #         default=u"Show this measure during Identification?"),
    #     description=_(
    #         "help_show_in_identification",
    #         default=u"Show this solution during the Identification phase as a "
    #         u"potential measure that is already in place? If the user selects "
    #         u"this measure during Identification, it will no longer be offered"
    #         u" in the Action Plan phase."),
    #     default=True,
    #     required=False,
    # )


class Solution(Item):
    implements(ISolution)
    title = _("title_common_solution", default=u"Measure")
    prevention_plan = None
    requirements = None
    portal_type = "euphorie.solution"

    def Title(self):
        survey = utils.getSurvey(self)
        return translate(
            Solution.title, context=self.REQUEST, target_language=survey.language
        ).encode("utf-8")


@indexer(ISolution)
def SearchableTextIndexer(obj):
    """Index the problem_description, question and solution_direction"""
    return " ".join(
        [
            obj.description,
            obj.action_plan or "",
            obj.prevention_plan or "",
            obj.requirements or "",
            obj.action or "",
        ]
    )


class View(grok.View):
    """View name: @@nuplone-view"""

    grok.context(ISolution)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("nuplone-view")
    grok.template("solution_view")

    def render_md(self, text):
        return markdown.markdown(text)


class Add(dexterity.AddForm):
    grok.context(ISolution)
    grok.name("euphorie.solution")
    grok.require("euphorie.content.AddNewRIEContent")

    def updateWidgets(self):
        super(Add, self).updateWidgets()
        self.widgets["action_plan"].mode = "hidden"
        self.widgets["prevention_plan"].mode = "hidden"
        self.widgets["action"].rows = 15


class Edit(form.SchemaEditForm):
    grok.context(ISolution)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("edit")

    def updateWidgets(self):
        super(Edit, self).updateWidgets()
        self.widgets["action_plan"].mode = "hidden"
        self.widgets["prevention_plan"].mode = "hidden"
        self.widgets["action"].rows = 15
