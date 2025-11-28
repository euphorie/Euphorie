from .fti import ConditionalDexterityFTI
from .fti import IConstructionFilter
from euphorie.content import MessageFactory as _
from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class ITrainingQuestion(model.Schema):
    """A simple schema that adds three answer fields to the content type."""

    title = schema.Text(title=_("Question"))
    right_answer = schema.Text(title=_("Right answer"))
    wrong_answer_1 = schema.Text(title=_("First wrong answer"))
    wrong_answer_2 = schema.Text(title=_("Second wrong answer"))


@implementer(ITrainingQuestion)
class TrainingQuestion(Container):
    """A Question for the training."""


@adapter(ConditionalDexterityFTI, Interface)
@implementer(IConstructionFilter)
class ConstructionFilter:
    """FTI construction filter for :py:class:`TrainingQuestion` objects. This
    filter prevents creating Training Questions if the OiRA Tool is not
    configured to provide online taining.

    This multi adapter requires the use of the conditional FTI as implemented
    by :py:class:`euphorie.content.fti.ConditionalDexterityFTI`.
    """

    def __init__(self, fti, container):
        self.fti = fti
        self.container = container

    def allowed(self):
        if not api.portal.get_registry_record(
            "euphorie.use_training_module", default=False
        ):
            return False
        return getattr(self.container, "enable_test_questions", False)
