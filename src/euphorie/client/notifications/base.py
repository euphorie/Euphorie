from email.utils import formataddr
from euphorie.client import MessageFactory as _
from euphorie.client import model
from euphorie.client.mails.base import BaseEmail
from plone import api
from plone.memoize.view import memoize
from z3c.saconfig import Session


class BaseNotificationEmail(BaseEmail):
    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", api.portal.get(), self.request)

    @property
    def account(self):
        return self.context["account"]

    @property
    def sessions(self):
        return self.context["sessions"]

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
            [
                f"* [{session.title}]({session.absolute_url()}/@@start)"
                for session in self.sessions
            ]
        )

        # Compile the preferences link
        some_session = self.sessions[0]
        contextual_webhelpers = api.content.get_view(
            "webhelpers", some_session.tool, self.request
        )
        country_url = contextual_webhelpers.country_url
        preferences_link = f"{country_url}/preferences"

        return api.portal.translate(
            _(
                "notification_mail_text__base",
                default="""\
Hello ${full_name},

${main_text}

${session_links}

Best regards
Your OiRA Team

**This is an automatically generated mail. If you do not want to receive mails \
from OiRA, you can change this [here](${preferences_link})**""",
                mapping={
                    "full_name": full_name,
                    "main_text": self.main_text,
                    "session_links": session_links,
                    "preferences_link": preferences_link,
                },
            )
        )


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
