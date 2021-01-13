# coding=utf-8

from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_parent
from euphorie.client import model
from euphorie.client.model import SurveyTreeItem
from euphorie.ghost import PathGhost
from euphorie.testing import EuphorieIntegrationTestCase
from sqlalchemy import sql
from z3c.saconfig import Session


def build_tree_aq_chain(root, tree_id):
    """Build an acquisition context for a tree node.
    XXX This uses the path ghost and is obsolete
    """
    tail = Session.query(SurveyTreeItem).get(tree_id)
    walker = root
    path = tail.path
    while len(path) > 3:
        id = str(int(path[:3]))
        path = path[3:]
        walker = PathGhost(id).__of__(walker)
    return tail.__of__(walker)


def find_sql_context(session_id, zodb_path):
    """Find the closest SQL tree node for a candidate path.
    The path has to be given as a list of path entries. The session
    timestamp is only used as part of a cache key for this method.
    The return value is the id of the SQL tree node. All consumed
    entries will be removed from the zodb_path list.
    XXX This uses the path ghost and is obsolete
    """
    # Pop all integer elements from the URL
    path = ""
    head = []
    while zodb_path:
        next = zodb_path.pop()
        if len(next) > 3:
            zodb_path.append(next)
            break

        try:
            path += "%03d" % int(next)
            head.append(next)
        except ValueError:
            zodb_path.append(next)
            break

    # Try and find a SQL tree node that matches our URL
    query = (
        Session.query(SurveyTreeItem)
        .filter(SurveyTreeItem.session_id == session_id)
        .filter(SurveyTreeItem.path == sql.bindparam("path"))
    )
    while path:
        node = query.params(path=path).first()
        if node is not None:
            return node
        path = path[:-3]
        zodb_path.append(head.pop())


class find_sql_context_tests(EuphorieIntegrationTestCase):
    def find_sql_context(self, *a, **kw):
        return find_sql_context(*a, **kw)

    def createSqlData(self):
        self.session = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey = model.SurveySession(
            title=u"Survey", zodb_path="survey", account=account
        )
        self.session.add(self.survey)
        self.session.flush()
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.session.flush()

    def test_unknown_path(self):
        self.createSqlData()
        zodb_path = ["not", "found"]
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertTrue(result is None)
        self.assertEqual(zodb_path, ["not", "found"])

    def test_one_step_path(self):
        self.createSqlData()
        zodb_path = ["1"]
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertEqual(result.id, self.mod1.id)
        self.assertEqual(zodb_path, [])

    def test_two_step_path(self):
        self.createSqlData()
        zodb_path = ["1", "1"]
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertEqual(result.id, self.q1.id)
        self.assertEqual(zodb_path, [])

    def test_keep_non_numeric_elements(self):
        self.createSqlData()
        zodb_path = ["oops", "1"]
        result = self.find_sql_context(self.survey.id, zodb_path)
        self.assertEqual(result.id, self.mod1.id)
        self.assertEqual(zodb_path, ["oops"])

    def test_keep_sessions_apart(self):
        self.createSqlData()
        account = model.Account(loginname=u"john", password=u"jane")
        self.session.add(account)
        survey2 = model.SurveySession(
            title=u"Survey", zodb_path="survey", account=account
        )
        self.session.add(survey2)
        self.session.flush()
        zodb_path = ["1"]
        result = self.find_sql_context(survey2.id, zodb_path)
        self.assertTrue(result is None)


class build_tree_aq_chain_tests(EuphorieIntegrationTestCase):
    def build_tree_aq_chain(self, *a, **kw):
        return build_tree_aq_chain(*a, **kw)

    def createSqlData(self):
        self.session = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey = model.SurveySession(
            title=u"Survey", zodb_path="survey", account=account
        )
        self.session.add(self.survey)
        self.session.flush()
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.session.flush()

    def testSetupContext_OneStep(self):
        self.createSqlData()
        root = model.BaseObject()
        context = self.build_tree_aq_chain(root, self.mod1.id)
        self.assertEqual(len(aq_chain(context)), 2)
        self.assertTrue(aq_base(context) is self.mod1)
        self.assertTrue(aq_base(aq_parent(context)) is root)

    def testSetupContext_TwoSteps(self):
        self.createSqlData()
        root = model.BaseObject()
        context = self.build_tree_aq_chain(root, self.q1.id)
        self.assertEqual(len(aq_chain(context)), 3)
        self.assertTrue(aq_base(context) is self.q1)
        parent = aq_parent(context)
        self.assertTrue(isinstance(parent, PathGhost))
        self.assertEqual(parent.id, "1")
        self.assertTrue(aq_base(aq_parent(aq_parent(context))) is root)


class completion_percentage_tests(EuphorieIntegrationTestCase):
    def setUp(self):
        super(completion_percentage_tests, self).setUp()
        self.session = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey = model.SurveySession(
            title=u"Survey", zodb_path="survey", account=account
        )
        self.session.add(self.survey)
        self.session.flush()

    def test_no_risks(self):
        with self._get_view("webhelpers", self.portal.client) as view:
            view.update_completion_percentage(self.survey)
        self.assertEqual(self.survey.completion_percentage, 0)

    def test_half_complete(self):
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.q2 = self.mod1.addChild(
            model.Risk(title=u"question 2", risk_id="2", zodb_path="a/c")
        )
        self.session.flush()

        self.q1.postponed = False
        self.q1.identification = "no"

        with self._get_view("webhelpers", self.portal.client) as view:
            view.update_completion_percentage(self.survey)
        self.assertEqual(self.survey.completion_percentage, 50)

    def test_two_thirds_complete(self):
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.q2 = self.mod1.addChild(
            model.Risk(title=u"question 2", risk_id="2", zodb_path="a/c")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title=u"module 2", module_id="2", zodb_path="k")
        )
        self.q21 = self.mod1.addChild(
            model.Risk(title=u"question 3", risk_id="3", zodb_path="k/l")
        )
        self.session.flush()

        self.q1.postponed = False
        self.q1.identification = "n/a"
        self.q21.postponed = False
        self.q21.identification = "yes"

        with self._get_view("webhelpers", self.portal.client) as view:
            view.update_completion_percentage(self.survey)
        self.assertEqual(self.survey.completion_percentage, 67)

    def test_optional_module(self):
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title=u"module 2", module_id="2", zodb_path="k")
        )
        self.q2 = self.mod2.addChild(
            model.Risk(title=u"question 2", risk_id="2", zodb_path="k/c")
        )
        self.q1.postponed = False
        self.q1.identification = "yes"
        self.mod2.skip_children = True

        with self._get_view("webhelpers", self.portal.client) as view:
            view.update_completion_percentage(self.survey)
        self.assertEqual(self.survey.completion_percentage, 100)

    def test_optional_submodule(self):
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title=u"module 2", module_id="2", zodb_path="k")
        )
        self.mod21 = self.mod2.addChild(
            model.Module(title=u"module 3", module_id="3", zodb_path="k/c")
        )
        self.q2 = self.mod21.addChild(
            model.Risk(title=u"question 2", risk_id="2", zodb_path="k/c/u")
        )
        self.q1.postponed = False
        self.q1.identification = "yes"
        self.mod21.skip_children = True

        with self._get_view("webhelpers", self.portal.client) as view:
            view.update_completion_percentage(self.survey)
        self.assertEqual(self.survey.completion_percentage, 100)

    def test_optional_module_with_submodule(self):
        self.mod1 = self.survey.addChild(
            model.Module(title=u"module 1", module_id="1", zodb_path="a")
        )
        self.q1 = self.mod1.addChild(
            model.Risk(title=u"question 1", risk_id="1", zodb_path="a/b")
        )
        self.mod2 = self.survey.addChild(
            model.Module(title=u"module 2", module_id="2", zodb_path="k")
        )
        self.mod21 = self.mod2.addChild(
            model.Module(title=u"module 3", module_id="3", zodb_path="k/c")
        )
        self.q2 = self.mod21.addChild(
            model.Risk(title=u"question 2", risk_id="2", zodb_path="k/c/u")
        )

        self.q1.postponed = False
        self.q1.identification = "yes"
        self.mod2.skip_children = True
        self.mod21.skip_children = False
        with self._get_view("webhelpers", self.portal.client) as view:
            view.update_completion_percentage(self.survey)
        self.assertEqual(self.survey.completion_percentage, 100)
