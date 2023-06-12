from euphorie.client import model
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from unittest import mock
from unittest import TestCase


class TestWebhelpers(EuphorieIntegrationTestCase):
    def test_get_sessions_query_anonymous(self):
        with self._get_view("webhelpers", self.portal.client) as view:
            # anonymous does not see anything
            self.assertIn("WHERE 0 = 1", str(view.get_sessions_query()))

    def _get_query_filters(self, query):
        """Return the filters of a SQLAlchemy query."""
        return str(query).partition("\nFROM session \n")[-1]

    def test_content_country_object(self):
        with api.env.adopt_user(SITE_OWNER_NAME):
            content_country = api.content.create(
                container=self.portal.sectors, type="euphorie.country", id="eu"
            )
            client_country = api.content.create(
                container=self.portal.client, type="euphorie.clientcountry", id="eu"
            )

        with self._get_view("webhelpers", self.portal.client.eu) as view:
            self.assertNotEqual(view.content_country_obj, client_country)
            self.assertEqual(view.content_country_obj, content_country)

    def test_get_sessions_query_authenticated(self):
        account = addAccount(password="secret")
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
        with api.env.adopt_user(user=account):
            # Check with no parameter
            with self._get_view("webhelpers", self.portal.client) as view:
                self.assertEqual(
                    self._get_query_filters(view.get_sessions_query()),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.account_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )

                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(include_archived=True)
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.account_id = ? "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.account_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) AND "
                        "lower(session.title) LIKE lower(?) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                foo_group = model.Group(group_id="foo")
                account.group = foo_group
                model.Session.flush()
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(filter_by_group=True)
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.account_id = ? AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(filter_by_account=False)
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=True
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=foo_group
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=[foo_group]
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                bar_group = model.Group(group_id="bar")
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False,
                            filter_by_group=[foo_group, bar_group],
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id IN (__[POSTCOMPILE_group_id_1]) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )

    def test_get_sessions_query_authenticated_with_organization(self):
        account1 = addAccount("foo", password="secret")
        account2 = addAccount("bar", password="secret")
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

        # Make account2 a member of account1 organization
        model.Session.add(
            model.OrganisationMembership(owner_id=account1.id, member_id=account2.id)
        )
        model.Session.flush()

        # For account1 the filter should be unchanged
        # (he sees only the sessions with its own id)
        session_filter = "session.account_id = ?"
        with api.env.adopt_user(user=account1):
            # Check with no parameter
            with self._get_view("webhelpers", self.portal.client) as view:
                self.assertEqual(
                    self._get_query_filters(view.get_sessions_query()),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} AND "
                        f"(session.archived >= ? OR session.archived IS NULL) "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )

                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(include_archived=True)
                    ),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} AND "
                        f"(session.archived >= ? OR session.archived IS NULL) AND "
                        f"lower(session.title) LIKE lower(?) "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                foo_group = model.Group(group_id="foo")
                account1.group = foo_group
                model.Session.flush()
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(filter_by_group=True)
                    ),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} AND "
                        f"session.group_id = ? AND "
                        f"(session.archived >= ? OR session.archived IS NULL) "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(filter_by_account=False)
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=True
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=foo_group
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=[foo_group]
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                bar_group = model.Group(group_id="bar")
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False,
                            filter_by_group=[foo_group, bar_group],
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id IN (__[POSTCOMPILE_group_id_1]) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )

        # For account2 the filter is changed to include also the sessions of the
        # other organization members
        session_filter = "session.account_id IN (__[POSTCOMPILE_account_id_1])"
        with api.env.adopt_user(user=account2):
            # Check with no parameter
            with self._get_view("webhelpers", self.portal.client) as view:
                self.assertEqual(
                    self._get_query_filters(view.get_sessions_query()),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} AND "
                        f"(session.archived >= ? OR session.archived IS NULL) "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                view.get_sessions_query(include_archived=True)
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(include_archived=True)
                    ),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} AND "
                        f"(session.archived >= ? OR session.archived IS NULL) AND "
                        f"lower(session.title) LIKE lower(?) "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                baz_group = model.Group(group_id="baz")
                account2.group = baz_group
                model.Session.flush()
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(filter_by_group=True)
                    ),
                    (
                        f"WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        f"{session_filter} AND "
                        f"session.group_id = ? AND "
                        f"(session.archived >= ? OR session.archived IS NULL) "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(filter_by_account=False)
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=True
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=foo_group
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=[foo_group]
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id = ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                fiz_group = model.Group(group_id="fiz")
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False,
                            filter_by_group=[baz_group, fiz_group],
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (__[POSTCOMPILE_zodb_path_1]) AND "
                        "session.group_id IN (__[POSTCOMPILE_group_id_1]) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )

    def test_can_view_session(self):
        # Setup a bunch of accounts and sessions
        account1 = addAccount("foo", password="secret")
        account2 = addAccount("bar", password="secret")
        account3 = addAccount("baz", password="secret")

        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)

        survey_session1 = model.SurveySession(
            id=1,
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=account1,
        )
        model.Session.add(survey_session1)

        survey_session2 = model.SurveySession(
            id=2,
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=account2,
        )
        model.Session.add(survey_session2)

        country = self.portal.client.nl
        traversed_session1 = country.ict["software-development"].restrictedTraverse(
            "++session++1"
        )
        traversed_session2 = country.ict["software-development"].restrictedTraverse(
            "++session++2"
        )

        # account1 can view its own session
        with api.env.adopt_user(user=account1):
            with self._get_view("webhelpers", traversed_session1) as view:
                self.assertTrue(view.can_view_session)

        # account2 cannot view
        with api.env.adopt_user(user=account2):
            with self._get_view("webhelpers", traversed_session1) as view:
                self.assertFalse(view.can_view_session)

        # We now make account 2 a member of account 1 organization
        model.Session.add(
            model.OrganisationMembership(owner_id=account1.id, member_id=account2.id)
        )

        # now account2 can view
        with api.env.adopt_user(user=account2):
            with self._get_view("webhelpers", traversed_session1) as view:
                self.assertTrue(view.can_view_session)

        # of course account1 cannot view account2's session
        with api.env.adopt_user(user=account1):
            with self._get_view("webhelpers", traversed_session2) as view:
                self.assertFalse(view.can_view_session)

        # account3 still cannot
        with api.env.adopt_user(user=account3):
            with self._get_view("webhelpers", traversed_session1) as view:
                self.assertFalse(view.can_view_session)

    def test_is_survey(self):
        """Test if webhelper's context is within a survey."""

        # Setup basic content.

        account = addAccount("foo", password="secret")

        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)

        survey_session = model.SurveySession(
            id=1,
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=account,
        )
        model.Session.add(survey_session)

        traversed_session = self.portal.client.nl.ict[
            "software-development"
        ].restrictedTraverse("++session++1")

        # Tests

        with self._get_view("webhelpers", self.portal) as view:
            self.assertFalse(view.is_survey)

        with self._get_view("webhelpers", self.portal.client) as view:
            self.assertFalse(view.is_survey)

        with self._get_view("webhelpers", self.portal.client.nl) as view:
            self.assertFalse(view.is_survey)

        with self._get_view("webhelpers", self.portal.client.nl.ict) as view:
            self.assertFalse(view.is_survey)

        with self._get_view(
            "webhelpers", self.portal.client.nl.ict["software-development"]
        ) as view:
            self.assertTrue(view.is_survey)

        with self._get_view("webhelpers", traversed_session) as view:
            self.assertTrue(view.is_survey)

    def test_survey_tree_data(self):
        """Test the survey navigation tree data."""

        # Setup basic content.

        account = addAccount("foo", password="secret")

        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)

        survey_session = model.SurveySession(
            id=1,
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=account,
        )
        model.Session.add(survey_session)

        traversed_session = self.portal.client.nl.ict[
            "software-development"
        ].restrictedTraverse("++session++1")

        # Tests

        with mock.patch(
            "euphorie.client.browser.webhelpers.WebHelpers.is_new_session",
            new_callable=mock.PropertyMock,
        ) as is_new_session:
            is_new_session.return_value = False
            with mock.patch(
                "euphorie.client.browser.webhelpers.WebHelpers.get_phase",
                return_value="preparation",
            ):
                is_new_session.return_value = False
                with api.env.adopt_user(user=account):
                    with self._get_view("webhelpers", traversed_session) as view:
                        nav_tree = view.survey_tree_data

                        self.assertEqual(nav_tree[0]["id"], "step-1")
                        self.assertEqual(nav_tree[1]["id"], "step-2")
                        self.assertEqual(nav_tree[2]["id"], "step-4")
                        self.assertEqual(nav_tree[3]["id"], "step-5")
                        self.assertEqual(nav_tree[4]["id"], "status")

                        self.assertTrue("@@start" in nav_tree[0]["href"])
                        self.assertTrue("@@identification" in nav_tree[1]["href"])
                        self.assertTrue("@@actionplan" in nav_tree[2]["href"])
                        self.assertTrue("@@report" in nav_tree[3]["href"])
                        self.assertTrue("@@status" in nav_tree[4]["href"])

                        self.assertEqual(nav_tree[0]["active"], True)
                        self.assertEqual(nav_tree[1]["active"], False)
                        self.assertEqual(nav_tree[2]["active"], False)
                        self.assertEqual(nav_tree[3]["active"], False)
                        self.assertEqual(nav_tree[4]["active"], False)

                        self.assertEqual(nav_tree[0]["disabled"], False)
                        self.assertEqual(nav_tree[1]["disabled"], False)
                        self.assertEqual(nav_tree[2]["disabled"], False)
                        self.assertEqual(nav_tree[3]["disabled"], False)
                        self.assertEqual(nav_tree[4]["disabled"], False)

    def test_survey_tree_data__archived__training(self):
        """Test the survey navigation tree data when survey is archived and the
        training module active.

        The report, training and status navigation items should not be
        disabled.
        """

        # Setup basic content.

        account = addAccount("foo", password="secret")

        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)

        survey_session = model.SurveySession(
            id=1,
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=account,
        )
        model.Session.add(survey_session)

        traversed_session = self.portal.client.nl.ict[
            "software-development"
        ].restrictedTraverse("++session++1")

        # Tests

        with mock.patch(
            "euphorie.client.model.SurveySession.is_archived",
            new_callable=mock.PropertyMock,
        ) as is_archived:
            is_archived.return_value = True
            with mock.patch(
                "euphorie.client.browser.webhelpers.WebHelpers.use_training_module",
                new_callable=mock.PropertyMock,
            ) as use_training_module:
                use_training_module.return_value = True
                with mock.patch(
                    "euphorie.client.browser.webhelpers.WebHelpers.is_new_session",
                    new_callable=mock.PropertyMock,
                ) as is_new_session:
                    is_new_session.return_value = False
                    with mock.patch(
                        "euphorie.client.browser.webhelpers.WebHelpers.get_phase",
                        return_value="preparation",
                    ):
                        is_new_session.return_value = False
                        with api.env.adopt_user(user=account):
                            with self._get_view(
                                "webhelpers", traversed_session
                            ) as view:
                                nav_tree = view.survey_tree_data

                                self.assertEqual(nav_tree[0]["id"], "step-1")
                                self.assertEqual(nav_tree[1]["id"], "step-2")
                                self.assertEqual(nav_tree[2]["id"], "step-4")
                                self.assertEqual(nav_tree[3]["id"], "step-5")
                                self.assertEqual(nav_tree[4]["id"], "step-6")
                                self.assertEqual(nav_tree[5]["id"], "status")

                                self.assertTrue("@@start" in nav_tree[0]["href"])
                                self.assertTrue(
                                    "@@identification" in nav_tree[1]["href"]
                                )
                                self.assertTrue("@@actionplan" in nav_tree[2]["href"])
                                self.assertTrue("@@report" in nav_tree[3]["href"])
                                self.assertTrue("@@training" in nav_tree[4]["href"])
                                self.assertTrue("@@status" in nav_tree[5]["href"])

                                self.assertEqual(nav_tree[0]["active"], True)
                                self.assertEqual(nav_tree[1]["active"], False)
                                self.assertEqual(nav_tree[2]["active"], False)
                                self.assertEqual(nav_tree[3]["active"], False)
                                self.assertEqual(nav_tree[4]["active"], False)
                                self.assertEqual(nav_tree[5]["active"], False)

                                self.assertEqual(nav_tree[0]["disabled"], False)
                                self.assertEqual(nav_tree[1]["disabled"], True)
                                self.assertEqual(nav_tree[2]["disabled"], True)
                                self.assertEqual(nav_tree[3]["disabled"], False)
                                self.assertEqual(nav_tree[4]["disabled"], False)
                                self.assertEqual(nav_tree[5]["disabled"], False)

    def test_survey_tree_data__consultancy(self):
        """Test the survey navigation tree data when consultancy is active."""

        # Setup basic content.

        account = addAccount("foo", password="secret")

        with api.env.adopt_user("admin"):
            addSurvey(self.portal, BASIC_SURVEY)

        survey_session = model.SurveySession(
            id=1,
            title="Dummy session",
            zodb_path="nl/ict/software-development",
            account=account,
        )
        model.Session.add(survey_session)

        traversed_session = self.portal.client.nl.ict[
            "software-development"
        ].restrictedTraverse("++session++1")

        # Tests
        with mock.patch(
            "euphorie.client.browser.webhelpers.WebHelpers.use_consultancy_phase",
            new_callable=mock.PropertyMock,
        ) as use_training_module:
            use_training_module.return_value = True
            with mock.patch(
                "euphorie.client.browser.webhelpers.WebHelpers.is_new_session",
                new_callable=mock.PropertyMock,
            ) as is_new_session:
                is_new_session.return_value = False
                with mock.patch(
                    "euphorie.client.browser.webhelpers.WebHelpers.get_phase",
                    return_value="preparation",
                ):
                    is_new_session.return_value = False
                    with api.env.adopt_user(user=account):
                        with self._get_view("webhelpers", traversed_session) as view:
                            nav_tree = view.survey_tree_data

                            self.assertEqual(nav_tree[0]["id"], "step-1")
                            self.assertEqual(nav_tree[1]["id"], "step-2")
                            self.assertEqual(nav_tree[2]["id"], "step-4")
                            self.assertEqual(nav_tree[3]["id"], "step-consultancy")
                            self.assertEqual(nav_tree[4]["id"], "step-5")
                            self.assertEqual(nav_tree[5]["id"], "status")

                            self.assertTrue("@@start" in nav_tree[0]["href"])
                            self.assertTrue("@@identification" in nav_tree[1]["href"])
                            self.assertTrue("@@actionplan" in nav_tree[2]["href"])
                            self.assertTrue("@@consultancy" in nav_tree[3]["href"])
                            self.assertTrue("@@report" in nav_tree[4]["href"])
                            self.assertTrue("@@status" in nav_tree[5]["href"])

                            self.assertEqual(nav_tree[0]["active"], True)
                            self.assertEqual(nav_tree[1]["active"], False)
                            self.assertEqual(nav_tree[2]["active"], False)
                            self.assertEqual(nav_tree[3]["active"], False)
                            self.assertEqual(nav_tree[4]["active"], False)
                            self.assertEqual(nav_tree[5]["active"], False)

                            self.assertEqual(nav_tree[0]["disabled"], False)
                            self.assertEqual(nav_tree[1]["disabled"], False)
                            self.assertEqual(nav_tree[2]["disabled"], False)
                            self.assertEqual(nav_tree[3]["disabled"], False)
                            self.assertEqual(nav_tree[4]["disabled"], False)
                            self.assertEqual(nav_tree[5]["disabled"], False)


class TestWebhelpersUnit(TestCase):
    def get_webhelpers(self, path):
        class DummyRequest:
            def __init__(self, path):
                self.PATH_INFO = path

        return WebHelpers(None, DummyRequest(path))

    def test_get_dashboard_tab(self):
        webhelpers = self.get_webhelpers(
            "/VirtualHostBase/https/oira.local:443/VirtualHostRoot/_vh_daimler"
            "/Plone/client/de/assessments"
        )
        self.assertEqual(webhelpers.get_dashboard_tab(), "assessments")

        webhelpers = self.get_webhelpers(
            "/VirtualHostBase/https/oira.local:443/VirtualHostRoot/_vh_daimler"
            "/Plone/client/de/assessments/"
        )
        self.assertEqual(webhelpers.get_dashboard_tab(), "assessments")

        webhelpers = self.get_webhelpers(
            "/VirtualHostBase/https/oira.local:443/VirtualHostRoot/_vh_daimler"
            "/Plone/client/de/@@assessments"
        )
        self.assertEqual(webhelpers.get_dashboard_tab(), "assessments")

        webhelpers = self.get_webhelpers(
            "/VirtualHostBase/https/oira.local:443/VirtualHostRoot/_vh_daimler"
            "/Plone/client/de/@@assessments/"
        )
        self.assertEqual(webhelpers.get_dashboard_tab(), "assessments")
