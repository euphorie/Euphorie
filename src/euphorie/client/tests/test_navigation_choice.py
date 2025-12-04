from euphorie.client import model
from euphorie.client import navigation
from euphorie.client.browser.risk import ActionPlanView
from euphorie.testing import EuphorieIntegrationTestCase

import unittest


def createSurvey():
    session = model.Session()
    account = model.Account(loginname="jane", password="secret")
    session.add(account)
    survey = model.SurveySession(
        title="Session",
        zodb_path="survey",
        account=account,
    )
    session.add(survey)
    return (session, survey)


class MockRequest:
    def __init__(self, agent=None):
        self.__headers = {}
        if agent is not None:
            self.__headers["User-Agent"] = agent

    def get_header(self, key, default):
        return self.__headers.get(key, default)


class FindNextQuestionTests(EuphorieIntegrationTestCase):
    def testSingleQuestion(self):
        (session, survey) = createSurvey()
        child = model.Choice(title="Choice", zodb_path="1")
        survey.addChild(child)
        self.assertTrue(navigation.FindNextQuestion(child, survey) is None)

    def test_Question_at_same_level_as_module(self):
        (session, survey) = createSurvey()
        session.add(survey)
        child = model.Choice(title="Choice", zodb_path="1")
        survey.addChild(child)
        sister = model.Choice(title="Choice", zodb_path="2")
        survey.addChild(sister)
        self.assertTrue(navigation.FindNextQuestion(child, survey) is sister)

    def testQuestionIsNextModule(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(title="Module 1", module_id="1", zodb_path="1")
        survey.addChild(mod1)
        c1 = model.Choice(title="Choice 1", zodb_path="1/2")
        mod1.addChild(c1)
        mod2 = model.Module(
            title="Module 2", module_id="2", zodb_path="2", has_description=True
        )
        survey.addChild(mod2)
        self.assertTrue(navigation.FindNextQuestion(c1, survey) is mod2)

    def testSkipChildren(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=True
        )
        survey.addChild(mod1)
        c1 = model.Choice(title="Choice 1", zodb_path="1/1", has_description=True)
        mod1.addChild(c1)
        mod2 = model.Module(
            title="Module 2", module_id="2", zodb_path="2", has_description=True
        )
        survey.addChild(mod2)
        self.assertTrue(navigation.FindNextQuestion(mod1, survey) is mod2)

    def test_ignore_module_without_description(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(title="Module 1", module_id="1", zodb_path="1")
        survey.addChild(mod1)
        c1 = model.Choice(title="Choice 1", zodb_path="1/1")
        mod1.addChild(c1)
        mod2 = model.Module(
            title="Module 2", module_id="2", zodb_path="2", has_description=False
        )
        survey.addChild(mod2)
        mod3 = model.Module(
            title="Module 3", module_id="3", zodb_path="3", has_description=True
        )
        survey.addChild(mod3)
        self.assertTrue(navigation.FindNextQuestion(c1, survey) is mod3)


class FindPreviousQuestionTests(EuphorieIntegrationTestCase):
    def testSingleQuestion(self):
        (session, survey) = createSurvey()
        child = model.Choice(title="Choice", zodb_path="1")
        survey.addChild(child)
        self.assertTrue(navigation.FindPreviousQuestion(child, survey) is None)

    def testQuestionAtSameModule(self):
        (session, survey) = createSurvey()
        child = model.Choice(title="Choice 1", zodb_path="1")
        survey.addChild(child)
        sister = model.Choice(title="Choice 2", zodb_path="2")
        survey.addChild(sister)
        self.assertTrue(navigation.FindPreviousQuestion(sister, survey) is child)

    def testQuestionAtPreviousModule(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(title="Module 1", module_id="1", zodb_path="1")
        survey.addChild(mod1)
        c1 = model.Choice(title="Choice 1", zodb_path="1/1")
        mod1.addChild(c1)
        mod2 = model.Module(title="Module 2", module_id="2", zodb_path="2")
        survey.addChild(mod2)
        self.assertTrue(navigation.FindPreviousQuestion(mod2, survey) is c1)

    def testQuestionAtPreviousModuleWithSkippedChildren(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title="Module 1",
            module_id="1",
            zodb_path="1",
            has_description=True,
            skip_children=True,
        )
        survey.addChild(mod1)
        c1 = model.Choice(title="Choice 1", zodb_path="1/1")
        mod1.addChild(c1)
        mod2 = model.Module(title="Module 2", module_id="2", zodb_path="2")
        survey.addChild(mod2)
        self.assertTrue(navigation.FindPreviousQuestion(mod2, survey) is mod1)

    def test_skip_module_without_description(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", has_description=True
        )
        survey.addChild(mod1)
        c1 = model.Choice(title="Choice 1", zodb_path="1/1")
        mod1.addChild(c1)
        mod2 = model.Module(
            title="Module 2", module_id="2", zodb_path="2", has_description=False
        )
        survey.addChild(mod2)
        mod3 = model.Module(title="Module 3", module_id="3", zodb_path="3")
        survey.addChild(mod3)
        self.assertTrue(navigation.FindPreviousQuestion(mod3, survey) is c1)


class ActionPlanNavigationTests(EuphorieIntegrationTestCase):
    """Test if the filter determining which modules and choices to show during
    the action plan phase are correct."""

    def filter(self):
        return ActionPlanView.question_filter

    def testSkipModuleWithoutChoices(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        survey.addChild(mod1)
        mod11 = model.Module(
            title="Module 1.1", module_id="11", zodb_path="1/1", skip_children=False
        )
        mod1.addChild(mod11)
        self.assertEqual(navigation.FindNextQuestion(mod1, survey, self.filter()), None)

    def testSkipModuleIfNoChoicesPresent(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        survey.addChild(mod1)
        mod11 = model.Module(
            title="Module 1.1", module_id="11", zodb_path="1/1", skip_children=False
        )
        mod1.addChild(mod11)
        c111 = model.Choice(title="Choice 1.1.1", zodb_path="1/1/1")
        mod11.addChild(c111)
        self.assertEqual(navigation.FindNextQuestion(mod1, survey, self.filter()), None)

    def testSkipChoiceIfNotPresent(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        survey.addChild(mod1)
        c11 = model.Choice(title="Choice 1.1", zodb_path="1/1")
        mod1.addChild(c11)
        self.assertEqual(navigation.FindNextQuestion(mod1, survey, self.filter()), None)


class GetTreeDataTests(EuphorieIntegrationTestCase):
    def createSqlData(self):
        self.request = MockRequest()
        (self.session, self.survey) = createSurvey()
        self.survey.restrictedTraverse = lambda x: None
        self.request.survey = self.survey
        self.survey.absolute_url = lambda self=None: "http://nohost"
        self.session.flush()
        self.mod1 = self.survey.addChild(
            model.Module(title="module 1", module_id="1", zodb_path="a")
        )
        self.c1 = self.mod1.addChild(model.Choice(title="question 1", zodb_path="a/b"))
        self.session.flush()

    def testMinimalTree(self):
        self.createSqlData()
        data = navigation.getTreeData(self.request, self.c1, survey=self.survey)
        self.assertTrue(isinstance(data, dict))
        children = data["children"]
        self.assertEqual(len(children), 1)
        mod1 = children[0]
        self.assertEqual(mod1["id"], self.mod1.id)
        self.assertEqual(mod1["type"], "module")
        self.assertEqual(mod1["number"], "1")
        self.assertEqual(mod1["title"], "module 1")
        self.assertEqual(mod1["current"], False)
        self.assertEqual(mod1["current_parent"], True)
        self.assertEqual(mod1["leaf_module"], True)
        self.assertEqual(mod1["active"], True)
        self.assertEqual(mod1["class"], "active current_parent")
        self.assertEqual(mod1["url"], "http://nohost/1/@@identification")
        self.assertEqual(len(mod1["children"]), 1)
        c1 = mod1["children"][0]
        self.assertEqual(c1["id"], self.c1.id)
        self.assertEqual(c1["type"], "choice")
        self.assertEqual(c1["number"], "1.1")
        self.assertEqual(c1["title"], "question 1")
        self.assertEqual(c1["current"], True)
        self.assertEqual(c1["active"], False)
        self.assertEqual(c1["class"], "current")
        self.assertEqual(c1["url"], "http://nohost/1/1/@@identification")
        self.assertEqual(len(c1["children"]), 0)

    def testIncludeChoicesChildrenOfModule(self):
        self.createSqlData()
        data = navigation.getTreeData(self.request, self.mod1, survey=self.survey)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 1)
        self.assertEqual(mod1_data["leaf_module"], True)

    def testIncludeChoicesChildrenOfModuleUnlessSkipped(self):
        self.createSqlData()
        self.mod1.skip_children = True
        data = navigation.getTreeData(self.request, self.mod1, survey=self.survey)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 0)
        self.assertEqual(mod1_data["leaf_module"], False)

    def test_list_sibling_modules_of_parent_if_choice(self):
        self.createSqlData()
        self.mod1.removeChildren()
        mod11 = self.mod1.addChild(
            model.Module(title="module 1.1", module_id="11", zodb_path="a/a")
        )
        mod12 = self.mod1.addChild(
            model.Module(title="module 1.2", module_id="12", zodb_path="a/b")
        )
        c111 = mod11.addChild(model.Choice(title="question 1.1.1", zodb_path="a/b/c"))
        data = navigation.getTreeData(self.request, c111, survey=self.survey)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 2)
        self.assertEqual(mod1_data["children"][0]["id"], mod11.id)
        self.assertEqual(mod1_data["children"][0]["current_parent"], True)
        self.assertEqual(mod1_data["children"][0]["current"], False)
        self.assertEqual(mod1_data["children"][0]["leaf_module"], True)
        self.assertEqual(mod1_data["children"][0]["active"], True)
        self.assertEqual(mod1_data["children"][1]["id"], mod12.id)
        self.assertEqual(mod1_data["children"][1]["current_parent"], False)
        self.assertEqual(mod1_data["children"][1]["current"], False)
        self.assertEqual(mod1_data["children"][1]["active"], False)

    def testIgnoreSiblingQuestions(self):
        self.createSqlData()
        self.mod1.removeChildren()
        mod11 = self.mod1.addChild(
            model.Module(title="module 1.1", module_id="11", zodb_path="a/a")
        )
        c111 = mod11.addChild(model.Choice(title="question 1.1.1", zodb_path="a/a/a"))
        self.mod1.addChild(model.Choice(title="question 1.2", zodb_path="a/b"))
        data = navigation.getTreeData(self.request, c111, survey=self.survey)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 1)
        self.assertEqual(mod1_data["children"][0]["id"], mod11.id)

    def testListRootSiblingModules(self):
        self.createSqlData()
        self.mod1.removeChildren()
        mod11 = self.mod1.addChild(
            model.Module(title="module 1.1", module_id="11", zodb_path="a/a")
        )
        c111 = mod11.addChild(model.Choice(title="question 1.1.1", zodb_path="a/a/a"))
        mod2 = self.survey.addChild(
            model.Module(title="module 2", module_id="2", zodb_path="b")
        )
        data = navigation.getTreeData(self.request, c111, survey=self.survey)
        self.assertEqual(len(data["children"]), 2)
        self.assertEqual(data["children"][0]["id"], self.mod1.id)
        self.assertEqual(data["children"][0]["current"], False)
        self.assertEqual(data["children"][0]["active"], True)
        self.assertEqual(data["children"][1]["id"], mod2.id)
        self.assertEqual(data["children"][1]["current"], False)
        self.assertEqual(data["children"][1]["active"], False)


class FirstTests(unittest.TestCase):
    def testNonIterableRaisesTypeError(self):
        self.assertRaises(TypeError, navigation.first, lambda x: x, None)

    def testEmptyList(self):
        self.assertEqual(navigation.first(lambda x: x, []), None)

    def testNoMatchInList(self):
        self.assertEqual(navigation.first(lambda x: x, [False]), None)

    def testMatch(self):
        self.assertEqual(navigation.first(lambda x: x, [False, True]), True)

    def testFirstMatch(self):
        self.assertEqual(navigation.first(lambda x: x, [1, 2]), 1)

    def testGenerator(self):
        self.assertEqual(navigation.first(lambda x: x, range(5)), 1)
