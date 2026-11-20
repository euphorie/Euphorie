from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from euphorie.client.model import Account
from euphorie.client.model import OrganisationMembership
from euphorie.client.model import SurveySession
from euphorie.client.notifications.base import BaseNotification
from euphorie.client.notifications.base import BaseNotificationEmail
from logging import getLogger
from plone import api
from plone.memoize.view import memoize
from sqlalchemy import sql
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
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

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

    def get_responsible_users(self, session):
        return (
            Session.query(Account)
            .outerjoin(
                OrganisationMembership, OrganisationMembership.member_id == Account.id
            )
            .filter(
                sql.or_(
                    sql.and_(
                        OrganisationMembership.owner_id == session.account_id,
                        OrganisationMembership.member_role.in_(["admin", "manager"]),
                    ),
                    Account.id == session.account_id,
                )
            )
        )

    @property
    def notifications_query(self):
        """Return the query for overdue assessments."""
        today = datetime.date.today()
        base_query = self.webhelpers.get_sessions_query(
            context=self.context,
            include_archived=False,
            filter_by_account=False,
        )
        return base_query.filter(
            SurveySession.modified
            <= (today - datetime.timedelta(days=self.reminder_days))
        )

    def iter_candidate_session_recipients(self):
        """Yield (assessment, candidate recipient) pairs before eligibility checks."""
        for session in self.notifications_query.all():
            for account in self.get_responsible_users(session):
                yield session, account

    def can_notify_for_session(self, session, account):
        """Allow subclasses to exclude a recipient for a specific assessment."""
        return True

    @property
    def notifications(self):
        """Group eligible assessments by the account ID of subscribed recipients."""
        # TODO filter for already sent notifications
        notifications = {}
        for session, account in self.iter_candidate_session_recipients():
            if not self.can_notify_for_session(session, account):
                continue
            if not self.notification_enabled(account):
                continue
            notifications.setdefault(
                account.id,
                {
                    "account": account,
                    "sessions": [],
                },
            )["sessions"].append(session)
        return notifications

    def notify(self):
        """Send one email per eligible recipient when this category is available."""
        if not self.available:
            return

        for notification in self.notifications.values():
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
                ", ".join(
                    [
                        session.title or f"{self.title_missing} (id {session.id})"
                        for session in notification["sessions"]
                    ]
                ),
            )
