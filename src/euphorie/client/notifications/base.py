from email.utils import formataddr
from euphorie.client import MessageFactory as _
from euphorie.client import model
from euphorie.client.mails.base import BaseEmail
from logging import getLogger
from plone import api
from plone.memoize.view import memoize
from z3c.saconfig import Session


logger = getLogger(__name__)


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
    def sender(self):
        from_address = api.portal.get_registry_record(
            "euphorie.notification__email_from_address", default=False
        ) or api.portal.get_registry_record("plone.email_from_address")
        from_name = api.portal.get_registry_record(
            "euphorie.notification__email_from_name", default=False
        ) or api.portal.get_registry_record("plone.email_from_name")
        return formataddr((from_name, from_address))

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

        title_missing = api.portal.translate(
            _("label_missing_title", default="Title is missing")
        )

        session_links = ""
        for session in self.sessions:
            session_url = ""
            try:
                session_url = session.absolute_url()
            except ValueError:
                logger.exception(
                    "Could not get session URL for session %r and "
                    "zodb_path %r (session id: %r). There might be a data "
                    "inconsistency. Not including this session in the "
                    "notification mailing.",
                    session.title or title_missing,
                    session.zodb_path,
                    session.id,
                )
                continue

            session_links += (
                f"* [{session.title or title_missing}]({session_url}/@@start)\n"
            )

        # Compile the preferences link
        some_session = self.sessions[0]
        country = api.portal.get().client[some_session.country]
        country_url = country.absolute_url()
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

    def send_email(self):
        if not self.webhelpers.get_user_email(self.account):
            logger.warning(
                "Account %r has no email address. Not sending notification email.",
                self.account.id,
            )
            return
        super().send_email()


class BaseNotification:
    id = None
    default = False

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def title_missing(self):
        return api.portal.translate(
            _("label_missing_title", default="Title is missing")
        )

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
