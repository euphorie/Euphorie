"""
Survey
======

A survey holds the entire risk assessment survey. The survey is a hierarchical
structure containing modules, profile questions and questions. Both modules and
profile questions are used to create the hierarchy.
"""

from .. import MessageFactory as _
from .behaviour.uniqueid import get_next_id
from .behaviour.uniqueid import INameFromUniqueId
from .datamanager import ParentAttributeField
from .fti import check_fti_paste_allowed
from .interfaces import IQuestionContainer
from .profilequestion import IProfileQuestion
from .utils import StripMarkup
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.content.dependency import ConditionalHtmlText
from euphorie.content.dependency import ConditionalTextLine
from euphorie.content.utils import get_tool_type_default
from euphorie.content.utils import IToolTypesInfo
from euphorie.htmllaundry.z3cform import HtmlText
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.supermodel import model
from plonetheme.nuplone.z3cform.directives import depends
from zope import schema
from zope.component import getUtility
from zope.interface import implementer

import sys


class ISurvey(model.Schema, IBasic):
    """Survey.

    The survey is the root of a survey.
    """

    title = schema.TextLine(
        title=_("label_survey_title", default="Version name"),
        description=_(
            "help_survey_title",
            default="This is the title of this OiRA Tool version. This "
            "name is never shown to users.",
        ),
        required=True,
    )
    directives.order_before(title="*")

    directives.omitted("description")

    introduction = HtmlText(
        title=_("label_introduction", default="Introduction text"),
        description=_(
            "The introduction text is shown when starting a new "
            "OiRA Tool session. If no introduction is provided here a "
            "standard text will be shown. Please keep this text brief "
            "so it will easily fit on screens of small devices such as "
            "phones and PDAs."
        ),
        required=False,
    )
    directives.widget(introduction=WysiwygFieldWidget)

    evaluation_optional = schema.Bool(
        title=_("label_evaluation_optional", default="Evaluation may be skipped"),
        description=_(
            "help_evaluation_optional",
            default="This option allows users to skip the evaluation " "phase.",
        ),
        default=False,
        required=False,
    )

    language = schema.Choice(
        title=_("label_language", default="Language"),
        vocabulary="plone.app.vocabularies.AvailableContentLanguages",
        default="en",
        required=True,
    )

    classification_code = schema.TextLine(
        title=_("label_classification_code", default="Classification code"),
        description=_(
            "help_classification_code",
            default="A code identifying this sector. Classification "
            "codes are defined by national standards bodies "
            "and based on revision 2 of the NACE standard.",
        ),
        required=False,
    )

    tool_type = schema.Choice(
        title=_("label_tool_type", default="Type of OiRA Tool"),
        description=_(
            "description_tool_type",
            default="This selection determines, which variant of an OiRA Tool"
            ' will be created. If you are not sure, select "Classic".',
        ),
        vocabulary="euphorie.tool_types_vocabulary",
        defaultFactory=get_tool_type_default,
        required=True,
    )

    measures_text_handling = schema.Choice(
        title=_(
            "measures_text_handling",
            default="Handling of measures text (if measures-in-place are used)",
        ),
        description=_(
            "description_measures_text_handling",
            default=(
                "Defines how the “Measures in place” options are displayed "
                "to the user. "
                "Choose “Simple” if the texts for Description and General Approach "
                "are identical in your measures. "
                "Choose “Full” if the texts in General Approach "
                "provide more details than the Description."
            ),
        ),
        vocabulary="euphorie.measures_text_handling_vocabulary",
        default="full",
        required=True,
    )

    integrated_action_plan = schema.Bool(
        title=_("label_integrated_action_plan", default="Integrated Action Plan"),
        description=_(
            "description_integrated_action_plan",
            default="If selected, the option to plan measures will be offered "
            "directly on the “Identification” page. There will be no separate "
            "“Action Plan” step in the navigation.",
        ),
        required=False,
        default=False,
    )

    enable_web_training = schema.Bool(
        title=_("label_enable_web_training", default="Enable Web Based Training?"),
        description=_(
            "help_enable_web_training",
            default="If this option is activated, users will be able to take an "
            "online training with this OiRA tool. A successful training will be "
            "recorded and shown with a certificate on the user's dashbooard. You "
            "will be asked to provide Training Questions for the final exam.",
        ),
        required=False,
    )

    depends("num_training_questions", "enable_web_training", "on")
    num_training_questions = schema.Int(
        title=_(
            "label_num_training_questions",
            default="Number of questions asked after training",
        ),
        description=_(
            "help_num_training_questions",
            default="Please enter the number of questions to be shown at the end of "
            "your training session. If the number is lower than the number of existing "
            "questions, the questions will be picked randomly. Empty the field to show "
            "all questions.",
        ),
        required=False,
    )

    enable_tool_notification = schema.Bool(
        title=_(
            "label_enable_tool_notification",
            default="Show a custom notification for this OiRA tool?",
        ),
        description=_(
            "description_tool_notification",
            default="If you enter text here, it will be shown to users "
            "in a pop-up when they open the tool. It can be used for "
            "notifying users about changes.",
        ),
        required=False,
        default=False,
    )

    depends("tool_notification_title", "enable_tool_notification", "on")
    tool_notification_title = ConditionalTextLine(
        title=_("label_tool_notification_title", default="Tool notification title"),
        required=True,
    )

    depends("tool_notification_message", "enable_tool_notification", "on")
    tool_notification_message = ConditionalHtmlText(
        title=_("label_tool_notification", default="Tool notification message"),
        required=True,
    )
    directives.widget(tool_notification_message=WysiwygFieldWidget)


class SurveyAttributeField(ParentAttributeField):
    parent_mapping = {
        "survey_title": "title",
        "obsolete": "obsolete",
    }


def get_tool_type(context):
    """Return the tool type used in a given context.

    The type is set on the survey.
    """
    from euphorie.content.survey import ISurvey  # XXX Circular

    tt_default = get_tool_type_default()
    for parent in aq_chain(aq_inner(context)):
        if ISurvey.providedBy(parent):
            return getattr(parent, "tool_type", "") or tt_default
    return tt_default


@implementer(ISurvey, IQuestionContainer)
class Survey(Container):
    """A risk assessment survey.

    A survey uses the *IIdGenerationRoot* behaviour to guarantee that
    all items inside the survey have a unique id.
    """

    dirty = False

    def _get_id(self, orig_id):
        """Pick an id for pasted content."""
        frame = sys._getframe(1)
        ob = frame.f_locals.get("ob")
        if ob is not None and INameFromUniqueId.providedBy(ob):
            return get_next_id(self)
        return super()._get_id(orig_id)

    def _verifyObjectPaste(self, object, validate_src=True):
        super()._verifyObjectPaste(object, validate_src)
        if validate_src:
            check_fti_paste_allowed(self, object)

    def hasProfile(self):
        """Check if this survey has any profile questions.

        .. todo::    Implement the deprecation checking
        """

        for child in self.values():
            if IProfileQuestion.providedBy(child):
                return True
        else:
            return False

    def hasNotification(self):
        """Checks if a notification message was set."""
        return self.enable_tool_notification or False

    def ProfileQuestions(self):
        """Return a list of all profile questions."""
        return [child for child in self.values() if IProfileQuestion.providedBy(child)]

    def get_tool_type_name(self):
        """Returns the human readable name of the chosen tool type."""
        my_tool_type = get_tool_type(self)
        tti = getUtility(IToolTypesInfo)
        tool_types = tti()
        if my_tool_type not in tool_types:
            my_tool_type = tti.default_tool_type
        return tool_types[my_tool_type]["title"]


@indexer(ISurvey)
def SearchableTextIndexer(obj):
    return " ".join(
        [
            obj.title,
            StripMarkup(obj.description),
            StripMarkup(obj.introduction),
            obj.classification_code or "",
        ]
    )


@indexer(ISurvey)
def LanguageIndexer(obj):
    language = obj.language or ""
    return language.strip().split("-")[0]


class ISurveyAddSchema(model.Schema):
    title = schema.TextLine(
        title=_("label_survey_title", default="Version name"),
        description=_(
            "help_survey_title",
            default="This is the title of this OiRA Tool version. This "
            "name is never shown to users.",
        ),
        required=True,
    )


def handleSurveyUnpublish(survey, event):
    """Event handler (subscriber) for unpublishing a survey."""
    if hasattr(aq_base(survey), "published"):
        delattr(survey, "published")

    surveygroup = aq_parent(survey)
    if surveygroup.published == survey.id:
        surveygroup.published = None
