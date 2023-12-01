from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from euphorie.client.model import Account
from euphorie.client.model import SurveySession
from euphorie.client.notifications.base import BaseNotification
from euphorie.client.notifications.base import BaseNotificationEmail
from logging import getLogger
from plone import api
from z3c.saconfig import Session
from zope.interface import implementer

import datetime


logger = getLogger(__name__)


class Email(BaseNotificationEmail):
    @property
    def main_text(self):
        return _(
            "notification_mail_body__ra_not_modified",
            default="""\
You have not modified your risk assessment for ${reminder_days} days. Please \
remember to keep your risk assessment up to date.
With this link you can access the risk assessment.""",
            msgid_plural="notification_mail_body__ra_not_modified__plural",
            default_plural="""\
You have not modified your risk assessments for ${reminder_days} days. Please \
remember to keep your risk assessments up to date.
With these links you can access the risk assessments.""",
            mapping={
                "reminder_days": self.reminder_days,
            },
            number=len(self.sessions),
        )

    @property
    def translatable_subject(self):
        return _(
            "notification_mail_subject__ra_not_modified",
            default="Reminder: Update of risk assessment (${num} open)",
            mapping={
                "num": len(self.sessions),
            },
        )

    @property
    def reminder_days(self):
        value = api.portal.get_registry_record(
            "euphorie.notification__ra_not_modified__reminder_days", default=365
        )
        return value


@implementer(INotificationCategory)
class Notification(BaseNotification):
    id = "notification__ra_not_modified"
    title = _(
        "notification_title__ra_not_modified",
        default="Notify on orphaned risk assessments.",
    )
    interval = INTERVAL_DAILY
    available = False  # This feature is not yet available

    @property
    def description(self):
        return _(
            "notification_description__ra_not_modified",
            default="Notify when a risk assessment was not modified for ${days} days.",
            mapping={"days": self.reminder_days},
        )

    @property
    def default(self):
        value = api.portal.get_registry_record(
            "euphorie.notification__ra_not_modified__default", default=False
        )
        return value

    @property
    def reminder_days(self):
        value = api.portal.get_registry_record(
            "euphorie.notification__ra_not_modified__reminder_days", default=365
        )
        return value

    def notify(self):
        if not self.available:
            return

        today = datetime.date.today()

        query = (
            Session.query(
                SurveySession,
                Account,
            )
            .join(
                Account,
                SurveySession.account_id == Account.id,
            )
            .filter(SurveySession.get_archived_filter())
            .filter(
                SurveySession.modified
                <= (today - datetime.timedelta(days=self.reminder_days))
            )
        )

        # TODO filter for already sent notifications

        sessions = query.all()

        notifications = {}
        for session, account in sessions:
            if not self.notification_enabled(account):
                continue

            notifications.setdefault(
                account.id,
                {
                    "account": account,
                    "sessions": [],
                },
            )["sessions"].append(session)

        for notification in notifications.values():
            mail = api.content.get_view(
                name="notification__ra-not-modified__email",
                context={
                    "account": notification["account"],
                    "sessions": notification["sessions"],
                },
                request=self.request,
            )
            mail.send_email()
            logger.info(
                "Sent %s to %s for sessions %s",
                self.id,
                notification["account"].email,
                ", ".join([session.title for session in notification["sessions"]]),
            )
