from euphorie.client import MessageFactory as _
from euphorie.client.mails.base import BaseEmail
from euphorie.client import utils
from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from euphorie.client.model import SurveySession
from z3c.saconfig import Session
from zope.interface import implementer

import datetime


class NotificationEmail(BaseEmail):

    @property
    def subject(self):
        return _("Erinnerung: Aktualisierung der Gefährdungsbeurteilung und Wiederholungsunterweisung")

    @property
    def sender(self):
        return ""




@implementer(INotificationCategory)
class NotificationRANotModified:
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
        # TODO: get XXX da\ys
        self.notify()
        return _(
            "notification_description__ra_not_modified",
            default="Notify when a risk assessment was not modified for ${days} days.",
            mapping={"days": self.modification_threshold_days},
        )

    @property
    def modification_threshold_days(self):
        return 365

    @property
    def available(self):
        # TODO: Check if user is allowed to set this setting.
        return True

    def notify(self):
        today = datetime.date.today()

        country_notifications = {}

        query = (
            Session.query(SurveySession)
            .filter(SurveySession.get_archived_filter())
            .filter(
                SurveySession.modified
                <= (today - datetime.timedelta(days=self.modification_threshold_days))
            )
        )
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

                manager.notify(events)

        __import__("pdb").set_trace()

        return events
