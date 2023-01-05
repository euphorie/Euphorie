from Acquisition import aq_inner
from Acquisition import aq_parent
from euphorie.content import MessageFactory as _
from plone import api
from Products.Five import BrowserView
from zExceptions import Unauthorized
from zope.component import getMultiAdapter


class Lock(BrowserView):
    """Lock or unlock a User account.

    View name: @@lock
    """

    def __call__(self):
        if self.request.method != "POST":
            raise Unauthorized
        authenticator = getMultiAdapter(
            (self.context, self.request), name="authenticator"
        )
        if not authenticator.verify():
            raise Unauthorized

        self.context.locked = locked = self.request.form.get("action", "lock") == "lock"
        if locked:
            api.portal.show_message(
                _(
                    "message_user_locked",
                    default='Account "${title}" has been locked.',
                    mapping=dict(title=self.context.title),
                ),
                self.request,
                "success",
            )
        else:
            api.portal.show_message(
                _(
                    "message_user_unlocked",
                    default='Account "${title}" has been unlocked.',
                    mapping=dict(title=self.context.title),
                ),
                self.request,
                "success",
            )

        country = aq_parent(aq_inner(self.context))
        self.request.response.redirect("%s/@@manage-users" % country.absolute_url())
