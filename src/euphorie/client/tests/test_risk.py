from euphorie.client.model import Risk
from euphorie.client.risk import IdentificationView
from euphorie.content.risk import IFrenchEvaluation as IFr
from euphorie.content.risk import IKinneyEvaluation as IKi
from euphorie.content.survey import Survey

import mock
import unittest


class EvaluationViewTests(unittest.TestCase):

    def EvaluationView(self, **kw):
        """
        Note: the EvaluationView does not exist as a separate view any more.
        Its functionality was merged to the identification view.
        For these tests, we just keep the name EvaluationView but return
        IdentificationView, since it contains all the relevant code
        """
        return IdentificationView(Risk(**kw), None)

    def Risk(self, **kw):
        return Risk(**kw)

    def reply(self, freq, effect, prob=None):
        if prob is None:  # French
            return {
                "frequency": IFr['default_frequency'
                                 ].vocabulary.getTermByToken(freq).value,
                "severity": IFr['default_severity']
                .vocabulary.getTermByToken(effect).value,
            }
        else:  # Kinney
            return {
                "frequency": IKi['default_frequency'
                                 ].vocabulary.getTermByToken(freq).value,
                "effect": IKi['default_effect'
                              ].vocabulary.getTermByToken(effect).value,
                "probability": IKi['default_probability']
                .vocabulary.getTermByToken(prob).value,
            }

    def test_evaluation_algorithm_fallback(self):
        view = self.EvaluationView()
        risk = self.Risk()
        self.assertEqual(view.evaluation_algorithm(risk), u"kinney")

    def test_evaluation_algorithm_survey_parent(self):
        view = self.EvaluationView()
        survey = Survey()
        survey.evaluation_algorithm = u"dummy"
        risk = self.Risk().__of__(survey)
        self.assertEqual(view.evaluation_algorithm(risk), u"dummy")

    def test_calculatePriority_kinney_nothing_set(self):
        view = self.EvaluationView()
        risk = self.Risk()
        risk.evaluation_method = 'calculated'
        with mock.patch(
            'euphorie.client.risk.evaluation_algorithm', return_value='kinney'
        ):
            self.assertEqual(view.calculatePriority(risk, {}), None)

    def test_calculatePriority_french_nothing_set(self):
        view = self.EvaluationView()
        risk = self.Risk()
        risk.evaluation_method = 'calculated'
        with mock.patch(
            'euphorie.client.risk.evaluation_algorithm', return_value='french'
        ):
            self.assertEqual(view.calculatePriority(risk, {}), None)

    def test_calculatePriority_french(self):
        view = self.EvaluationView()
        with mock.patch(
            'euphorie.client.risk.evaluation_algorithm', return_value='french'
        ):
            risk = self.Risk()
            risk.evaluation_method = 'calculated'
            # Risks with weak severity are always low priority
            for freq in ["rare", "not-often", "often", "regularly"]:
                self.assertEqual(
                    view.calculatePriority(risk, self.reply(freq, "weak")),
                    "low"
                )
            # High priority items
            self.assertEqual(
                view.calculatePriority(risk, self.reply("often", "severe")),
                "high"
            )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("often", "very-severe")
                ), "high"
            )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("regularly", "severe")
                ), "high"
            )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("regularly", "very-severe")
                ), "high"
            )
            # Some medium priority items
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("rare", "very-severe")
                ), "medium"
            )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("not-often", "not-severe")
                ), "medium"
            )

    def test_calculatePriority_kinney(self):
        view = self.EvaluationView()
        risk = self.Risk()
        risk.evaluation_method = 'calculated'
        with mock.patch(
            'euphorie.client.risk.evaluation_algorithm', return_value='kinney'
        ):
            # Risks with weak severity are always low priority
            for freq in ["almost-never", "regular", "constant"]:
                self.assertEqual(
                    view.calculatePriority(
                        risk, self.reply(freq, "weak", 'small')
                    ), "low"
                )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("constant", "significant", 'medium')
                ), "high"
            )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("constant", "high", 'medium')
                ), "high"
            )
            self.assertEqual(
                view.calculatePriority(
                    risk, self.reply("constant", "weak", 'medium')
                ), "medium"
            )
