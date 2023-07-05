from euphorie.client.adapters.history_item import IHistoryItem
from euphorie.client.model import SessionEvent
from logging import getLogger
from plone.memoize.view import memoize
from Products.Five import BrowserView
from z3c.saconfig import Session
from zope.component import getAdapter
from zope.interface.interfaces import ComponentLookupError


logger = getLogger(__name__)


class HistoryPopup(BrowserView):
    """The view that keeps track of the history timeline of a session."""

    @property
    @memoize
    def events(self):
        """Get the events for this session."""
        return (
            Session.query(SessionEvent)
            .filter(SessionEvent.session == self.context.session)
            .order_by(SessionEvent.time)
        ).all()

    @property
    def items(self):
        """The sorted list of items related to this session."""
        session = self.context.session
        items = [getAdapter(session, IHistoryItem, name="started")]
        for event in self.events:
            try:
                items.append(getAdapter(event, IHistoryItem, name=event.action))
            except ComponentLookupError:
                logger.warning(
                    "Discarding unknown even type: %r, %r", event, event.action
                )
        if session.is_archived:
            items.append(getAdapter(session, IHistoryItem, name="archived"))
        return items
