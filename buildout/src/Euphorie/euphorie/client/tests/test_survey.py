import unittest
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_parent
from euphorie.client.survey import AddToTree
from euphorie.client.survey import BuildSurveyTree
from euphorie.client.survey import SurveyPublishTraverser
from euphorie.client import model
from euphorie.client.tests.database import DatabaseTests

def createContainer(id, profile=False):
    from zope.interface import implements
    from euphorie.content.interfaces import IQuestionContainer
    class Container(dict):
        implements(IQuestionContainer)
        title=u"container"
        def __init__(self, id):
            self.id=id
    c=Container(id)
    if profile:
        from zope.interface import alsoProvides
        from euphorie.content.profilequestion import IProfileQuestion
        alsoProvides(c, IProfileQuestion)
    return c



def createRisk(id):
    from zope.interface import implements
    from euphorie.content.risk import IRisk
    class Risk(object):
        implements(IRisk)
        title=u"risk"
        type="risk"
        default_probability=0
        default_frequency=0
        default_effect=0

        def __init__(self, id):
            self.id=id
    return Risk(id)



class AddToTreeTests(DatabaseTests):
    def setUp(self):
        from z3c.saconfig import Session
        super(AddToTreeTests, self).setUp()
        self.session=Session()
        account=model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey=model.SurveySession(title=u"Survey", zodb_path="survey", account=account)
        self.session.add(self.survey)
        self.session.flush()
        self.root=self.survey.addChild(model.Module(title=u"test session",
            module_id="1", zodb_path="1"))

    def testAddNonInterestingNode(self):
        AddToTree(self.root, None, title="title")
        self.assertEqual(list(self.root.children()), [])


    def testAddRisk(self):
        question=createRisk("13")
        AddToTree(self.root, question)
        children=list(self.root.children())
        self.assertEqual(len(children), 1)

        child=children[0]
        self.failUnless(isinstance(child, model.Risk))
        self.assertEqual(child.title, u"risk")
        self.assertEqual(child.risk_id, "13")


    def testAddEmptyContainer(self):
        container=createContainer("13")
        AddToTree(self.root, container)
        children=list(self.root.children())
        self.assertEqual(len(children), 1)
        child=children[0]
        self.failUnless(isinstance(child, model.Module))
        self.assertEqual(child.title, u"container")
        self.assertEqual(child.module_id, "13")


    def testOverrideTitle(self):
        question=createRisk("13")
        AddToTree(self.root, question, title=u"other title")
        self.assertEqual(self.root.children().first().title, u"other title")


    def testContainerWithChildren(self):
        container=createContainer("13")
        container["5"]=createRisk("5")
        container["11"]=createRisk("11")
        AddToTree(self.root, container)
        children=list(self.root.children())
        self.assertEqual(len(children), 1)
        child=children[0]
        grandchildren=list(child.children())
        self.assertEqual(len(grandchildren), 2)

    def testContainerWithTitleAndProfile(self):
        # This is a test for #96
        container=createContainer("1")
        container["2"]=createContainer("2")
        AddToTree(self.root, container, [], title=u"Top level title", profile_index=1)
        children=list(self.root.children())
        self.assertEqual(len(children), 1)
        child=children[0]
        self.assertEqual(child.title, u"Top level title")
        self.assertEqual(child.profile_index, 1)




class MockSession(list):
    def reset(self):
        pass

    def removeChildren(self):
        pass

class BuildSurveyTreeTests(unittest.TestCase):
    def setUp(self):
        from euphorie.client import survey

        def AddToTree(dbsession, child, title=None, profile_index=0):
            dbsession.append((child.id, title))

        self._AddToTree=survey.AddToTree
        survey.AddToTree=AddToTree


    def tearDown(self):
        from euphorie.client import survey
        survey.AddToTree=self._AddToTree


    def testEmptyProfileNoQuestions(self):
        BuildSurveyTree(dict(), dbsession=MockSession())

    def testEmptyProfileWithQuestion(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createRisk("13")), dbsession=dbsession)
        self.assertEqual(dbsession, [("13", None)])

    def testEmptyProfileWithContainer(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createContainer("13")), dbsession=dbsession)
        self.assertEqual(dbsession, [("13", None)])

    def testEmptyProfileWithProfileQuestion(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createContainer("13", True)), dbsession=dbsession)
        self.assertEqual(dbsession, [])

    def testOptionalProfilePositive(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createContainer("13", True)),
                        profile={"13": True}, dbsession=dbsession)
        self.assertEqual(dbsession, [("13", None)])

    def testOptionalProfileNegative(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createContainer("13", True)),
                        profile={"13": False}, dbsession=dbsession)
        self.assertEqual(dbsession, [])

    def testRepeatProfileNoAnswers(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createContainer("13", True)),
                        profile={"13": []}, dbsession=dbsession)
        self.assertEqual(dbsession, [])

    def testRepeatProfileMultipleAnswers(self):
        dbsession=MockSession()
        BuildSurveyTree(dict(one=createContainer("13", True)),
                        profile={"13": ["one", "two"]}, dbsession=dbsession)
        self.assertEqual(dbsession, [("13", "one"), ("13", "two")])



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




def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

