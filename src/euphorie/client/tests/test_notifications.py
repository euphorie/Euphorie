from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.model import NotificationSubscription
from euphorie.client.tests.utils import addAccount
from euphorie.client.tests.utils import addSurvey
from euphorie.content.tests.utils import BASIC_SURVEY
from euphorie.testing import EuphorieIntegrationTestCase
from plone import api
from unittest import mock
from z3c.saconfig import Session
from zope.interface import alsoProvides


class NotificationsSettingsTests(EuphorieIntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.loginAsPortalOwner()
        addSurvey(self.portal, BASIC_SURVEY)
        self.account = addAccount(password="secret")
        alsoProvides(self.request, IClientSkinLayer)

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
                "euphorie.client.browser.settings.Preferences.show_notifications",
                return_value=True,
            ):
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
