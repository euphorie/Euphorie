# FIXME fix inheritance
from euphorie.client.browser.risk import IdentificationView as RiskIdentificationView
from plone import api
from plone.memoize.instance import memoize
from Products.Five import BrowserView


class IdentificationView(RiskIdentificationView):
    """A view for displaying a choice in the identification phase."""

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context.aq_parent, self.request)

    @property
    @memoize
    def choice(self):
        return self.webhelpers.traversed_session.restrictedTraverse(
            self.context.zodb_path.split("/")
        )

    @property
    @memoize
    def selected(self):
        return [option.zodb_path for option in self.context.options]

    @property
    @memoize
    def risk(self):
        # XXX don't inherit this method
        return self.context.aq_parent.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/")
        )

    @property
    def is_custom_risk(self):
        # XXX don't inherit this method
        return False

    def set_answer_data(self, reply):
        answer = reply.get("answer", [])
        if not isinstance(answer, (list, tuple)):
            answer = [answer]
        # XXX Check if paths are valid?
        self.context.set_options_by_zodb_path(answer)

    def __call__(self):
        # Render the page only if the user has inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                self.context.aq_parent.absolute_url() + "/@@start"
            )
        if self.request.method == "POST":
            reply = self.request.form
            self.set_answer_data(reply)
            return self.proceed_to_next(reply)
        else:
            return self.index()
