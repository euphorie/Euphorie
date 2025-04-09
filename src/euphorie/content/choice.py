from .. import MessageFactory as _
from .behaviour.richdescription import IRichDescription
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.select import SelectFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


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
