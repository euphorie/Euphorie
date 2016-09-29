import unittest
from euphorie.client.profile import AddToTree
from euphorie.client.profile import BuildSurveyTree
from euphorie.client import model
from euphorie.client.tests.database import DatabaseTests
from euphorie.client.tests.test_update import TreeTests


def createContainer(id, profile=False):
    from zope.interface import implements
    from euphorie.content.interfaces import IQuestionContainer

    class Container(dict):
        implements(IQuestionContainer)
        title = u"container"
        description = None

        def __init__(self, id):
            self.id = id
    c = Container(id)
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
        title = u'risk'
        type = 'risk'
        default_probability = 0
        default_frequency = 0
        default_effect = 0
        description = None
        evaluation_method = 'calculated'
        risk_always_present = None

        def __init__(self, id):
            self.id = id
    return Risk(id)


def createModule(id):
    from zope.interface import implements
    from euphorie.content.module import IModule
    from euphorie.content.interfaces import IQuestionContainer

    class Module(dict):
        implements(IModule, IQuestionContainer)
        title = u'module'
        description = None
        optional = False
        solution_direction = False

        def __init__(self, id):
            dict.__init__(self)
            self.id = id
    return Module(id)


class AddToTreeTests(DatabaseTests):
    def setUp(self):
        from z3c.saconfig import Session
        super(AddToTreeTests, self).setUp()
        self.session = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey = model.SurveySession(title=u"Survey", zodb_path="survey",
                account=account)
        self.session.add(self.survey)
        self.session.flush()
        self.root = self.survey.addChild(model.Module(title=u"test session",
            module_id="1", zodb_path="1"))

    def testAddNonInterestingNode(self):
        AddToTree(self.root, None, title="title")
        self.assertEqual(list(self.root.children()), [])

    def testAddRisk(self):
        question = createRisk("13")
        AddToTree(self.root, question)
        children = list(self.root.children())
        self.assertEqual(len(children), 1)

        child = children[0]
        self.failUnless(isinstance(child, model.Risk))
        self.assertEqual(child.title, u"risk")
        self.assertEqual(child.risk_id, "13")
        self.assertEqual(child.risk_type, "risk")

    def testAddPolicy(self):
        question = createRisk("13")
        question.type = "policy"
        AddToTree(self.root, question)
        children = list(self.root.children())
        child = children[0]
        self.assertEqual(child.risk_type, "policy")
        self.assertEqual(child.priority, "high")

    def testAddTop5Risk(self):
        question = createRisk("13")
        question.type = "top5"
        AddToTree(self.root, question)
        children = list(self.root.children())
        child = children[0]
        self.assertEqual(child.risk_type, "top5")
        self.assertEqual(child.priority, "high")

    def testAddEmptyContainer(self):
        container = createContainer("13")
        AddToTree(self.root, container)
        children = list(self.root.children())
        self.assertEqual(len(children), 1)
        child = children[0]
        self.failUnless(isinstance(child, model.Module))
        self.assertEqual(child.title, u"container")
        self.assertEqual(child.module_id, "13")

    def testOverrideTitle(self):
        question = createRisk("13")
        AddToTree(self.root, question, title=u"other title")
        self.assertEqual(self.root.children().first().title, u"other title")

    def testContainerWithChildren(self):
        container = createContainer("13")
        container["5"] = createRisk("5")
        container["11"] = createRisk("11")
        AddToTree(self.root, container)
        children = list(self.root.children())
        self.assertEqual(len(children), 1)
        child = children[0]
        grandchildren = list(child.children())
        self.assertEqual(len(grandchildren), 2)

    def testContainerWithTitleAndProfile(self):
        # This is a test for #96
        container = createContainer("2")
        container["2"] = createContainer("3")
        AddToTree(self.root, container, [],
                title=u"Top level title", profile_index=1)
        children = list(self.root.children())
        self.assertEqual(len(children), 1)
        child = children[0]
        self.assertEqual(child.title, u"Top level title")
        # Profile index is forced back to 0 since root has profile index 0
        self.assertEqual(child.profile_index, 0)

    def test_item_with_description(self):
        question = createRisk("13")
        question.description = u'<p>Hello!</p>'
        AddToTree(self.root, question)
        children = list(self.root.children())
        child = children[0]
        self.assertEqual(child.has_description, True)

    def test_item_without_description(self):
        question = createRisk("13")
        question.description = u'<p></p>'
        AddToTree(self.root, question)
        children = list(self.root.children())
        child = children[0]
        self.assertEqual(child.has_description, False)

    def test_pretend_optional_module_has_description(self):
        # This is necessary to make sure optional modules are never skipped.
        module = createModule("13")
        module.optional = True
        AddToTree(self.root, module)
        children = list(self.root.children())
        child = children[0]
        self.assertEqual(child.has_description, True)


class BuildSurveyTreeTests(DatabaseTests):
    def setUp(self):
        from z3c.saconfig import Session
        super(BuildSurveyTreeTests, self).setUp()
        self.session = Session()
        account = model.Account(loginname=u"jane", password=u"secret")
        self.session.add(account)
        self.survey = model.SurveySession(title=u"Survey", zodb_path="survey",
                account=account)
        self.session.add(self.survey)
        self.session.flush()

    def test_empty_profile_no_question(self):
        BuildSurveyTree({}, dbsession=self.survey)
        self.assertTrue(not self.survey.hasTree())

    def test_empty_profile_with_risk(self):
        BuildSurveyTree({'one': createRisk("13")}, dbsession=self.survey)
        self.assertTrue(self.survey.hasTree())
        children = self.survey.children().all()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].zodb_path, '13')
        self.assertEqual(children[0].children().count(), 0)

    def test_empty_profile_with_container(self):
        BuildSurveyTree({'one': createContainer("13")}, dbsession=self.survey)
        self.assertTrue(self.survey.hasTree())
        children = self.survey.children().all()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].zodb_path, '13')
        self.assertEqual(children[0].children().count(), 0)

    def test_empty_profile_with_profile_question(self):
        BuildSurveyTree({'one': createContainer("13", True)},
                dbsession=self.survey)
        self.assertTrue(not self.survey.hasTree())

    def test_profile_without_answers(self):
        BuildSurveyTree({'one': createContainer("13", True)},
                        profile={"13": []}, dbsession=self.survey)
        self.assertTrue(not self.survey.hasTree())

    def test_profile_with_multiple_answers(self):
        BuildSurveyTree({'one': createContainer("13", True)},
                        profile={"13": ["one", "two"]}, dbsession=self.survey)
        self.assertTrue(self.survey.hasTree())
        children = self.survey.children().all()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].zodb_path, '13')
        self.assertEqual(children[0].profile_index, -1)
        grandchildren = children[0].children().all()
        self.assertEqual(len(grandchildren), 2)
        self.assertEqual(grandchildren[0].title, 'one')
        self.assertEqual(grandchildren[0].profile_index, 0)
        self.assertEqual(grandchildren[1].title, 'two')
        self.assertEqual(grandchildren[1].profile_index, 1)


class ExtractProfileTests(TreeTests):
    def extractProfile(self, *a, **kw):
        from euphorie.client.profile import extractProfile
        return extractProfile(*a, **kw)

    def testNoProfileQuestions(self):
        survey = self.createClientSurvey()
        survey.invokeFactory('euphorie.module', '1')
        session = self.createSurveySession()
        session.addChild(model.Module(
            title=u'Root', module_id='1', zodb_path='1'))
        self.assertEqual(self.extractProfile(survey, session), {})

    def testRepeatableProfileQuestionNotSelected(self):
        survey = self.createClientSurvey()
        survey.invokeFactory('euphorie.profilequestion', '1')
        session = self.createSurveySession()
        self.assertEqual(self.extractProfile(survey, session), {'1': []})

    def testRepeatableProfileQuestionSingleOption(self):
        survey = self.createClientSurvey()
        survey.invokeFactory('euphorie.profilequestion', '1')
        pq = survey['1']
        pq.title = u'Repeatable profile question'
        session = self.createSurveySession()
        session.addChild(model.Module(
            title=u'First answer', module_id='1', zodb_path='1'))
        self.assertEqual(
                self.extractProfile(survey, session),
                {'1': [u'First answer']})


class Profile_getDesiredProfile_Tests(TreeTests):
    def getDesiredProfile(self, survey, form):
        from euphorie.client.profile import Profile

        class Request(object):
            def __init__(self, form):
                self.form = form

            @property
            def request(self):
                return self

        view = Profile(survey, Request(form))
        return view.getDesiredProfile()

    def testNoProfile(self):
        survey = self.createClientSurvey()
        self.assertEqual(self.getDesiredProfile(survey, {}), {})

    def testNoProfile_FluffInForm(self):
        survey = self.createClientSurvey()
        self.assertEqual(self.getDesiredProfile(survey, {"dummy": True}), {})

    def test_profile_no_anwer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(self.getDesiredProfile(survey, {}), {})

    def test_profile_whitespace_answer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(self.getDesiredProfile(survey, {"1": [u"   "], "pq1.present": "yes"}),
                {"1": []})

    def test_profile_with_two_answers_not_multiple_active(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
                self.getDesiredProfile(survey,
                    {"1": [u"one", u"two"], "pq1.present": "yes"}),
                {"1": [u"one"]})

    def test_profile_with_two_answers_multiple_active(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
                self.getDesiredProfile(survey,
                    {"1": [u"one", u"two"], "pq1.present": "yes", "pq1.multiple": "yes"}),
                {"1": [u"one", "two"]})

    def test_profile_strip_whitespace(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
                self.getDesiredProfile(survey, {"1": [u" *** "], "pq1.present": "yes"}),
                {"1": [u"***"]})


class Profile_setupSession_Tests(TreeTests):
    def makeView(self, survey):
        from euphorie.client.profile import Profile
        view = Profile(survey, self.portal.REQUEST)
        view.session = view.request.other["euphorie.session"] = \
                self.createSurveySession()
        view.request.client = self.portal.client
        return view

    def setupSession(self, view):
        from euphorie.client.utils import setRequest
        from euphorie.client.model import SurveySession
        from AccessControl.SecurityManagement import getSecurityManager
        from AccessControl.SecurityManagement import setSecurityManager
        from AccessControl.SecurityManagement import newSecurityManager
        setRequest(self.portal.REQUEST)
        sm = getSecurityManager()
        # Add stub for copySessionData since it tries to run SQL code which
        # SQLite does not handle (UPDATE FROM)
        _copySessionData = SurveySession.copySessionData
        SurveySession.copySessionData = lambda *a: None
        try:
            newSecurityManager(None, self.session.account)
            return view.setupSession()
        finally:
            SurveySession.copySessionData = _copySessionData
            setSecurityManager(sm)
            setRequest(None)

    def test_NewSession_NoProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        mod = survey["1"]
        mod.title = u"Module one"
        view = self.makeView(survey)
        session = view.session
        self.setupSession(view)
        self.failUnless(view.session is session)
        self.assertEqual(session.hasTree(), True)

    def test_NewSession_SimpleProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        session = view.session
        view.request.form["1"] = [u"one"]
        view.request.form["pq1.present"] = "yes"
        self.setupSession(view)
        self.failUnless(view.session is session)
        self.assertEqual(session.hasTree(), True)

    def test_NewSession_EmptyProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        session = view.session
        self.setupSession(view)
        self.failUnless(view.session is session)
        self.assertEqual(session.hasTree(), False)

    def test_ExistingSession_NoProfile(self):
        from euphorie.client.profile import BuildSurveyTree
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        mod = survey["1"]
        mod.title = u"Module one"
        view = self.makeView(survey)
        view.current_profile = {}
        session = view.session
        BuildSurveyTree(survey, {}, session)
        self.setupSession(view)
        self.failUnless(view.session is session)
        self.assertEqual(session.hasTree(), True)

    def test_ExistingSession_NoProfileChange(self):
        from euphorie.client.profile import BuildSurveyTree
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        view.current_profile = {"1": [u'London']}
        session = view.session
        BuildSurveyTree(survey, {"1": [u'London']}, session)
        view.request.form["1"] = [u'London']
        view.request.form["pq1.present"] = "yes"
        self.setupSession(view)
        self.failUnless(view.session is session)
        self.assertEqual(view.session.hasTree(), True)

    def test_ExistingSession_ProfileChanged(self):
        from euphorie.client.profile import BuildSurveyTree
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        view.current_profile = {"1": ['London']}
        session = view.session
        BuildSurveyTree(survey, {"1": ['London', 'Paris']}, session)
        view.request.form["1"] = False
        self.setupSession(view)
        self.failUnless(view.session is not session)
        self.assertEqual(view.session.hasTree(), False)
