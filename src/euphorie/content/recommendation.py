from .. import MessageFactory as _
from euphorie.htmllaundry.z3cform import HtmlText
from plone.autoform import directives
from plone.supermodel import model
from plonetheme.nuplone.z3cform.widget import WysiwygFieldWidget


class IRecommendation(model.Schema):
    """ """

    text = HtmlText(
        title=_("label_recommendation_text", "Text"),
        description=_(
            "help_recommendation_text",
            default="Text to be included in the report",
        ),
        required=False,
    )
    directives.widget(text=WysiwygFieldWidget)
