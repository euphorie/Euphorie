# coding=utf-8
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api


class TestWebhelpers(EuphorieIntegrationTestCase):
    def test_get_sessions_query_anonymous(self):
        with self._get_view("webhelpers", self.portal.client) as view:
            # anonymous does not see anything
            self.assertIn("WHERE 0 = 1", str(view.get_sessions_query()))

    def _get_query_filters(self, query):
        """ Return the filters of a SQLAlchemy query
        """
        return str(query).partition("\nFROM session \n")[-1]

    def test_get_sessions_query_authenticated(self):
        account = addAccount(password="secret")
        eu = api.content.create(
            type="euphorie.clientcountry", id="eu", container=self.portal.client
        )
        eusector = api.content.create(
            type="euphorie.clientsector", id="eusector", container=eu
        )
        api.content.create(type="euphorie.survey", id="eusurvey", container=eusector)
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
                foo_group = model.Group(group_id=u"foo")
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
                bar_group = model.Group(group_id=u"bar")
                self.assertEqual(
                    self._get_query_filters(
                        view.get_sessions_query(
                            filter_by_account=False, filter_by_group=[foo_group, bar_group]
                        )
                    ),
                    (
                        "WHERE session.zodb_path IN (?) AND "
                        "session.group_id IN (?, ?) AND "
                        "(session.archived >= ? OR session.archived IS NULL) "
                        "ORDER BY session.modified DESC, session.title"
                    ),
                )
