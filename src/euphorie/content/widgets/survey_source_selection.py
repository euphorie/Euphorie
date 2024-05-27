from euphorie import MessageFactory as _
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IObjectWidget
from z3c.form.object import ObjectWidget
from z3c.form.widget import FieldWidget
from zope import schema
from zope.component import adapter
from zope.interface import classImplementsFirst
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ISurveySourceSchema(Interface):
    source = schema.Choice(
        title=_("label_source", default="How would you like to start"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    "scratch",
                    title=_(
                        "survey_source_scratch",
                        default="Create a new OiRA Tool from scratch",
                    ),
                ),
                SimpleTerm(
                    "local",
                    title=_(
                        "survey_source_local",
                        default=(
                            "Base my new OiRA Tool "
                            "on an existing OiRA Tool of my organisation"
                        ),
                    ),
                ),
                SimpleTerm(
                    "other",
                    title=_(
                        "survey_source_other",
                        default=(
                            "Base my new OiRA Tool "
                            "on an existing OiRA Tool of another organisation"
                        ),
                    ),
                ),
            ]
        ),
        default="scratch",
    )

    country = schema.Choice(
        title=_("label_choose_country", default="Choose a country"),
        vocabulary=SimpleVocabulary([]),
        required=False,
    )

    local_surveygroup = schema.Choice(
        title=_("label_choose_surveygroup", default="Choose an OiRA Tool"),
        required=False,
        vocabulary=SimpleVocabulary([]),
    )

    local_revision = schema.Choice(
        title=_(
            "label_choose_survey",
            default="Choose a revision for the selected OiRA Tool",
        ),
        required=False,
        vocabulary=SimpleVocabulary([]),
    )


class ISurveySourceSelectionField(schema.interfaces.IObject):
    """Interface for field that allows the user to select a source for the survey."""


class SurveySourceSelectionField(schema.Object):
    """A field that allows the user to select a source for the survey."""

    def __init__(self, **kwargs):
        super().__init__(schema=ISurveySourceSchema, **kwargs)


classImplementsFirst(SurveySourceSelectionField, ISurveySourceSelectionField)


class ISurveySourceSelectionWidget(IObjectWidget):
    """A widget for the survey source selection field."""


@implementer(ISurveySourceSelectionWidget)
class SurveySourceSelectionWidget(ObjectWidget):
    klass = "survey-source-selection-widget"
    css = "survey-source-selection"


@adapter(ISurveySourceSelectionField, IFormLayer)
@implementer(IFieldWidget)
def SurveySourceSelectionFieldWidget(field, request):
    """IFieldWidget factory for IObjectWidget."""
    return FieldWidget(field, SurveySourceSelectionWidget(request))
