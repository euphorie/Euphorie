# coding=utf-8
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from zExceptions import Unauthorized

import mock


class TestArchivingViews(EuphorieIntegrationTestCase):
    def setUp(self):
        super(TestArchivingViews, self).setUp()
        addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        survey_session = model.SurveySession(
            title=u"Dummy session 1",
            zodb_path="nl/ict/software-development",
            account=self.account,
        )
        model.Session.add(survey_session)
        survey_session = model.SurveySession(
            title=u"Dummy session 2",
            zodb_path="nl/ict/software-development",
            account=self.account,
        )
        model.Session.add(survey_session)

    def test_archive_session_view(self):
        country = self.portal.client.nl
        traversed_session = country.ict["software-development"].restrictedTraverse(
            "++session++1"
        )
        session = traversed_session.session

        # Check that an unauthorized user cannot archive it
        john = model.Account(loginname="john@example.com")
        model.Session.add(john)
        with api.env.adopt_user(user=john):
            with self._get_view("archive-session", traversed_session) as view:
                with self.assertRaises(Unauthorized):
                    view()

        # By default, webhelpers.use_archive_feature is False, so the archive
        # feature is disabled. Nobody can archive.
        with api.env.adopt_user(user=self.account):
            with self._get_view("archive-session", traversed_session) as view:
                with self.assertRaises(Unauthorized):
                    view()

        # Now, activate the archive feature.
        # Check that an authorized user can archive it
        with mock.patch(
            "euphorie.client.browser.webhelpers.WebHelpers.use_archive_feature",
            return_value=True,
        ):
            with api.env.adopt_user(user=self.account):
                with self._get_view("archive-session", traversed_session) as view:
                    traversed_session
                    self.assertIsNone(session.archived)
                    view()
                    # Now the archival date is set
                    self.assertIsNotNone(session.archived)
                    # and we are redirected to the session view...
                    self.assertDictEqual(
                        view.request.response.headers,
                        {
                            "location": "http://nohost/plone/client/nl/ict/software-development/++session++1"  # noqa: E501
                        },
                    )
                    # ... or the referer (if specified)
                    view.request.set("HTTP_REFERER", "http://example.com")
                    view.redirect()
                    self.assertDictEqual(
                        view.request.response.headers,
                        {"location": "http://example.com"},
                    )

                with self._get_view("view", country) as view:
                    # The country view by default hides the archived sessions
                    self.assertTrue(view.hide_archived)
                    self.assertEqual(len(view.get_ordered_sessions()), 1)

                    view.request.__annotations__.clear()

                    # To show it we have to make sure the user unchecked a checkbox
                    # that by dfault is marked
                    view.request.set("hide_archived_marker", "1")
                    self.assertFalse(view.hide_archived)
                    self.assertEqual(len(view.get_ordered_sessions()), 2)

                    view.request.__annotations__.clear()

                    view.request.set("hide_archived", "1")
                    self.assertTrue(view.hide_archived)
                    self.assertEqual(len(view.get_ordered_sessions()), 1)

                with self._get_view("session-browser-sidebar", country) as view:
                    # There is also a sidebar that unluckily uses a different logic
                    # XXX the logic should be unified
                    self.assertEqual(len(view.leaf_sessions()), 1)
