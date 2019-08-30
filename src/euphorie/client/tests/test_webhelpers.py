# coding=utf-8
from euphorie.client.tests.utils import addAccount
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api


class TestWebhelpers(EuphorieIntegrationTestCase):
    def test_get_sessions_query_anonymous(self):
        with self._get_view("webhelpers", self.portal.client) as view:
            # anonymous does not see anything
            self.assertTrue(str(view.get_sessions_query()).endswith("WHERE 0 = 1"))

    def _get_query_filters(sefl, query):
        """ Return the filters of a SQLAlchemy query
        """
        return str(query).partition("\nFROM session \n")[-1]

    def test_get_sessions_query_authenticated(self):
        account = addAccount(password="secret")
        with api.env.adopt_user(user=account):
            # Check with no parameter
            with self._get_view("webhelpers", self.portal.client) as view:
                self.assertEqual(
                    self._get_query_filters(view.get_sessions_query()),
                    (
                        "WHERE session.account_id = ? AND "
                        "session.zodb_path LIKE ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(include_archived=True)
                    ),
                    (
                        "WHERE session.account_id = ? AND "
                        "session.zodb_path LIKE ? "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(searchable_text="foo")
                    ),
                    (
                        "WHERE session.account_id = ? AND "
                        "session.zodb_path LIKE ? AND "
                        "(session.archived >= ? OR session.archived IS NULL) AND "
                        "lower(session.title) LIKE lower(?) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
