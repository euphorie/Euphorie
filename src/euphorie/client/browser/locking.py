from euphorie.client import model
from euphorie.client.config import LOCKING_ACTIONS
from plone import api
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from Products.Five import BrowserView
from zExceptions import Unauthorized


class LockingMenu(BrowserView):
    lock_actions = LOCKING_ACTIONS

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    def redirect(self):
        target = self.request.get("HTTP_REFERER") or self.context.absolute_url()
        return self.request.response.redirect(target)

    @property
    @memoize_contextless
    def portal(self):
        """The currently authenticated account."""
        return api.portal.get()

    @property
    def is_locked(self):
        """Return whether the session is locked."""
        return self.context.session.is_locked

    @property
    def is_validated(self):
        """Return whether the session is validated."""
        return self.context.session.is_validated

    def show_actions(self):
        """Return whether we should show the actions in the menu."""
        if self.is_locked:
            return self.webhelpers.can_unlock_session
        return self.webhelpers.can_lock_session

    @property
    def state(self):
        """Return the state of the session."""
        if self.is_validated:
            return "validated"
        if self.is_locked:
            return "locked"
        return "unlocked"

    def create_event(self, action):
        event = model.SessionEvent(
            account_id=self.webhelpers.current_account.id,
            session_id=self.context.session.id,
            action=action,
        )
        model.Session.add(event)

    def refresh_lock(self):
        """Reset the session date to now."""
        if not self.webhelpers.can_lock_session:
            raise Unauthorized()
        self.create_event("lock_refresh")
        return self.redirect()

    def set_lock(self):
        """Set the session date to now."""
        if not self.webhelpers.can_lock_session:
            raise Unauthorized()
        self.create_event("lock_set")
        return self.redirect()

    def unset_lock(self):
        """Unset the session date."""
        if not self.webhelpers.can_unlock_session:
            raise Unauthorized()
        self.create_event("lock_unset")
        return self.redirect()
