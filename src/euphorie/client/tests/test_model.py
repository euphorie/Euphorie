from AccessControl.PermissionRole import _what_not_even_god_should_do
from datetime import timedelta
from euphorie.client import config
from euphorie.client import model
from euphorie.client.tests.database import DatabaseTests
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.event.base import localized_now
from sqlalchemy.exc import StatementError
from unittest import mock
from z3c.saconfig import Session


def createSurvey():
    session = Session()
    account = model.Account(loginname="jane", password="secret")
    session.add(account)
    survey = model.SurveySession(title="Session", zodb_path="survey", account=account)
    session.add(survey)
    session.flush()
    return (session, survey)


class SurveySessionTests(EuphorieIntegrationTestCase):
    def test_iface(self):
        """SurveySessions are marked by the ISurveySession interface."""
        survey = createSurvey()[-1]
        self.assertTrue(model.ISurveySession.providedBy(survey))

    def test_is_archived(self):
        """Verify that a session is archived when the archived attribute is set
        and it is in the past."""
        session = model.SurveySession()
        self.assertIsNone(session.archived)
        self.assertFalse(session.is_archived)
        session.archived = localized_now()
        self.assertTrue(session.is_archived)
        session.archived += timedelta(days=1)
        self.assertFalse(session.is_archived)

    def test_get_context_filter(self):
        with api.env.adopt_user("admin"):
            eu = api.content.create(
                type="euphorie.clientcountry", id="eu", container=self.portal.client
            )
            eusector = api.content.create(
                type="euphorie.clientsector", id="eusector", container=eu
            )
            api.content.create(
                type="euphorie.survey", id="eusurvey", container=eusector
            )
            nl = api.content.create(
                type="euphorie.clientcountry", id="nl", container=self.portal.client
            )
            nlsector = api.content.create(
                type="euphorie.clientsector", id="nlsector", container=nl
            )
            api.content.create(
                type="euphorie.survey", id="nlsurvey", container=nlsector
            )

            context_filter = model.SurveySession.get_context_filter(self.portal)
            self.assertSetEqual(
                set(context_filter.right.value),
                {"eu/eusector/eusurvey", "nl/nlsector/nlsurvey"},
            )

            context_filter = model.SurveySession.get_context_filter(self.portal.client)
            self.assertSetEqual(
                set(context_filter.right.value),
                {"eu/eusector/eusurvey", "nl/nlsector/nlsurvey"},
            )

            context_filter = model.SurveySession.get_context_filter(
                self.portal.client.eu
            )
            self.assertSetEqual(
                set(context_filter.right.value),
                {"eu/eusector/eusurvey"},
            )

            context_filter = model.SurveySession.get_context_filter(self.portal.sectors)
            self.assertFalse(context_filter)

    def testNoChildren(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        ses.add(root)
        ses.flush()
        self.assertEqual(root.children().count(), 0)

    def testAddChild(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        ses.add(root)
        root.addChild(model.Module(title="Module", module_id="1", zodb_path="1/1"))
        ses.flush()
        self.assertEqual(root.children().count(), 1)

    def testChildOrder(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        ses.add(root)
        ses.flush()
        root.addChild(model.Module(title="Profile 5", module_id="5", zodb_path="1/5"))
        root.addChild(model.Module(title="Profile 1", module_id="1", zodb_path="1/1"))
        root.addChild(model.Module(title="Profile 3", module_id="3", zodb_path="1/3"))
        ses.flush()
        self.assertEqual([c.module_id for c in list(root.children())], ["5", "1", "3"])

    def testReset_NoChildren(self):
        (ses, survey) = createSurvey()
        survey.reset()
        children = ses.query(model.SurveyTreeItem.id).filter(
            model.SurveyTreeItem.session == survey
        )
        self.assertEqual(children.count(), 0)

    def testReset_SingleChild(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        ses.add(root)
        children = ses.query(model.SurveyTreeItem.id).filter(
            model.SurveyTreeItem.session == survey
        )
        self.assertEqual(children.count(), 1)
        survey.reset()
        self.assertEqual(children.count(), 0)

    def testHasTree_NoChildren(self):
        (ses, survey) = createSurvey()
        self.assertEqual(survey.hasTree(), False)

    def testHasTree_SingleChild(self):
        (ses, survey) = createSurvey()
        root = survey.addChild(model.Module(title="Root", module_id="1", zodb_path="1"))
        ses.add(root)
        self.assertEqual(survey.hasTree(), True)

    def test_absolute_url(self):
        survey = createSurvey()[1]
        with self.assertRaises(ValueError):
            survey.absolute_url()

        # We now set the zodb_path to something
        # traversable in the context of the client folder
        survey.zodb_path = ""

        self.assertEqual(
            survey.absolute_url(), "http://nohost/plone/client/++session++1"
        )


class RiskPresentFilterTests(EuphorieIntegrationTestCase):
    def createData(self):
        (self.session, self.survey) = createSurvey()
        self.mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        self.survey.addChild(self.mod1)
        self.q1 = model.Risk(
            title="Risk 1",
            risk_id="1",
            zodb_path="1/1",
            type="risk",
            identification="no",
        )
        self.mod1.addChild(self.q1)

    def query(self):
        return self.session.query(model.SurveyTreeItem).filter(
            model.RISK_PRESENT_FILTER
        )

    def testValidRisk(self):
        self.createData()
        self.assertEqual(self.query().count(), 1)

    def testIncludeTop5(self):
        self.createData()
        self.q1.risk_type = "top5"
        self.assertEqual(self.query().count(), 1)

    def testNoPresentRisk(self):
        self.createData()
        self.q1.identification = "n/a"
        self.assertEqual(self.query().count(), 0)


class RiskPresentNoTop5FilterTests(EuphorieIntegrationTestCase):
    def createData(self):
        (self.session, self.survey) = createSurvey()
        self.mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        self.survey.addChild(self.mod1)
        self.q1 = model.Risk(
            title="Risk 1",
            risk_id="1",
            zodb_path="1/1",
            type="risk",
            identification="no",
        )
        self.mod1.addChild(self.q1)

    def query(self):
        return self.session.query(model.SurveyTreeItem).filter(
            model.RISK_PRESENT_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER
        )

    def testValidRisk(self):
        self.createData()
        self.assertEqual(self.query().count(), 1)

    def testSkipTop5(self):
        self.createData()
        self.q1.risk_type = "top5"
        self.assertEqual(self.query().count(), 0)

    def testSkipPolicy(self):
        self.createData()
        self.q1.risk_type = "policy"
        self.assertEqual(self.query().count(), 0)

    def testNoPresentRisk(self):
        self.createData()
        self.q1.identification = "n/a"
        self.assertEqual(self.query().count(), 0)


class ModuleWithRiskFilterTests(EuphorieIntegrationTestCase):
    def createData(self):
        (self.session, self.survey) = createSurvey()
        self.mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        self.survey.addChild(self.mod1)
        self.q1 = model.Risk(
            title="Risk 1",
            risk_id="1",
            zodb_path="1/1",
            type="risk",
            identification="no",
        )
        self.mod1.addChild(self.q1)

    def query(self):
        return self.session.query(model.SurveyTreeItem).filter(
            model.MODULE_WITH_RISK_FILTER
        )

    def testValidModule(self):
        self.createData()
        self.assertEqual(self.query().count(), 1)

    def testSkipChildren(self):
        self.createData()
        self.mod1.skip_children = True
        self.assertEqual(self.query().count(), 0)

    def testNoPresentRisk(self):
        self.createData()
        self.q1.identification = "n/a"
        self.assertEqual(self.query().count(), 0)

    def testNoChildren(self):
        (self.session, self.survey) = createSurvey()
        self.session.add(self.survey)
        self.mod1 = model.Module(
            title="Module 1", module_id="1", zodb_path="1", skip_children=False
        )
        self.survey.addChild(self.mod1)
        self.assertEqual(self.query().count(), 0)


class AccountTests(DatabaseTests):
    def testGlobalRoles(self):
        user = model.Account()
        self.assertEqual(user.getRoles(), ("EuphorieUser",))

    def testRolesInContext(self):
        user = model.Account()
        self.assertEqual(user.getRolesInContext(None), ("EuphorieUser",))

    def testNoViewPermission(self):
        user = model.Account()
        self.assertEqual(user.has_permission("View", None), False)

    def testHasSurveyViewPermission(self):
        user = model.Account()
        self.assertEqual(user.has_permission("Euphorie: View a Survey", None), True)

    def testAccountType(self):
        (self.session, self.survey) = createSurvey()
        account = self.survey.account
        self.assertEqual(account.account_type, config.FULL_ACCOUNT)
        account.account_type = config.GUEST_ACCOUNT
        self.assertEqual(account.account_type, config.GUEST_ACCOUNT)
        self.session.flush()  # check that exception is not raised
        account.account_type = config.CONVERTED_ACCOUNT
        self.session.flush()  # check that exception is not raised
        self.assertEqual(account.account_type, config.CONVERTED_ACCOUNT)
        account.account_type = "invalid"
        self.assertRaises(StatementError, self.session.flush)

    def testGroups(self):
        session = Session()
        group1 = model.Group(group_id="1")
        session.add(group1)
        session.flush()
        self.assertEqual(group1.group_id, "1")
        # Verify that a group might have one parent but many children
        group2 = model.Group(group_id="2")
        session.add(group2)
        group3 = model.Group(group_id="3")
        session.add(group3)
        group3.parent = group2.parent = group1
        session.flush()
        self.assertEqual(group2.group_id, "2")
        self.assertEqual(group2.parent, group1)
        self.assertEqual(group1.parent, None)
        self.assertListEqual(group1.children, [group2, group3])
        self.assertListEqual(group2.children, [])

    def testAccountGroupsRelationship(self):
        session = Session()
        group1 = model.Group(group_id="1")
        session.add(group1)
        session.flush()
        account1 = model.Account(loginname="account1")
        session.add(account1)
        account2 = model.Account(loginname="account2")
        session.add(account2)
        session.flush()
        self.assertEqual(account1.group, None)
        account1.group = group1
        account2.group = group1
        self.assertListEqual(group1.accounts, [account1, account2])

    def testAccountGroupsHierarchy(self):
        session = Session()
        group1 = model.Group(group_id="1")
        session.add(group1)
        group2 = model.Group(group_id="2")
        group2.parent = group1
        session.add(group2)
        group3 = model.Group(group_id="3")
        session.add(group3)
        group3.parent = group1
        group4 = model.Group(group_id="4")
        session.add(group4)
        group4.parent = group2
        session.flush()
        account1 = model.Account(loginname="account1")
        session.add(account1)
        account1.group = group1
        account2 = model.Account(loginname="account2")
        session.add(account2)
        account2.group = group2
        account3 = model.Account(loginname="account3")
        session.add(account3)
        account3.group = group3
        account4 = model.Account(loginname="account4")
        session.add(account4)
        session.flush()
        self.assertListEqual(group1.descendants, [group2, group3, group4])
        self.assertListEqual(group2.descendants, [group4])
        self.assertListEqual(group3.descendants, [])
        self.assertListEqual(account1.groups, [group1, group2, group3, group4])
        self.assertListEqual(account2.groups, [group2, group4])
        self.assertListEqual(account3.groups, [group3])
        self.assertListEqual(account4.groups, [])
        self.assertListEqual(group1.parents, [])
        self.assertListEqual(group2.parents, [group1])
        self.assertListEqual(group3.parents, [group1])
        self.assertListEqual(group4.parents, [group2, group1])

    def testSessions(self):
        session = Session()
        group1 = model.Group(group_id="1")
        session.add(group1)
        group2 = model.Group(group_id="2")
        session.add(group2)
        account1 = model.Account(loginname="account1")
        session.add(account1)
        account1.group = group1
        group2.parent = group1
        from functools import partial

        add_survey = partial(model.SurveySession, account=account1)
        survey1 = add_survey(zodb_path="1")
        session.add(survey1)
        survey2 = add_survey(zodb_path="2", group=group1)
        session.add(survey2)
        survey3 = add_survey(zodb_path="3", group=group2)
        session.add(survey3)
        session.flush()
        self.assertListEqual(account1.sessions, [survey1, survey2, survey3])
        self.assertListEqual(group1.sessions, [survey2])
        self.assertListEqual(group2.sessions, [survey3])

    def testSessionAcquisition(self):
        """Users belonging to a group should be able to see all the sessions
        belonging to the group and the group children."""
        session = Session()
        group1 = model.Group(group_id="1")
        session.add(group1)
        group2 = model.Group(group_id="2")
        session.add(group2)
        account1 = model.Account(loginname="account1")
        session.add(account1)
        account1.group = group1
        group2.parent = group1
        account2 = model.Account(loginname="account2")
        session.add(account2)
        account2.group = group2
        survey1 = model.SurveySession(
            account=account1,
            group=group1,
            zodb_path="1",
        )
        session.add(survey1)
        survey2 = model.SurveySession(
            account=account2,
            group=group2,
            zodb_path="2",
        )
        session.add(survey2)
        session.flush()
        self.assertListEqual(account1.sessions, [survey1])
        self.assertListEqual(account2.sessions, [survey2])
        self.assertListEqual(account1.acquired_sessions, [survey1, survey2])
        self.assertListEqual(account2.acquired_sessions, [survey2])


class AccountIntegrationTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.allowed = model.Account().allowed
        self.client = self.portal.client

    def test_not_licet_iovi_not_licet_bovi(self):
        self.assertFalse(self.allowed(self.client, _what_not_even_god_should_do))

    def test_has_anonymous_role(self):
        self.assertTrue(self.allowed(self.client, ["Anonymous"]))

    def test_has_authenticated_role(self):
        self.assertTrue(self.allowed(self.client, ["Authenticated"]))

    def test_has_euphorie_user_role(self):
        self.assertTrue(self.allowed(self.client, ["EuphorieUser"]))

    def test_has_reader_role(self):
        self.assertTrue(self.allowed(self.client, ["EuphorieUser"]))

    def test_no_other_role(self):
        self.assertFalse(self.allowed(self.client, ["Manager"]))

    def test_has_no_reader_role_on_portal(self):
        self.assertFalse(self.allowed(self.portal, ["Reader"]))


class SurveySessionDBTests(DatabaseTests):
    def test_get_account_filter(self):
        session = model.SurveySession()
        account = model.Account(id=1)
        # Note assertFalse will not do what you want on Binary expression
        self.assertEqual(str(session.get_account_filter()), "False")
        self.assertEqual(str(session.get_account_filter(False)), "False")
        self.assertEqual(str(session.get_account_filter(None)), "False")
        self.assertEqual(str(session.get_account_filter("")), "False")
        self.assertEqual(str(session.get_account_filter([])), "False")
        self.assertEqual(str(session.get_account_filter([""])), "False")
        self.assertEqual(
            str(session.get_account_filter("1")), "session.account_id = :account_id_1"
        )
        self.assertEqual(
            str(session.get_account_filter(1)), "session.account_id = :account_id_1"
        )
        session.get_account_filter(account)
        self.assertEqual(
            str(session.get_account_filter(account)),
            "session.account_id = :account_id_1",
        )
        self.assertEqual(
            str(session.get_account_filter(["1"])), "session.account_id = :account_id_1"
        )
        self.assertEqual(
            str(session.get_account_filter([1])), "session.account_id = :account_id_1"
        )
        self.assertEqual(
            str(session.get_account_filter([account])),
            "session.account_id = :account_id_1",
        )
        self.assertEqual(
            str(session.get_account_filter([account, "2"])),
            "session.account_id IN (__[POSTCOMPILE_account_id_1])",
        )
        with mock.patch("euphorie.client.model.get_current_account", return_value=None):
            self.assertEqual(str(session.get_account_filter(True)), "False")
        with mock.patch(
            "euphorie.client.model.get_current_account", return_value=account
        ):
            self.assertEqual(
                str(session.get_account_filter(True)),
                "session.account_id = :account_id_1",
            )
        with self.assertRaises(TypeError):
            session.get_account_filter(session)

    def test_get_group_filter(self):
        session = model.SurveySession()
        group = model.Group(group_id="foo")
        account = model.Account(id=1)
        # Note assertFalse will not do what you want on Binary expression
        self.assertEqual(str(session.get_group_filter()), "False")
        self.assertEqual(str(session.get_group_filter(False)), "False")
        self.assertEqual(str(session.get_group_filter(None)), "False")
        self.assertEqual(str(session.get_group_filter("")), "False")
        self.assertEqual(str(session.get_group_filter([])), "False")
        self.assertEqual(str(session.get_group_filter([""])), "False")
        self.assertEqual(
            str(session.get_group_filter("1")), "session.group_id = :group_id_1"
        )
        self.assertEqual(
            str(session.get_group_filter(1)), "session.group_id = :group_id_1"
        )
        self.assertEqual(
            str(session.get_group_filter(group)),
            "session.group_id = :group_id_1",
        )
        self.assertEqual(
            str(session.get_group_filter(["1"])), "session.group_id = :group_id_1"
        )
        self.assertEqual(
            str(session.get_group_filter([1])), "session.group_id = :group_id_1"
        )
        self.assertEqual(
            str(session.get_group_filter([group])),
            "session.group_id = :group_id_1",
        )
        self.assertEqual(
            str(session.get_group_filter([group, "2"])),
            "session.group_id IN (__[POSTCOMPILE_group_id_1])",
        )
        with mock.patch("euphorie.client.model.get_current_account", return_value=None):
            self.assertEqual(str(session.get_group_filter(True)), "False")

        # The account still does not have a group, so we should have False here
        with mock.patch(
            "euphorie.client.model.get_current_account", return_value=account
        ):
            self.assertEqual(str(session.get_group_filter(True)), "False")

        account.group_id = "foo"
        with mock.patch(
            "euphorie.client.model.get_current_account", return_value=account
        ):
            self.assertEqual(
                str(session.get_group_filter(True)),
                "session.group_id = :group_id_1",
            )

        with self.assertRaises(TypeError):
            session.get_group_filter(session)
