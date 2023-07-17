from euphorie.client import MessageFactory as _
from euphorie.client.model import SessionEvent
from euphorie.client.model import show_timezone
from euphorie.client.model import SurveySession
from json import JSONDecodeError
from json import loads
from logging import getLogger
from plone import api
from plone.memoize.instance import memoize
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


logger = getLogger(__name__)


class IHistoryItem(Interface):
    """"""


@implementer(IHistoryItem)
class HistoryItem:
    """An item used to build the history timeline of a session."""

    _message = ""
    css_classes = "object"
    time_attribute = ""

    def __init__(self, context):
        self.context = context

    @property
    def email(self):
        return self.context.account.login

    @property
    def raw_time(self):
        return getattr(self.context, self.time_attribute)

    @property
    def time(self):
        return self.raw_time.isoformat()

    @property
    def message(self):
        return api.portal.translate(self._message)


@adapter(SurveySession)
class SessionStarted(HistoryItem):
    _message = _("started assessment")
    time_attribute = "created"


@adapter(SurveySession)
class SessionArchived(HistoryItem):
    _message = _("archived")
    time_attribute = "archived"


@adapter(SessionEvent)
class SessionEventHistoryItem(HistoryItem):
    """An item used to build the history timeline of a session built on top of
    an SQL object."""

    time_attribute = "time"

    @property
    @memoize
    def note(self):
        """Return the additional informations for this stored event."""
        try:
            return loads(self.context.note)
        except JSONDecodeError:
            logger.warning(
                "Could not load note for session_event %r (%r)",
                self.context.id,
                self.context.note,
            )
            return {}

    @property
    def raw_time(self):
        """The dates are returned naive, localize them with the proper timezone"""
        time = getattr(self.context, self.time_attribute)
        timezone = show_timezone()
        return timezone.localize(time)

    def session_url(self):
        session = self.context.session
        return "{tool_url}/++session++{session_id}".format(
            tool_url=session.tool.absolute_url(), session_id=session.id
        )

    def email2link(self, email):
        if not email:
            return None
        return '<a href="mailto:{email}">{email}</a>'.format(email=email)


class SessionValidationRequested(SessionEventHistoryItem):
    _message = _("validation requested")


class SessionValidated(SessionEventHistoryItem):
    _message = _("validated")


class SessionInalidated(SessionEventHistoryItem):
    _message = _("invalidated")


class SessionLockSet(SessionEventHistoryItem):
    _message = _("lock set")


class SessionLockUnset(SessionEventHistoryItem):
    _message = _("lock unset")


class SessionLockRefresh(SessionEventHistoryItem):
    _message = _("lock refreshed")
