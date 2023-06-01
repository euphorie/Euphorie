from datetime import datetime
from euphorie.client import model
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from lxml import html
from plone import api
from Products.Five.browser.metaconfigure import ViewNotCallableError
from time import sleep
from zExceptions.unauthorized import Unauthorized
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TestSurveyViews(EuphorieIntegrationTestCase):
    def _make_traversed_survey_session(self):
        with api.env.adopt_user("admin"):
            survey = addSurvey(self.portal, BASIC_SURVEY)
        account = addAccount(password="secret")
        survey_session = model.SurveySession(
            id=123,
            title="Dummy session",
            created=datetime(2012, 4, 22, 23, 5, 12),
            modified=datetime(2012, 4, 23, 11, 50, 30),
            zodb_path="nl/ict/software-development",
            account=account,
            company=model.Company(country="nl", employees="1-9", referer="other"),
        )
        model.Session.add(survey_session)
        survey = self.portal.client.nl.ict["software-development"]
        session_id = "++session++%d" % survey_session.id
        traversed_survey_session = survey.restrictedTraverse(session_id)
        return traversed_survey_session

    def test_survey_locking_views_when_feature_disabled(self):
        """The view is not callable but it has allowed attributes.
        They will anyway raise Unauthorized if the feature is not toggled on
        """
        traversed_survey_session = self._make_traversed_survey_session()
        survey_session = traversed_survey_session.session
        with api.env.adopt_user(user=survey_session.account):
            with self._get_view(
                "locking_view", traversed_survey_session, survey_session
            ) as view:
                # The view is not callable but
                # has traversable allowed attributes
                with self.assertRaises(ViewNotCallableError):
                    view()
                with self.assertRaises(Unauthorized):
                    view.set_lock()
                with self.assertRaises(Unauthorized):
                    view.refresh_lock()
                with self.assertRaises(Unauthorized):
                    view.unset_lock()

    def test_survey_locking_views_when_feature_enabled(self):
        """We have some views to display and set the locked state
        for a survey session."""
        traversed_survey_session = self._make_traversed_survey_session()
        survey_session = traversed_survey_session.session

        # We need to turn on the locking feature to access the view methods
        api.portal.set_registry_record("euphorie.use_locking_feature", True)

        with api.env.adopt_user(user=survey_session.account):
            with self._get_view(
                "locking_view", traversed_survey_session, survey_session
            ) as view:
                # The view is not callable but
                # has traversable allowed attributes
                self.assertRaises(ViewNotCallableError, view)
                # We have some column/properties that are going to change
                # when locking/unlocking the session
                self.assertEqual(survey_session.last_modifier, None)
                self.assertFalse(survey_session.is_locked)
                # Now we create a new locking event
                # If no referer is set,
                # the methods will redirect to the context url
                self.assertEqual(
                    view.set_lock(), traversed_survey_session.absolute_url()
                )
                self.assertEqual(
                    survey_session.last_locking_event.account, survey_session.account
                )
                self.assertTrue(survey_session.is_locked)
                old_lock_time = survey_session.last_locking_event.time

                view.request.__annotations__.clear()
                # Changing the HTTP_REFERER will redirect there
                # and calling refresh_lock will update the locking date
                view.request.set("HTTP_REFERER", "foo")
                # We need to wait at least one second because the datetime
                # is stored with that accuracy
                sleep(1)
                self.assertEqual(view.refresh_lock(), "foo")
                self.assertLess(old_lock_time, survey_session.last_locking_event.time)

                sleep(1)
                view.request.__annotations__.clear()
                # Calling unset_date will restore the unlocked state info
                self.assertEqual(view.unset_lock(), "foo")
                self.assertFalse(survey_session.is_locked)

            # We also have a menu view
            with self._get_view(
                "locking_menu", traversed_survey_session, survey_session
            ) as view:
                soup = html.fromstring(view())
                self.assertListEqual(
                    ["locking_view/set_lock#content"],
                    [
                        el.attrib["action"].rpartition("@@")[-1]
                        for el in soup.cssselect("form")
                    ],
                )

            # We trigger the session to be private
            with self._get_view(
                "locking_view", traversed_survey_session, survey_session
            ) as view:
                sleep(1)
                view.set_lock()

            # Now the locking menu will have options to uinlock and refresh lock
            with self._get_view(
                "locking_menu", traversed_survey_session, survey_session
            ) as view:
                soup = html.fromstring(view())
                self.assertListEqual(
                    [
                        "locking_view/unset_lock#content",
                        "locking_view/refresh_lock#content",
                    ],
                    [
                        el.attrib["action"].rpartition("@@")[-1]
                        for el in soup.cssselect("form")
                    ],
                )

    def test_modify_updates_last_modifier(self):
        account = addAccount(password="secret")
        survey_session = model.SurveySession(
            title="Dummy session", account=account, zodb_path=""
        )
        self.assertEqual(survey_session.modified, None)
        self.assertEqual(survey_session.last_modifier, None)
        with api.env.adopt_user(user=account):
            notify(ObjectModifiedEvent(survey_session))
        self.assertIsInstance(survey_session.modified, datetime)
        self.assertEqual(survey_session.last_modifier, account)
