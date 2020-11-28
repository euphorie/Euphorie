# coding=utf-8
from ..risk import evaluation_algorithm
from ..risk import IFrenchEvaluation
from ..risk import IKinneyEvaluation
from ..risk import IKinneyRisk
from ..risk import IRisk
from ..solution import ISolution
from ..utils import DragDropHelper
from ..utils import getTermTitleByValue
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.memoize.instance import memoize
from Products.Five import BrowserView


class RiskView(BrowserView, DragDropHelper):
    @property
    @memoize
    def my_context(self):
        return aq_inner(self.context)

    @property
    def module_title(self):
        return aq_parent(self.context).title

    @property
    def evaluation_algorithm(self):
        return evaluation_algorithm(self.my_context)

    @property
    def risk_type(self):
        return getTermTitleByValue(IRisk["type"], self.my_context.type)

    @property
    def solutions(self):
        return [
            {
                "id": solution.id,
                "url": solution.absolute_url(),
                "description": solution.description,
            }
            for solution in self.my_context.values()
            if ISolution.providedBy(solution)
        ]

    @property
    def evaluation_method(self):
        return getTermTitleByValue(
            IRisk["evaluation_method"], self.my_context.evaluation_method
        )

    @property
    def default_priority(self):
        return getTermTitleByValue(
            IKinneyRisk["default_priority"], self.my_context.default_priority
        )

    @property
    def default_severity(self):
        return getTermTitleByValue(
            IFrenchEvaluation["default_severity"], self.my_context.default_severity
        )

    @property
    def default_frequency(self):
        if self.evaluation_algorithm == u"french":
            return getTermTitleByValue(
                IFrenchEvaluation["default_frequency"],
                self.my_context.default_frequency,
            )
        else:
            return getTermTitleByValue(
                IKinneyEvaluation["default_frequency"],
                self.my_context.default_frequency,
            )

    @property
    def default_probability(self):
        return getTermTitleByValue(
            IKinneyEvaluation["default_probability"],
            self.my_context.default_probability,
        )

    @property
    def default_effect(self):
        return getTermTitleByValue(
            IKinneyEvaluation["default_effect"], self.my_context.default_effect
        )
