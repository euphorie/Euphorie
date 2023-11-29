from euphorie.client.interfaces import INotificationCategory
from euphorie.client.interfaces import INTERVAL_DAILY
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from zope.component import getAdapters
from zope.interface import alsoProvides


class SendNotificationsDaily(BrowserView):
    def do_send(self):
        if not api.portal.get_registry_record(
            "euphorie.notifications__enabled", default=False
        ):
            return
        notifications = getAdapters((self.context, self.request), INotificationCategory)
        for notification in notifications:
            if not notification[1].available:
                continue
            if not notification[1].interval == INTERVAL_DAILY:
                continue
            notification[1].notify()

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.do_send()
