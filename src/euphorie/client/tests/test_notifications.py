from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import NotificationSubscription
from euphorie.client.model import SurveySession
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.client.tests.utils import MockMailFixture
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from unittest import mock
from z3c.saconfig import Session
from zope.interface import alsoProvides

import datetime


class NotificationsSettingsTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        alsoProvides(self.request, IClientSkinLayer)
        api.portal.set_registry_record("euphorie.notifications__enabled", True)

    def test_all_notifications(self):
        view = api.content.get_view(
            context=self.portal.client.nl, request=self.request, name="preferences"
        )
        with mock.patch(
            "euphorie.client.notifications.notification__ra_not_modified.Notification"
            ".available",
            return_value=True,
        ):
            notification_ids = [category.id for category in view.all_notifications]
        self.assertEqual(notification_ids, ["notification__ra_not_modified"])

    def test_subscribe_notification(self):
        request = self.request.clone()
        request.form["notifications"] = {
            "notification__ra_not_modified": True,
            "form.buttons.save": "",
        }
        view = api.content.get_view(
            context=self.portal.client.nl, request=request, name="preferences"
        )
        with api.env.adopt_user(user=self.account):
            view.update()
            with mock.patch(
                "euphorie.client.notifications.notification__ra_not_modified"
                ".Notification.available",
                return_value=True,
            ):
                view.handleSave(view, None)
        subscriptions = (
            Session.query(NotificationSubscription)
            .filter(NotificationSubscription.account_id == self.account.getId())
            .all()
        )
        self.assertEqual(subscriptions[0].category, "notification__ra_not_modified")

    def test_disallow_user_settings(self):
        api.portal.set_registry_record(
            "euphorie.notifications__allow_user_settings", False
        )
        request = self.request.clone()
        request.form["notifications"] = {
            "notification__ra_not_modified": True,
            "form.buttons.save": "",
        }
        view = api.content.get_view(
            context=self.portal.client.nl, request=request, name="preferences"
        )
        with api.env.adopt_user(user=self.account):
            view.update()

            # This attribute, based on the
            # `euphorie.notifications__allow_user_settings` registry entry,
            # should be set to False
            self.assertEqual(view.allow_notification_settings, False)

            # Try to save the notification
            with mock.patch(
                "euphorie.client.notifications.notification__ra_not_modified"
                ".Notification.available",
                return_value=True,
            ):
                view.handleSave(view, None)

        subscriptions = (
            Session.query(NotificationSubscription)
            .filter(NotificationSubscription.account_id == self.account.getId())
            .all()
        )

        # Notification should not be saved
        self.assertEqual(subscriptions, [])


class NotificationsSendingTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        alsoProvides(self.request, IClientSkinLayer)

        survey_session = SurveySession(
            id=1,
            title="Euphorie",
            zodb_path="nl/ict/software-development",
            account=self.account,
        )
        survey_session.modified = datetime.datetime.now() - datetime.timedelta(days=366)
        Session.add(survey_session)
        survey_session2 = SurveySession(
            id=2,
            title="Depublished",
            zodb_path="nl/ict/depublished",
            account=self.account,
        )
        survey_session2.modified = datetime.datetime.now() - datetime.timedelta(
            days=366
        )
        Session.add(survey_session2)
        api.portal.set_registry_record("euphorie.notifications__enabled", True)

    def test_send_notification(self):
        Session.add(
            NotificationSubscription(
                account_id=self.account.getId(),
                category="notification__ra_not_modified",
                enabled=True,
            )
        )
        view = api.content.get_view(
            context=self.portal.client.nl,
            request=self.request,
            name="send-notifications-daily",
        )
        mail_fixture = MockMailFixture()
        with mock.patch(
            "euphorie.client.notifications.notification__ra_not_modified"
            ".Notification.available",
            return_value=True,
        ):
            view()
        mail = mail_fixture.storage[0][0][0]
        self.assertIn(self.account.email, mail.get("To"))
        self.assertEqual(
            mail_fixture.storage[0][1]["subject"],
            "Reminder: Update of risk assessment (1 open)",
        )
