"""
Help
----

A Help document with multiple rich text fields.

https://admin.oiraproject.eu/documents/en/help

portal_type: euphorie.help
"""

from .. import MessageFactory as _
from euphorie.content.utils import StripMarkup
from euphorie.htmllaundry.z3cform import HtmlText
from plone.autoform import directives
from plone.indexer import indexer
from plone.supermodel import model
from plonetheme.nuplone.z3cform.widget import WysiwygFieldWidget


class IOnlineHelp(model.Schema):
    introduction = HtmlText(
        title=_("label_help_introduction", default="Introduction"),
        description=_(
            "help_help_introduction", default="General information on risk assessment"
        ),
        required=True,
    )
    directives.widget(introduction=WysiwygFieldWidget)

    authentication = HtmlText(
        title=_("label_help_authentication", default="Registration"),
        description=_(
            "help_authentication",
            default="This text should explain how to register and login.",
        ),
        required=True,
    )
    directives.widget(authentication=WysiwygFieldWidget)

    sessions = HtmlText(
        title=_("label_help_sessions", default="Carrying out your risk assessment"),
        description=_(
            "help_sessions",
            default="This text should describe the main functions of the OiRA Tool.",
        ),
        required=True,
    )
    directives.widget(sessions=WysiwygFieldWidget)

    preparation = HtmlText(
        title=_("label_help_preparation", default="1. Preparation"),
        description=_(
            "help_preparation",
            default="This text should explain the 2 types of profile questions.",
        ),
        required=True,
    )
    directives.widget(preparation=WysiwygFieldWidget)

    identification = HtmlText(
        title=_("label_help_identification", default="2. Identification"),
        description=_(
            "help_identification",
            default="This text should explain how the risk identification works.",
        ),
        required=True,
    )
    directives.widget(identification=WysiwygFieldWidget)

    evaluation = HtmlText(
        title=_("label_help_evaluation", default="3. Evaluation"),
        description=_(
            "help_evaluation",
            default="This text should explain how to evaluate the identified risks.",
        ),
        required=True,
    )
    directives.widget(evaluation=WysiwygFieldWidget)

    actionplan = HtmlText(
        title=_("label_help_actionplan", default="4. Action Plan"),
        description=_(
            "help_actionplan",
            default="This text should explain how to fill in the Action plan.",
        ),
        required=True,
    )
    directives.widget(actionplan=WysiwygFieldWidget)

    report = HtmlText(
        title=_("label_help_reports", default="5. Report"),
        description=_(
            "help_reports",
            default="This text should describe how the report can either be saved or printed.",  # noqa: E501
        ),
        required=True,
    )
    directives.widget(report=WysiwygFieldWidget)

    finalwords = HtmlText(
        title=_("label_help_finalwords", default="What happens next?"),
        description=_("help_finalwords", default="General final recommendations."),
        required=True,
    )
    directives.widget(finalwords=WysiwygFieldWidget)


@indexer(IOnlineHelp)
def SearchableTextIndexer(obj):
    """Index the introduction, authentication, sessions, identification,
    evaluation, actionplan, report and finalwords."""
    return " ".join(
        [
            StripMarkup(obj.introduction),
            StripMarkup(obj.authentication),
            StripMarkup(obj.sessions),
            StripMarkup(obj.identification),
            StripMarkup(obj.evaluation),
            StripMarkup(obj.actionplan),
            StripMarkup(obj.report),
            StripMarkup(obj.finalwords),
        ]
    )
