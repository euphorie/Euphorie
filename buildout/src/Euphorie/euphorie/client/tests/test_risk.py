import unittest


class EvaluationViewTests(unittest.TestCase):
    def EvaluationView(self, **kw):
        from euphorie.client.model import Risk
        from euphorie.client.risk import EvaluationView
        return EvaluationView(Risk(**kw), None)

    def Risk(self, **kw):
        from euphorie.content.risk import Risk
        return Risk(**kw)

    def reply(self, freq, effect):
        from euphorie.content.risk import IFrenchEvaluation

        def get(voc, token):
            vocabulary = IFrenchEvaluation[voc].vocabulary
            return vocabulary.getTermByToken(token).value

        return {"frequency": get("default_frequency", freq),
                "severity": get("default_severity", effect)}

    def test_calculatePriority_kinney_nothing_set(self):
        view = self.EvaluationView()
        risk = self.Risk(evaluation_algorithm=u"kinney")
        self.assertEqual(view.calculatePriority(risk, {}), None)

    def test_calculatePriority_french_nothing_set(self):
        view = self.EvaluationView()
        risk = self.Risk(evaluation_algorithm=lambda: u"french")
        self.assertEqual(view.calculatePriority(risk, {}), None)

    def test_calculatePriority_matrix(self):
        view = self.EvaluationView()
        risk = self.Risk(evaluation_algorithm=lambda: u"french")
        # Risks with weak severty are always low priority
        for freq in ["rare", "not-often", "often", "regularly"]:
            self.assertEqual(
                    view.calculatePriority(risk, self.reply(freq, "weak")),
                    "low")
        # High priority items
        self.assertEqual(
            view.calculatePriority(risk, self.reply("often", "severe")),
            "high")
        self.assertEqual(
            view.calculatePriority(risk, self.reply("often", "very-severe")),
            "high")
        self.assertEqual(
            view.calculatePriority(risk, self.reply("regularly", "severe")),
            "high")
        self.assertEqual(
            view.calculatePriority(risk,
                self.reply("regularly", "very-severe")),
            "high")
        # Some medium priority items
        self.assertEqual(
            view.calculatePriority(risk, self.reply("rare", "very-severe")),
            "medium")
        self.assertEqual(
            view.calculatePriority(risk,
                self.reply("not-often", "not-severe")),
            "medium")
