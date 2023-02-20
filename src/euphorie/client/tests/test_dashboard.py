from datetime import timedelta
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from plone.app.event.base import localized_now


class TestDashboard(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        # We setup two surveys, an archived one and one which is not archived
        survey_session = model.SurveySession(
            title="Dummy session 1",
            zodb_path="nl/ict/software-development",
            account=self.account,
        )
        model.Session.add(survey_session)
        survey_session = model.SurveySession(
            title="Dummy session 2",
            zodb_path="nl/ict/software-development",
            account=self.account,
        )
        survey_session.archived = localized_now() - timedelta(days=1)
        model.Session.add(survey_session)

    def test_portlets_available_tools(self):
        country = self.portal.client.nl

        with api.env.adopt_user(user=self.account):
            with self._get_view("portlet-available-tools", country) as view:
                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["software-development"],
                )

                view.request.__annotations__.clear()
                with api.env.adopt_user("admin"):
                    another_one = api.content.create(
                        container=country.ict,
                        type="euphorie.survey",
                        title="Another one",
                    )

                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["another-one", "software-development"],
                )

                view.request.__annotations__.clear()

                # Check we can filter previews
                another_one.preview = True

                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["software-development"],
                )
                another_one.preview = False

                # Check we can filter obsolete
                view.request.__annotations__.clear()
                another_one.obsolete = True

                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["software-development"],
                )
                another_one.obsolete = False

                # Check we can filter by language
                view.request.__annotations__.clear()
                view.request.locale.id.language = "nl"
                another_one.language = "en"
                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["software-development"],
                )

                view.request.__annotations__.clear()
                another_one.language = "nl"
                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["another-one", "software-development"],
                )

                view.request.__annotations__.clear()
                another_one.language = "nl_NL"
                self.assertListEqual(
                    [survey.getId() for survey in view.surveys],
                    ["another-one", "software-development"],
                )

    def test_portlet_my_ras(self):
        country = self.portal.client.nl

        with api.env.adopt_user(user=self.account):
            with self._get_view("portlet-my-ras", country) as view:
                # The portlet by default hides the archived sessions
                self.assertTrue(view.hide_archived)

                self.assertEqual(
                    len(view.sessions_by_organisation[self.account.organisation]), 1
                )

                view.request.__annotations__.clear()

                # To show it we have to make sure the user unchecked a checkbox
                # that by default is marked (we need and empty marker to check this)
                view.request.set("hide_archived_marker", "1")
                self.assertFalse(view.hide_archived)
                self.assertEqual(
                    len(view.sessions_by_organisation[self.account.organisation]), 2
                )

                view.request.__annotations__.clear()

                # If the checbox is marked, the sessions are hidden again
                view.request.set("hide_archived", "1")
                self.assertTrue(view.hide_archived)
                self.assertEqual(
                    len(view.sessions_by_organisation[self.account.organisation]), 1
                )

            with self._get_view("session-browser-sidebar", country) as view:
                self.assertEqual(len(view.leaf_sessions()), 1)
