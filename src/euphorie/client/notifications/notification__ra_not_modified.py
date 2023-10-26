from email.utils import formataddr
from euphorie.client import MessageFactory as _
from euphorie.client import model as model_euphorie
from euphorie.client import utils
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from euphorie.client.mails.base import BaseEmail
from plone import api
from z3c.saconfig import Session
from zope.interface import implementer

import datetime


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

    def index(self):
        """The mail text."""
        full_name = self.webhelpers.get_user_fullname(self.account)
        session_links = "\n".join(
            f"* [{session.title}]({session.absolute_url()}/@@start)"
            for session in self.sessions
        )

        return f"""Hallo {full_name},

Sie haben vor 365 Tagen Ihre Gefährdungsbeurteilung zuletzt bearbeitet \
(bzw. schreibgeschützt). Bitte denken Sie daran, Ihre Gefährdungsbeurteilung \
aktuell zu halten. Die jährliche Unterweisung Ihrer Mitarbeitenden ist nach \
365 Tagen zu wiederholen.
Mit diesem Link gelangen Sie zur Gefährdungsbeurteilung.

{session_links}

Mit freundlichen Grüßen
Ihr OiRA Team
"""


@implementer(INotificationCategory)
class Notification:
    id = "euphorie_category_ra_not_modified"
    title = _(
        "notification_title__ra_not_modified",
        default="Notify on orphaned risk assessments.",
    )
    default = False
    interval = INTERVAL_DAILY

    def __init__(self, context, request):
        self.context = context
        self.request = request

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

    @property
    def available(self):
        # TODO: Check if user is allowed to set this setting.
        return True

    def notify(self):
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

        events = query.all()

        for event in events:
            country_notifications.setdefault(event.country, []).append(event)

        for country, events in country_notifications.items():
            managers = utils.get_country_managers(self.context, country)
            for manager in managers:
                # TODO: check, if notification settings are enabled for user
                email = manager.contact_email
                # get email template
                # send email

        __import__("pdb").set_trace()

        return events
