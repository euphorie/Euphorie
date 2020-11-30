"""
Survey Group
------------

A Survey Group is a container for several Survey versions.

https://admin.oiraproject.eu/sectors/eu/eu-private-security/private-security-eu
"""

from .. import MessageFactory as _
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.directives import dexterity
from plone.directives import form
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


log = logging.getLogger(__name__)


class ISurveyGroup(form.Schema, IBasic):
    title = schema.TextLine(
        title=_("label_title", default=u"Title"),
        description=_(
            "help_surveygroup_title",
            default=u"The title of this OiRA Tool. This title is used in "
            u"the OiRA Tool overview in the clients.",
        ),
        required=True,
    )
    form.order_before(title="*")

    form.omitted("description")

    obsolete = schema.Bool(
        title=_("label_survey_obsolete", default=u"Obsolete OiRA tool"),
        description=_(
            "help_survey_obsolete",
            default=u"This OiRA Tool is obsolete; it has been retired or "
            u"replaced with another OiRA Tool.",
        ),
        default=False,
        required=False,
    )

    form.omitted(IEditForm, "evaluation_algorithm")
    evaluation_algorithm = schema.Choice(
        title=_("label_survey_evaluation_algorithm", default=u"Evaluation algorithm"),
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(
                    u"kinney",
                    title=_("algorithm_kinney", default=u"Standard three criteria"),
                ),
                SimpleTerm(
                    u"french", title=_("french", default=u"Simplified two criteria")
                ),
            ]
        ),
        default=u"kinney",
        required=True,
    )


class SurveyGroup(dexterity.Container):
    """
    A Survey Group is a container for several Survey versions
    """

    grok.name("euphorie.surveygroup")
    implements(ISurveyGroup)

    published = None
    evaluation_algorithm = u"kinney"
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
