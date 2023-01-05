from euphorie.client import model
from euphorie.client.browser.webhelpers import WebHelpers
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
                        "session.account_id = ? "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
                        "session.group_id IN (?, ?) AND "
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
                        f"WHERE session.zodb_path IN (?) AND "
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
                        f"WHERE session.zodb_path IN (?) AND "
                        f"{session_filter} "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        f"WHERE session.zodb_path IN (?) AND "
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
                        f"WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
                        "session.group_id IN (?, ?) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )

        # For account2 the filter is changed to include also the sessions of the
        # other organization members
        session_filter = "session.account_id IN (?, ?)"
        with api.env.adopt_user(user=account2):
            # Check with no parameter
            with self._get_view("webhelpers", self.portal.client) as view:
                self.assertEqual(
                    self._get_query_filters(view.get_sessions_query()),
                    (
                        f"WHERE session.zodb_path IN (?) AND "
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
                        f"WHERE session.zodb_path IN (?) AND "
                        f"{session_filter} "
                        f"ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        f"WHERE session.zodb_path IN (?) AND "
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
                        f"WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
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
                        "WHERE session.zodb_path IN (?) AND "
                        "session.group_id IN (?, ?) AND "
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
