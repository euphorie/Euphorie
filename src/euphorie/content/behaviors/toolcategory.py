from euphorie.content import MessageFactory as _
from euphorie.content.vocabularies import RegistryValueVocabulary
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IToolCategory(model.Schema):
    tool_category = schema.List(
        title=_("title_tool_category", default="Tool category"),
        description=_(
            "description_tool_category",
            default="Select one or more categories to which this OiRA tool "
            "is relevant. The user will then find this tool under the chosen"
            " categories.",
        ),
        required=False,
        value_type=schema.Choice(
            source=RegistryValueVocabulary(
                "euphorie.content.vocabularies.toolcategories",
            ),
        ),
    )
