from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from .fti import ConditionalDexterityFTI
from .fti import IConstructionFilter
from Acquisition import aq_chain
from Acquisition import aq_inner
from euphorie.content.survey import ISurvey
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.select import SelectFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class IChoice(model.Schema, IRichDescription, IBasic):
    """ """

    allow_multiple_options = schema.Bool(
        title=_("label_allow_multiple_options", default="Allow multiple options"),
        description=_(
            "help_allow_multiple_options",
            default="If active, checkboxes are shown to allow selecting more than one "
            "option. Otherwise, radio buttons are used to force a single selection.",
        ),
        default=True,
    )
    condition = RelationList(
        title="Condition",
        description="Only show this choice if the user selects certain options for "
        "another choice. You can pick multiple options here. If the user selects one "
        "or more of them, then this choice will be shown. Leave blank to always show "
        "this choice.",
        value_type=RelationChoice(
            vocabulary=StaticCatalogVocabulary({"portal_type": ["euphorie.option"]}),
        ),
        required=False,
        default=[],
    )
    directives.widget("condition", SelectFieldWidget)


@implementer(IChoice)
class Choice(Container):
    def get_client_condition(self):
        if not self.condition:
            return None
        option_objs = [
            option.to_object for option in self.condition if option and option.to_object
        ]
        option_paths = ["/".join(obj.getPhysicalPath()[-3:]) for obj in option_objs]
        return "|".join(option_paths)


@adapter(ConditionalDexterityFTI, Interface)
@implementer(IConstructionFilter)
class ConstructionFilter:
    """FTI construction filter for :py:class:`Choice` objects. This filter makes sure
    that Choice objects can only be added to tools of a `tool_type` that supports them.

    This multi adapter requires the use of the conditional FTI as implemented
    by :py:class:`euphorie.content.fti.ConditionalDexterityFTI`.
    """

    def __init__(self, fti, container):
        self.fti = fti
        self.container = container

    def allowed(self):
        """A choice is allowed to be created if the `tool_type` supports it.

        :rtype: bool
        """
        for parent in aq_chain(aq_inner(self.container)):
            if ISurvey.providedBy(parent):
                return parent.get_tool_type_info().get("allow_choice", False)
        # If we're not inside a survey we don't care what happens
        return True
