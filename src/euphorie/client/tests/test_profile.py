from euphorie.client import model
from euphorie.client.browser.session import Profile
from euphorie.client.profile import AddToTree
from euphorie.client.profile import BuildSurveyTree
from euphorie.client.profile import extractProfile
from euphorie.client.tests.test_update import TreeTests
from euphorie.content.profilequestion import IProfileQuestion
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from unittest import mock
from z3c.saconfig import Session
from zope.interface import alsoProvides


def createContainer(id, profile=False):
    from euphorie.content.interfaces import IQuestionContainer
    from zope.interface import implementer

    @implementer(IQuestionContainer)
    class Container(dict):
        title = "container"
        description = None

        def __init__(self, id):
            self.id = id

    c = Container(id)
    if profile:
        alsoProvides(c, IProfileQuestion)
    return c


def createRisk(id):
    from euphorie.content.risk import IRisk
    from zope.interface import implementer

    @implementer(IRisk)
    class Risk:
        title = "risk"
        type = "risk"
        default_probability = 0
        default_frequency = 0
        default_effect = 0
        description = None
        evaluation_method = "calculated"
        risk_always_present = None

        def __init__(self, id):
            self.id = id

    return Risk(id)


def createModule(id):
    from euphorie.content.interfaces import IQuestionContainer
    from euphorie.content.module import IModule
    from zope.interface import implementer

    @implementer(IModule, IQuestionContainer)
    class Module(dict):
        title = "module"
        description = None
        optional = False
        solution_direction = False

        def __init__(self, id):
            dict.__init__(self)
            self.id = id

    return Module(id)


class AddToTreeTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.session = Session()
        account = model.Account(id=1, loginname="jane", password="secret")
        self.session.add(account)
        self.survey = model.SurveySession(
            title="Survey", zodb_path="survey", account=account
        )
        self.session.add(self.survey)
        self.session.flush()
        self.root = self.survey.addChild(
            model.Module(title="test session", module_id="1", zodb_path="1")
        )

    def testAddNonInterestingNode(self):
        AddToTree(self.root, None, title="title")
        self.assertEqual(list(self.root.children()), [])

    def testAddRisk(self):
        question = createRisk("13")
        AddToTree(self.root, question)
        children = list(self.root.children())
        self.assertEqual(len(children), 1)

        child = children[0]
        self.assertTrue(isinstance(child, model.Risk))
        self.assertEqual(child.title, "risk")
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
        self.assertTrue(isinstance(child, model.Module))
        self.assertEqual(child.title, "container")
        self.assertEqual(child.module_id, "13")

    def testOverrideTitle(self):
        question = createRisk("13")
        AddToTree(self.root, question, title="other title")
        self.assertEqual(self.root.children().first().title, "other title")

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
        AddToTree(self.root, container, [], title="Top level title", profile_index=1)
        children = list(self.root.children())
        self.assertEqual(len(children), 1)
        child = children[0]
        self.assertEqual(child.title, "Top level title")
        # Profile index is forced back to 0 since root has profile index 0
        self.assertEqual(child.profile_index, 0)

    def test_item_with_description(self):
        question = createRisk("13")
        question.description = "<p>Hello!</p>"
        AddToTree(self.root, question)
        children = list(self.root.children())
        child = children[0]
        self.assertEqual(child.has_description, True)

    def test_item_without_description(self):
        question = createRisk("13")
        question.description = "<p></p>"
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


class BuildSurveyTreeTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.session = Session()
        account = model.Account(id=1, loginname="jane", password="secret")
        self.session.add(account)
        self.survey = model.SurveySession(
            title="Survey", zodb_path="survey", account=account
        )
        self.session.add(self.survey)
        self.session.flush()

    def test_empty_profile_no_question(self):
        BuildSurveyTree({}, {}, dbsession=self.survey)
        self.assertTrue(not self.survey.hasTree())

    def test_empty_profile_with_risk(self):
        BuildSurveyTree({"one": createRisk("13")}, {}, dbsession=self.survey)
        self.assertTrue(self.survey.hasTree())
        children = self.survey.children().all()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].zodb_path, "13")
        self.assertEqual(children[0].children().count(), 0)

    def test_empty_profile_with_container(self):
        BuildSurveyTree({"one": createContainer("13")}, {}, dbsession=self.survey)
        self.assertTrue(self.survey.hasTree())
        children = self.survey.children().all()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].zodb_path, "13")
        self.assertEqual(children[0].children().count(), 0)

    def test_empty_profile_with_profile_question(self):
        BuildSurveyTree({"one": createContainer("13", True)}, {}, dbsession=self.survey)
        self.assertTrue(not self.survey.hasTree())

    def testOptionalProfilePositive(self):
        BuildSurveyTree(
            {"one": createContainer("13", True)},
            profile={"13": True},
            dbsession=self.survey,
        )
        self.assertTrue(self.survey.hasTree())

    def testOptionalProfileNegative(self):
        BuildSurveyTree(
            {"one": createContainer("13", True)},
            profile={"13": False},
            dbsession=self.survey,
        )
        self.assertTrue(not self.survey.hasTree())

    def test_profile_without_answers(self):
        BuildSurveyTree(
            {"one": createContainer("13", True)},
            profile={"13": []},
            dbsession=self.survey,
        )
        self.assertTrue(not self.survey.hasTree())

    def test_profile_with_multiple_answers(self):
        BuildSurveyTree(
            {"one": createContainer("13", True)},
            profile={"13": ["one", "two"]},
            dbsession=self.survey,
        )
        self.assertTrue(self.survey.hasTree())
        children = self.survey.children().all()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].zodb_path, "13")
        self.assertEqual(children[0].profile_index, -1)
        grandchildren = children[0].children().all()
        self.assertEqual(len(grandchildren), 2)
        self.assertEqual(grandchildren[0].title, "one")
        self.assertEqual(grandchildren[0].profile_index, 0)
        self.assertEqual(grandchildren[1].title, "two")
        self.assertEqual(grandchildren[1].profile_index, 1)


class ExtractProfileTests(TreeTests):
    def extractProfile(self, *a, **kw):
        return extractProfile(*a, **kw)

    def testNoProfileQuestions(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        session = self.createSurveySession()
        session.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        self.assertEqual(self.extractProfile(survey, session), {})

    def testOptionalProfileQuestionNotSelected(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.use_location_question = False
        session = self.createSurveySession()
        self.assertEqual(self.extractProfile(survey, session), {"1": False})

    def testOptionalProfileQuestionSelected(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.use_location_question = False
        session = self.createSurveySession()
        session.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        self.assertEqual(self.extractProfile(survey, session), {"1": True})

    def testRepeatableProfileQuestionNotSelected(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        session = self.createSurveySession()
        self.assertEqual(self.extractProfile(survey, session), {"1": []})

    def testRepeatableProfileQuestionSingleOption(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.title = "Repeatable profile question"
        session = self.createSurveySession()
        session.addChild(
            model.Module(title="First answer", module_id="1", zodb_path="1")
        )
        self.assertEqual(self.extractProfile(survey, session), {"1": ["First answer"]})


class Profile_getDesiredProfile_Tests(TreeTests):
    def getDesiredProfile(self, survey, form):
        class Request:
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

    def testOptionalProfile_NoAnswer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.use_location_question = False
        self.assertEqual(self.getDesiredProfile(survey, {}), {})

    def testOptionalProfile_FalseAnswer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.use_location_question = False
        self.assertEqual(
            self.getDesiredProfile(survey, {"pq1.present": False}), {"1": False}
        )

    def testOptionalProfile_NegativeAnswer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.use_location_question = False
        self.assertEqual(
            self.getDesiredProfile(survey, {"pq1.present": "no"}), {"1": False}
        )

    def testOptionalProfile_TrueAnswer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        pq = survey["1"]
        pq.use_location_question = False
        self.assertEqual(
            self.getDesiredProfile(survey, {"pq1.present": "yes"}), {"1": True}
        )

    def test_profile_no_anwer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(self.getDesiredProfile(survey, {}), {})

    def test_profile_whitespace_answer(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
            self.getDesiredProfile(survey, {"1": ["   "], "pq1.present": "yes"}),
            {"1": []},
        )

    def test_profile_with_two_answers_not_multiple_active(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
            self.getDesiredProfile(survey, {"1": ["one", "two"], "pq1.present": "yes"}),
            {"1": ["one"]},
        )

    def test_profile_with_two_answers_multiple_active(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
            self.getDesiredProfile(
                survey,
                {"1": ["one", "two"], "pq1.present": "yes", "pq1.multiple": "yes"},
            ),
            {"1": ["one", "two"]},
        )

    def test_profile_strip_whitespace(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        self.assertEqual(
            self.getDesiredProfile(survey, {"1": [" *** "], "pq1.present": "yes"}),
            {"1": ["***"]},
        )


class Profile_setupSession_Tests(TreeTests):
    def makeView(self, survey, session=None):
        if not session:
            session = self.createSurveySession()
        return api.content.get_view(
            "profile",
            survey.restrictedTraverse("++session++%s" % session.id),
            self.get_client_request(),
        )

    def test_NewSession_NoProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        mod = survey["1"]
        mod.title = "Module one"
        view = self.makeView(survey)

        session = view.session
        with api.env.adopt_user(user=session.account):
            view.setupSession()
            self.assertTrue(view.session is session)
            self.assertEqual(session.hasTree(), True)

    def test_NewSession_SimpleProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        session = view.session
        view.request.form["1"] = ["one"]
        view.request.form["pq1.present"] = "yes"
        with api.env.adopt_user(user=session.account):
            view.setupSession()
            self.assertEqual(view.session, session)
            self.assertEqual(session.hasTree(), True)

    def test_NewSession_EmptyProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        session = view.session
        with api.env.adopt_user(user=session.account):
            view.setupSession()
            self.assertTrue(view.session is session)
            self.assertEqual(session.hasTree(), False)

    def test_ExistingSession_NoProfile(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.module", "1")
        mod = survey["1"]
        mod.title = "Module one"
        view = self.makeView(survey)
        with mock.patch("euphorie.client.profile.extractProfile", return_value={}):
            session = view.session
            BuildSurveyTree(survey, {}, session)
            with api.env.adopt_user(user=session.account):
                view.setupSession()
                self.assertEqual(view.session, session)
                self.assertTrue(session.hasTree())

    def test_ExistingSession_NoProfileChange(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        survey.invokeFactory("euphorie.profilequestion", "2")
        survey.get("2").use_location_question = False

        view = self.makeView(survey)
        with mock.patch(
            "euphorie.client.profile.extractProfile",
            return_value={"1": ["London"], "2": True},
        ):
            session = view.session
            BuildSurveyTree(survey, {"1": ["London"], "2": True}, session)
            view.request.form["1"] = ["London"]
            view.request.form["pq1.present"] = "yes"
            view.request.form["pq2.present"] = "yes"
            with api.env.adopt_user(user=session.account):
                view.setupSession()
                self.assertEqual(view.session, session)
                self.assertEqual(view.session.hasTree(), True)

    def test_ExistingSession_ProfileChanged(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        view = self.makeView(survey)
        with mock.patch(
            "euphorie.client.profile.extractProfile",
            return_value={"1": ["London"]},
        ):
            session = view.session
            with api.env.adopt_user(user=session.account):
                BuildSurveyTree(survey, {"1": ["London"]}, session)
                view.request.form["1"] = ["London", "Paris"]
                # this will run an SQL statement incompatible with sqlite
                with mock.patch(
                    "euphorie.client.model.SurveySession.copySessionData",
                    return_value=None,
                ):
                    new_session = view.setupSession()
                view = self.makeView(survey, new_session)
                self.assertTrue(view.session is not session)
                self.assertEqual(view.session.hasTree(), False)

    def test_ExistingSession_ProfileChangedNoLocation(self):
        survey = self.createClientSurvey()
        survey.invokeFactory("euphorie.profilequestion", "1")
        survey.get("1").use_location_question = False
        view = self.makeView(survey)
        with mock.patch(
            "euphorie.client.profile.extractProfile",
            return_value={"1": True},
        ):
            session = view.session
            with api.env.adopt_user(user=session.account):
                BuildSurveyTree(survey, {"1": True}, session)
                view.request.form["pq1.present"] = "no"
                # this will run an SQL statement incompatible with sqlite
                with mock.patch(
                    "euphorie.client.model.SurveySession.copySessionData",
                    return_value=None,
                ):
                    new_session = view.setupSession()
                view = self.makeView(survey, new_session)
                self.assertTrue(view.session is not session)
                self.assertEqual(view.session.hasTree(), False)

    def test_create_survey_session(self):
        survey = self.createClientSurvey()
        view = self.makeView(survey)
        survey_view = api.content.get_view("index_html", survey, view.request)
        new_session = survey_view.create_survey_session(
            "a",
            view.session.account,
            report_comment="b",
        )
        self.assertEqual(new_session.title, "a")
        self.assertEqual(new_session.account, view.session.account)
        self.assertEqual(new_session.zodb_path, view.session.zodb_path)
        self.assertEqual(new_session.report_comment, "b")
