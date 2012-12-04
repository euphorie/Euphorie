from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_parent
from euphorie.client import model
from euphorie.client.tests.database import DatabaseTests


class find_sql_context_tests(DatabaseTests):
    def find_sql_context(self, *a, **kw):
        from euphorie.client.survey import find_sql_context
        return find_sql_context(*a, **kw)

    def createSqlData(self):
        from z3c.saconfig import Session
        self.session = Session()
        account = model.Account(loginname=u'jane', password=u'secret')
        self.session.add(account)
        self.survey = model.SurveySession(title=u'Survey', zodb_path='survey',
                account=account)
        self.session.add(self.survey)
        self.session.flush()
        self.mod1 = self.survey.addChild(model.Module(
            title=u'module 1', module_id='1', zodb_path='a'))
        self.q1 = self.mod1.addChild(model.Risk(
            title=u'question 1', risk_id='1', zodb_path='a/b'))
        self.session.flush()

    def test_unknown_path(self):
        self.createSqlData()
        zodb_path = ['not', 'found']
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.failUnless(result is None)
        self.assertEqual(zodb_path, ['not', 'found'])

    def test_one_step_path(self):
        self.createSqlData()
        zodb_path = ['1']
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertEqual(result, self.mod1.id)
        self.assertEqual(zodb_path, [])

    def test_two_step_path(self):
        self.createSqlData()
        zodb_path = ['1', '1']
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertEqual(result, self.q1.id)
        self.assertEqual(zodb_path, [])

    def test_keep_non_numeric_elements(self):
        self.createSqlData()
        zodb_path = ['oops', '1']
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertEqual(result, self.mod1.id)
        self.assertEqual(zodb_path, ["oops"])

    def test_keep_sessions_apart(self):
        self.createSqlData()
        account = model.Account(loginname=u'john', password=u'jane')
        self.session.add(account)
        survey2 = model.SurveySession(title=u'Survey', zodb_path='survey',
                account=account)
        self.session.add(survey2)
        self.session.flush()
        zodb_path = ['1']
        result = self.find_sql_context(survey2.id, zodb_path)
        self.failUnless(result is None)


class build_tree_aq_chain_tests(DatabaseTests):
    def build_tree_aq_chain(self, *a, **kw):
        from euphorie.client.survey import build_tree_aq_chain
        return build_tree_aq_chain(*a, **kw)

    def createSqlData(self):
        from z3c.saconfig import Session
        self.session = Session()
        account = model.Account(loginname=u'jane', password=u'secret')
        self.session.add(account)
        self.survey = model.SurveySession(title=u'Survey', zodb_path='survey',
                account=account)
        self.session.add(self.survey)
        self.session.flush()
        self.mod1 = self.survey.addChild(model.Module(
            title=u'module 1', module_id='1', zodb_path='a'))
        self.q1 = self.mod1.addChild(model.Risk(
            title=u'question 1', risk_id='1', zodb_path='a/b'))
        self.session.flush()

    def testSetupContext_OneStep(self):
        self.createSqlData()
        root = model.BaseObject()
        context = self.build_tree_aq_chain(root, self.mod1.id)
        self.assertEqual(len(aq_chain(context)), 2)
        self.failUnless(aq_base(context) is self.mod1)
        self.failUnless(aq_base(aq_parent(context)) is root)

    def testSetupContext_TwoSteps(self):
        from euphorie.ghost import PathGhost
        self.createSqlData()
        root = model.BaseObject()
        context = self.build_tree_aq_chain(root, self.q1.id)
        self.assertEqual(len(aq_chain(context)), 3)
        self.failUnless(aq_base(context) is self.q1)
        parent = aq_parent(context)
        self.failUnless(isinstance(parent, PathGhost))
        self.assertEqual(parent.id, '1')
        self.failUnless(aq_base(aq_parent(aq_parent(context))) is root)
