from euphorie.client import model
from euphorie.testing import EuphorieIntegrationTestCase
from z3c.saconfig import Session


class completion_percentage_tests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.session = Session()
        account = model.Account(loginname="jane", password="secret")
        self.session.add(account)
        self.survey = model.SurveySession(
            title="Survey", zodb_path="survey", account=account
        )
        self.session.add(self.survey)
        self.session.flush()

    def test_no_risks(self):
        self.assertEqual(self.survey.completion_percentage, 0)

    def test_half_complete(self):
        self.mod1 = self.survey.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title="question 1", risk_id="1", zodb_path="a/b")
        )
        self.q2 = self.mod1.addChild(
            model.Risk(title="question 2", risk_id="2", zodb_path="a/c")
        )
        self.session.flush()

        self.q1.postponed = False
        self.q1.identification = "no"

        self.assertEqual(self.survey.completion_percentage, 50)

    def test_two_thirds_complete(self):
        self.mod1 = self.survey.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title="question 1", risk_id="1", zodb_path="a/b")
        )
        self.q2 = self.mod1.addChild(
            model.Risk(title="question 2", risk_id="2", zodb_path="a/c")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title="module 2", module_id="2", zodb_path="k")
        )
        self.q21 = self.mod1.addChild(
            model.Risk(title="question 3", risk_id="3", zodb_path="k/l")
        )
        self.session.flush()

        self.q1.postponed = False
        self.q1.identification = "n/a"
        self.q21.postponed = False
        self.q21.identification = "yes"

        self.assertEqual(self.survey.completion_percentage, 67)

    def test_optional_module(self):
        self.mod1 = self.survey.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title="question 1", risk_id="1", zodb_path="a/b")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title="module 2", module_id="2", zodb_path="k")
        )
        self.q2 = self.mod2.addChild(
            model.Risk(title="question 2", risk_id="2", zodb_path="k/c")
        )
        self.q1.postponed = False
        self.q1.identification = "yes"
        self.mod2.skip_children = True

        self.assertEqual(self.survey.completion_percentage, 100)

    def test_optional_submodule(self):
        self.mod1 = self.survey.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title="question 1", risk_id="1", zodb_path="a/b")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title="module 2", module_id="2", zodb_path="k")
        )
        self.mod21 = self.mod2.addChild(
            model.Module(title="module 3", module_id="3", zodb_path="k/c")
        )
        self.q2 = self.mod21.addChild(
            model.Risk(title="question 2", risk_id="2", zodb_path="k/c/u")
        )
        self.q1.postponed = False
        self.q1.identification = "yes"
        self.mod21.skip_children = True

        self.assertEqual(self.survey.completion_percentage, 100)

    def test_optional_module_with_submodule(self):
        self.mod1 = self.survey.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title="question 1", risk_id="1", zodb_path="a/b")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title="module 2", module_id="2", zodb_path="k")
        )
        self.mod21 = self.mod2.addChild(
            model.Module(title="module 3", module_id="3", zodb_path="k/c")
        )
        self.q2 = self.mod21.addChild(
            model.Risk(title="question 2", risk_id="2", zodb_path="k/c/u")
        )

        self.q1.postponed = False
        self.q1.identification = "yes"
        self.mod2.skip_children = True
        self.mod21.skip_children = False
        self.assertEqual(self.survey.completion_percentage, 100)
