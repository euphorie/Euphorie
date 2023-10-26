from euphorie.client import model
from z3c.saconfig import Session


class BaseNotification:
    id = None
    default = False

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def notification_enabled(self, account):
        query = (
            Session.query(model.NotificationSubscription)
            .filter(model.NotificationSubscription.account_id == account.id)
            .filter(model.NotificationSubscription.category == self.id)
        )
        result = query.first()
        if result:
            return result.enabled
        return self.default
