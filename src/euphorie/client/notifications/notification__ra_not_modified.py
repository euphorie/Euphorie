from email.utils import formataddr
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from euphorie.client.mails.base import BaseEmail
from euphorie.client.model import Account
from euphorie.client.model import OrganisationMembership
from euphorie.client.model import SurveySession
from euphorie.client.notifications.base import BaseNotification
from logging import getLogger
from plone import api
from z3c.saconfig import Session
from zope.interface import implementer

import datetime


logger = getLogger(__name__)


class Email(BaseEmail):
    @property
    def account(self):
        return self.context["account"]

    @property
    def sessions(self):
        return self.context["sessions"]

    @property
    def translatable_subject(self):
        return _(
            "notification_mail_subject__ra_not_modified",
            default=("Erinnerung: Aktualisierung der Gefährdungsbeurteilung"),
        )

    @property
    def recipient(self):
        return formataddr(
            (
                self.account.title,
                self.account.email,
            )
        )

    @property
    def reminder_days(self):
        value = api.portal.get_registry_record(
            "euphorie.notification__ra_not_modified__reminder_days", default=365
        )
        return value

    def index(self):
        """The mail text."""
        session_links = "\n".join(
            f"* [{session.title}]({session.absolute_url()}/@@start)"
            for session in self.sessions
        )

        return _(
            "notification_mail_body__ra_not_modified",
            default=(
                """\
Sie haben vor ${reminder_days} Tagen Ihre Gefährdungsbeurteilung zuletzt \
bearbeitet (bzw. schreibgeschützt). \
Bitte denken Sie daran, Ihre Gefährdungsbeurteilung aktuell zu halten.
Mit diesem Link gelangen Sie zur Gefährdungsbeurteilung.

${session_links}
"""
            ),
            mapping={
                "reminder_days": self.reminder_days,
                "session_links": session_links,
            },
        )


@implementer(INotificationCategory)
class Notification(BaseNotification):
    id = "notification__ra_not_modified"
    title = _(
        "notification_title__ra_not_modified",
        default="Notify on orphaned risk assessments.",
    )
    default = False
    interval = INTERVAL_DAILY
    available = True

    @property
    def description(self):
        return _(
            "notification_description__ra_not_modified",
            default="Notify when a risk assessment was not modified for ${days} days.",
            mapping={"days": self.reminder_days},
        )

    @property
    def reminder_days(self):
        value = api.portal.get_registry_record(
            "euphorie.notification__ra_not_modified__reminder_days", default=365
        )
        return value

    def get_responsible_users(self, session):
        return (
            Session.query(Account)
            .filter(OrganisationMembership.owner_id == session.account_id)
            .filter(OrganisationMembership.member_role.in_(["admin", "manager"]))
            .filter(OrganisationMembership.member_id == Account.id)
        )

    def notify(self):
        if not self.available:
            return

        today = datetime.date.today()

        query = (
            Session.query(SurveySession)
            .filter(SurveySession.get_archived_filter())
            .filter(
                SurveySession.modified
                <= (today - datetime.timedelta(days=self.reminder_days))
            )
        )

        # TODO filter for already sent notifications

        sessions = query.all()

        notifications = {}
        for session in sessions:
            for account in self.get_responsible_users(session):
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
