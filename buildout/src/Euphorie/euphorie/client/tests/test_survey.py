from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_parent
from euphorie.client.survey import SurveyPublishTraverser
from euphorie.client import model
from euphorie.client.tests.database import DatabaseTests


class TraversalTests(DatabaseTests):
    def createSqlData(self):
        from z3c.saconfig import Session
        self.session=Session()
        account=model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey=model.SurveySession(title=u"Survey", zodb_path="survey", account=account)
        self.session.add(self.survey)
        self.session.flush()
        self.mod1=self.survey.addChild(model.Module(
            title=u"module 1", module_id="1", zodb_path="a"))
        self.q1=self.mod1.addChild(model.Risk(
            title=u"question 1", risk_id="1", zodb_path="a/b"))
        self.session.flush()

    def testFindSqlContext_UnknownPath(self):
        self.createSqlData()
        traverser=SurveyPublishTraverser(None, None)
        zodb_path=["not", "found"]
        result=traverser.findSqlContext(self.survey.id, None, zodb_path)
        self.failUnless(result is None)
        self.assertEqual(zodb_path, ["not", "found"])

    def testFindSqlContext_OneStepPath(self):
        self.createSqlData()
        traverser=SurveyPublishTraverser(None, None)
        zodb_path=["1"]
        result=traverser.findSqlContext(self.survey.id, None, zodb_path)
        self.assertEqual(result, self.mod1.id)
        self.assertEqual(zodb_path, [])

    def testFindSqlContext_TwoStepPath(self):
        self.createSqlData()
        traverser=SurveyPublishTraverser(None, None)
        zodb_path=["1", "1"]
        result=traverser.findSqlContext(self.survey.id, None, zodb_path)
        self.assertEqual(result, self.q1.id)
        self.assertEqual(zodb_path, [])

    def testFindSqlContext_KeepNonNumericElements(self):
        self.createSqlData()
        traverser=SurveyPublishTraverser(None, None)
        zodb_path=["oops", "1"]
        result=traverser.findSqlContext(self.survey.id, None, zodb_path)
        self.assertEqual(result, self.mod1.id)
        self.assertEqual(zodb_path, ["oops"])

    def testFindSqlContext_KeepSessionsApart(self):
        self.createSqlData()
        account=model.Account(loginname=u"john", password=u"jane")
        self.session.add(account)
        survey2=model.SurveySession(title=u"Survey", zodb_path="survey", account=account)
        self.session.add(survey2)
        self.session.flush()
        traverser=SurveyPublishTraverser(None, None)
        zodb_path=["1"]
        result=traverser.findSqlContext(survey2.id, None, zodb_path)
        self.failUnless(result is None)

    def testSetupContext_OneStep(self):
        self.createSqlData()
        root=model.BaseObject()
        traverser=SurveyPublishTraverser(root, None)
        context=traverser.setupContext(self.mod1.id)
        self.assertEqual(len(aq_chain(context)), 2)
        self.failUnless(aq_base(context) is self.mod1)
        self.failUnless(aq_base(aq_parent(context)) is root)

    def testSetupContext_TwoSteps(self):
        from euphorie.client.survey import PathGhost
        self.createSqlData()
        root=model.BaseObject()
        traverser=SurveyPublishTraverser(root, None)
        context=traverser.setupContext(self.q1.id)
        self.assertEqual(len(aq_chain(context)), 3)
        self.failUnless(aq_base(context) is self.q1)
        parent=aq_parent(context)
        self.failUnless(isinstance(parent, PathGhost))
        self.assertEqual(parent.id, "1")
        self.failUnless(aq_base(aq_parent(aq_parent(context))) is root)

