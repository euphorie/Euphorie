"""
Survey Group
------------

A Survey Group is a container for several Survey versions.

https://admin.oiraproject.eu/sectors/eu/eu-private-security/private-security-eu
"""

from .. import MessageFactory as _
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


log = logging.getLogger(__name__)


class RichTerm(SimpleTerm):
    def __init__(
        self, value, token=None, title=None, description=None, extra_help=None
    ):
        super().__init__(value, token, title)
        self.description = description
        self.extra_help = extra_help


class ISurveyGroup(model.Schema, IBasic):
    title = schema.TextLine(
        title=_("label_title", default="Title"),
        description=_(
            "help_surveygroup_title",
            default="The title of this OiRA Tool. This title is used in "
            "the OiRA Tool overview in the clients.",
        ),
        required=True,
    )
    directives.order_before(title="*")

    directives.omitted("description")

    obsolete = schema.Bool(
        title=_("label_survey_obsolete", default="Obsolete OiRA tool"),
        description=_(
            "help_survey_obsolete",
            default="This OiRA Tool is obsolete; it has been retired or "
            "replaced with another OiRA Tool.",
        ),
        default=False,
        required=False,
    )

    directives.omitted(IEditForm, "evaluation_algorithm")
    evaluation_algorithm = schema.Choice(
        title=_("label_survey_evaluation_algorithm", default="Evaluation algorithm"),
        vocabulary=SimpleVocabulary(
            [
                RichTerm(
                    "kinney",
                    title=_("algorithm_kinney", default="Standard three criteria"),
                    description=_(
                        "This is the recommended evaluation algorithm, "
                        "based on the Kinney method"
                    ),
                    extra_help=_(
                        "help_survey_evaluation_algorithm_standard",
                        default=(
                            "This method involves risk assessment "
                            "by Severity x Exposure x Probability, "
                            "whereas these have to be understood as follows; "
                            "Severity of injury linked to hazard - "
                            "Exposure (Frequency) to the hazard - "
                            "Probability of the hazard occuring when exposed"
                        ),
                    ),
                ),
                RichTerm(
                    "french",
                    title=_("algorithm_french", default="Simplified two criteria"),
                    description=_(
                        "This is a simpler evaluation algorithm "
                        "using only two criteria."
                    ),
                    extra_help=_(
                        "help_survey_evaluation_algorithm_simplified",
                        default=(
                            "This method involves risk assessment "
                            "by Severity x Exposure, whereas these have "
                            "to be understood as follows; Severity of injury linked "
                            "to hazard - Exposure (Frequency) to the hazard"
                        ),
                    ),
                ),
            ]
        ),
        default="kinney",
        required=True,
    )


@implementer(ISurveyGroup)
class SurveyGroup(Container):
    """A Survey Group is a container for several Survey versions."""

    published = None
    evaluation_algorithm = "kinney"
    obsolete = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return op


def handleSurveyPublish(survey, event):
    """Event handler (subscriber) for succesfull workflow transitions for
    :py:obj:`ISurvey` objects. This handler performs necessary housekeeping
    tasks on the parent :py:class:`SurveyGroup`.

    If the workflow action is ``publish`` or ``update`` the ``published``
    attribute of the SurveyGroup is set to the id of the published
    survey instance.
    """
    if event.action not in ["publish", "update"]:
        return
    surveygroup = aq_parent(aq_inner(survey))
    surveygroup.published = survey.id


def handleSurveyRemoved(survey, event):
    """Event handler (subscriber) for deletion of
    :py:obj:`ISurvey` objects. This handler performs necessary houskeeping
    tasks on the parent :py:class:`SurveyGroup`.

    The 'published' attr on the surveygroup states the name of the currently
    published survey.

    If this survey gets deleted, we need to clear this attr.
    """
    parent = aq_parent(survey)
    if ISurveyGroup.providedBy(parent) and parent.published == survey.id:
        parent.published = None
