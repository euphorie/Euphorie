from email.utils import formataddr
from euphorie.client import MessageFactory as _
from euphorie.client import model as model_euphorie
from euphorie.client import utils
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from euphorie.client.mails.base import BaseEmail
from euphorie.client.notifications.base import BaseNotification
from plone import api
from z3c.saconfig import Session
from zope.interface import implementer

import datetime


# from logging import getLogger
# logger = getLogger(__name__)


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
            default=(
                "Erinnerung: Aktualisierung der Gefährdungsbeurteilung "
                "und Wiederholungsunterweisung"
            ),
        )

    @property
    def recipient(self):
        return formataddr(
            (
                self.webhelpers.get_user_fullname(self.account),
                self.webhelpers.get_user_email(self.account),
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
        full_name = self.webhelpers.get_user_fullname(self.account)
        session_links = "\n".join(
            f"* [{session.title}]({session.absolute_url()}/@@start)"
            for session in self.sessions
        )

        return f"""Hallo {full_name},

Sie haben vor {self.reminder_days} Tagen Ihre Gefährdungsbeurteilung zuletzt \
bearbeitet (bzw. schreibgeschützt). \
Bitte denken Sie daran, Ihre Gefährdungsbeurteilung \
aktuell zu halten. Die jährliche Unterweisung Ihrer Mitarbeitenden ist nach \
{self.reminder_days} Tagen zu wiederholen.
Mit diesem Link gelangen Sie zur Gefährdungsbeurteilung.

{session_links}

Mit freundlichen Grüßen
Ihr OiRA Team
"""


@implementer(INotificationCategory)
class Notification(BaseNotification):
    id = "euphorie_category_ra_not_modified"
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

    def get_responsible_user(self, session):
        # XXX get organisation manager / head of department
        return (
            Session.query(model_euphorie.Account)
            .filter(model_euphorie.Account.id == session.account_id)
            .one()
        )

    def notify(self):
        if not self.available:
            return

        today = datetime.date.today()

        country_notifications = {}

        query = (
            Session.query(model_euphorie.SurveySession)
            .filter(model_euphorie.SurveySession.get_archived_filter())
            .filter(
                model_euphorie.SurveySession.modified
                <= (today - datetime.timedelta(days=self.reminder_days))
            )
        )

        # TODO filter for already sent notifications
        # TODO: get manager users to send mails to. the code below is incorrect.

        sessions = query.all()

        notifications = {}
        for session in sessions:
            account = self.get_responsible_user(session)
            if "@" not in account.email:
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

        return notifications

        for session in sessions:
            country_notifications.setdefault(session.country, []).append(session)

        for country, sessions in country_notifications.items():
            managers = utils.get_country_managers(self.context, country)
            for manager in managers:
                pass
                # TODO: check, if notification settings are enabled for user
                # email = manager.contact_email
                # get email template
                # send email

            # logger.info(
            #     "Sent %s to %s for sessions %s",
            #     self.id,
            #     notification["account"].email,
            #     ", ".join([session.title for session in notification["sessions"]]),
            # )

        return sessions
