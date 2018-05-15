# coding=utf-8
from euphorie.client import model
from euphorie.client import navigation
from euphorie.client.risk import ActionPlanView
from euphorie.client.tests.utils import createSurvey
from euphorie.testing import EuphorieIntegrationTestCase

import unittest


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
        child = model.Risk(title=u"Risk", risk_id="1", zodb_path="1")
        survey.addChild(child)
        self.failUnless(navigation.FindNextQuestion(child, survey) is None)

    def test_Question_at_same_level_as_module(self):
        (session, survey) = createSurvey()
        session.add(survey)
        child = model.Risk(title=u"Risk", risk_id="1", zodb_path="1")
        survey.addChild(child)
        sister = model.Risk(title=u"Risk", risk_id="2", zodb_path="2")
        survey.addChild(sister)
        self.failUnless(navigation.FindNextQuestion(child, survey) is sister)

    def testQuestionIsNextModule(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(title=u"Module 1", module_id="1", zodb_path="1")
        survey.addChild(mod1)
        q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/2")
        mod1.addChild(q1)
        mod2 = model.Module(
            title=u"Module 2",
            module_id="2",
            zodb_path="2",
            has_description=True
        )
        survey.addChild(mod2)
        self.failUnless(navigation.FindNextQuestion(q1, survey) is mod2)

    def testSkipChildren(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            skip_children=True
        )
        survey.addChild(mod1)
        q1 = model.Risk(
            title=u"Risk 1",
            risk_id="1",
            zodb_path="1/1",
            has_description=True
        )
        mod1.addChild(q1)
        mod2 = model.Module(
            title=u"Module 2",
            module_id="2",
            zodb_path="2",
            has_description=True
        )
        survey.addChild(mod2)
        self.failUnless(navigation.FindNextQuestion(mod1, survey) is mod2)

    def test_ignore_module_without_description(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(title=u"Module 1", module_id="1", zodb_path="1")
        survey.addChild(mod1)
        q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1")
        mod1.addChild(q1)
        mod2 = model.Module(
            title=u"Module 2",
            module_id="2",
            zodb_path="2",
            has_description=False
        )
        survey.addChild(mod2)
        mod3 = model.Module(
            title=u"Module 3",
            module_id="3",
            zodb_path="3",
            has_description=True
        )
        survey.addChild(mod3)
        self.failUnless(navigation.FindNextQuestion(q1, survey) is mod3)


class FindPreviousQuestionTests(EuphorieIntegrationTestCase):

    def testSingleQuestion(self):
        (session, survey) = createSurvey()
        child = model.Risk(title=u"Risk", risk_id="1", zodb_path="1")
        survey.addChild(child)
        self.failUnless(navigation.FindPreviousQuestion(child, survey) is None)

    def testQuestionAtSameModule(self):
        (session, survey) = createSurvey()
        child = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1")
        survey.addChild(child)
        sister = model.Risk(title=u"Risk 2", risk_id="2", zodb_path="2")
        survey.addChild(sister)
        self.failUnless(
            navigation.FindPreviousQuestion(sister, survey) is child
        )

    def testQuestionAtPreviousModule(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(title=u"Module 1", module_id="1", zodb_path="1")
        survey.addChild(mod1)
        q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1")
        mod1.addChild(q1)
        mod2 = model.Module(title=u"Module 2", module_id="2", zodb_path="2")
        survey.addChild(mod2)
        self.failUnless(navigation.FindPreviousQuestion(mod2, survey) is q1)

    def testQuestionAtPreviousModuleWithSkippedChildren(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            has_description=True,
            skip_children=True
        )
        survey.addChild(mod1)
        q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1")
        mod1.addChild(q1)
        mod2 = model.Module(title=u"Module 2", module_id="2", zodb_path="2")
        survey.addChild(mod2)
        self.failUnless(navigation.FindPreviousQuestion(mod2, survey) is mod1)

    def test_skip_module_without_description(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            has_description=True
        )
        survey.addChild(mod1)
        q1 = model.Risk(title=u"Risk 1", risk_id="1", zodb_path="1/1")
        mod1.addChild(q1)
        mod2 = model.Module(
            title=u"Module 2",
            module_id="2",
            zodb_path="2",
            has_description=False
        )
        survey.addChild(mod2)
        mod3 = model.Module(title=u"Module 3", module_id="3", zodb_path="3")
        survey.addChild(mod3)
        self.failUnless(navigation.FindPreviousQuestion(mod3, survey) is q1)


class ActionPlanNavigationTests(EuphorieIntegrationTestCase):
    """Test if the filter determining which modules and risks to show during
    the action plan phase are correct.
    """

    def filter(self):
        return ActionPlanView.question_filter

    def testSkipModuleWithoutRisks(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            skip_children=False
        )
        survey.addChild(mod1)
        mod11 = model.Module(
            title=u"Module 1.1",
            module_id="11",
            zodb_path="1/1",
            skip_children=False
        )
        mod1.addChild(mod11)
        self.assertEqual(
            navigation.FindNextQuestion(mod1, survey, self.filter()), None
        )

    def testSkipModuleIfNoRisksPresent(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            skip_children=False
        )
        survey.addChild(mod1)
        mod11 = model.Module(
            title=u"Module 1.1",
            module_id="11",
            zodb_path="1/1",
            skip_children=False
        )
        mod1.addChild(mod11)
        q111 = model.Risk(
            title=u"Risk 1.1.1",
            risk_id="1",
            zodb_path="1/1/1",
            identification="yes"
        )
        mod11.addChild(q111)
        self.assertEqual(
            navigation.FindNextQuestion(mod1, survey, self.filter()), None
        )

    def testShowModuleWithTop5RiskEvenIfNotPresent(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u'Module 1',
            module_id='1',
            zodb_path='1',
            skip_children=False
        )
        survey.addChild(mod1)
        mod11 = model.Module(
            title=u'Module 1.1',
            module_id='11',
            zodb_path='1/1',
            skip_children=False,
            has_description=True
        )
        mod1.addChild(mod11)
        q111 = model.Risk(
            title=u'Risk 1.1.1',
            risk_id='1',
            zodb_path='1/1/1',
            identification='yes',
            risk_type='top5'
        )
        mod11.addChild(q111)
        self.failUnless(
            navigation.FindNextQuestion(mod1, survey, self.filter()) is mod11
        )

    def testSkipRiskIfNotPresent(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            skip_children=False
        )
        survey.addChild(mod1)
        q11 = model.Risk(
            title=u"Risk 1.1",
            risk_id="1",
            zodb_path="1/1",
            identification="yes"
        )
        mod1.addChild(q11)
        self.assertEqual(
            navigation.FindNextQuestion(mod1, survey, self.filter()), None
        )

    def testShowTop5RiskEvenIfNotPresent(self):
        (session, survey) = createSurvey()
        mod1 = model.Module(
            title=u"Module 1",
            module_id="1",
            zodb_path="1",
            skip_children=False
        )
        survey.addChild(mod1)
        q11 = model.Risk(
            title=u"Risk 1.1",
            risk_id="1",
            zodb_path="1/1",
            identification="yes",
            risk_type="top5"
        )
        mod1.addChild(q11)
        self.failUnless(
            navigation.FindNextQuestion(mod1, survey, self.filter()) is q11
        )


class GetTreeDataTests(EuphorieIntegrationTestCase):

    def createSqlData(self):
        self.request = MockRequest()
        (self.session, self.survey) = createSurvey()
        self.survey.restrictedTraverse = lambda x: None
        self.request.survey = self.survey
        self.survey.absolute_url = lambda self=None: "http://nohost"
        self.session.flush()
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.session.flush()

    def testMinimalTree(self):
        self.createSqlData()
        data = navigation.getTreeData(self.request, self.q1)
        self.failUnless(isinstance(data, dict))
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
        self.assertEqual(mod1["url"], "http://nohost/identification/1")
        self.assertEqual(len(mod1["children"]), 1)
        q1 = mod1["children"][0]
        self.assertEqual(q1["id"], self.q1.id)
        self.assertEqual(q1["type"], "risk")
        self.assertEqual(q1["number"], "1.1")
        self.assertEqual(q1["title"], "question 1")
        self.assertEqual(q1["current"], True)
        self.assertEqual(q1["active"], False)
        self.assertEqual(q1["class"], "current")
        self.assertEqual(q1["url"], "http://nohost/identification/1/1")
        self.assertEqual(len(q1["children"]), 0)

    def testIncludeRisksChildrenOfModule(self):
        self.createSqlData()
        data = navigation.getTreeData(self.request, self.mod1)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 1)
        self.assertEqual(mod1_data["leaf_module"], True)

    def testIncludeRisksChildrenOfModuleUnlessSkipped(self):
        self.createSqlData()
        self.mod1.skip_children = True
        data = navigation.getTreeData(self.request, self.mod1)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 0)
        self.assertEqual(mod1_data["leaf_module"], False)

    def test_list_sibling_modules_of_parent_if_risk(self):
        self.createSqlData()
        self.mod1.removeChildren()
        mod11 = self.mod1.addChild(
            model.Module(title=u"module 1.1", module_id="11", zodb_path="a/a")
        )
        mod12 = self.mod1.addChild(
            model.Module(title=u"module 1.2", module_id="12", zodb_path="a/b")
        )
        q111 = mod11.addChild(
            model.Risk(
                title=u"question 1.1.1", risk_id="111", zodb_path="a/b/c"
            )
        )
        data = navigation.getTreeData(self.request, q111)
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
            model.Module(title=u"module 1.1", module_id="11", zodb_path="a/a")
        )
        q111 = mod11.addChild(
            model.Risk(
                title=u"question 1.1.1", risk_id="111", zodb_path="a/a/a"
            )
        )
        self.mod1.addChild(
            model.Risk(title=u"question 1.2", risk_id="12", zodb_path="a/b")
        )
        data = navigation.getTreeData(self.request, q111)
        mod1_data = data["children"][0]
        self.assertEqual(len(mod1_data["children"]), 1)
        self.assertEqual(mod1_data["children"][0]["id"], mod11.id)

    def testListRootSiblingModules(self):
        self.createSqlData()
        self.mod1.removeChildren()
        mod11 = self.mod1.addChild(
            model.Module(title=u"module 1.1", module_id="11", zodb_path="a/a")
        )
        q111 = mod11.addChild(
            model.Risk(
                title=u"question 1.1.1", risk_id="111", zodb_path="a/a/a"
            )
        )
        mod2 = self.survey.addChild(
            model.Module(title=u"module 2", module_id="2", zodb_path="b")
        )
        data = navigation.getTreeData(self.request, q111)
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
        self.assertEqual(navigation.first(lambda x: x, xrange(5)), 1)
