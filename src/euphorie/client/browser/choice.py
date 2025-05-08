from euphorie.client import utils
from euphorie.client.navigation import getTreeData
from plone import api
from plone.memoize.instance import memoize
from Products.Five import BrowserView


class IdentificationView(BrowserView):
    """A view for displaying a choice in the identification phase."""

    variation_class = "variation-risk-assessment"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context.aq_parent, self.request)

    def check_render_condition(self):
        # Render the page only if the user can inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                "{session_url}/@@start".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return

    @property
    @memoize
    def navigation(self):
        return api.content.get_view("navigation", self.context, self.request)

    def _get_next(self, reply):
        _next = reply.get("next", None)
        # In Safari browser we get a list
        if isinstance(_next, list):
            _next = _next.pop()
        return _next

    @property
    def tree(self):
        return getTreeData(self.request, self.context)

    @property
    @memoize
    def session(self):
        return self.webhelpers.traversed_session.session

    @property
    @memoize
    def survey(self):
        """This is the survey dexterity object."""
        return self.webhelpers._survey

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

    def set_answer_data(self, reply):
        """Save the selected options as indicated by the paths in the `answer`
        field of `reply` (i.e. the request form).
        If the choice allows multiple options, then selecting none of them counts as
        a valid answer. In this case the `postponed` attribute is set to True.

        Note that this use of the `postponed` attribute does not exactly match
        the use for risks in that we don't expect the user to come back and
        answer later, but it is similar in that we record that the user has
        been here and clicked “Save” rather than “Skip”.
        """
        answer = reply.get("answer", [])
        if self.choice.allow_multiple_options:
            self.context.postponed = answer == "postponed"
        if answer == "postponed":
            answer = []
        if not isinstance(answer, (list, tuple)):
            answer = [answer]
        # XXX Check if paths are valid?
        # for path in answer[:]:
        #     try:
        #         self.webhelpers.traversed_session.restrictedTraverse(path)
        #     except KeyError:
        #        answer.remove(path)
        return self.context.set_options_by_zodb_path(answer)

    def __call__(self):
        # Render the page only if the user has inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                self.context.aq_parent.absolute_url() + "/@@start"
            )
        self.check_render_condition()

        utils.setLanguage(self.request, self.survey, self.survey.language)

        if self.request.method == "POST":
            reply = self.request.form
            if not self.webhelpers.can_edit_session:
                return self.navigation.proceed_to_next(reply)
            _next = self._get_next(reply)
            # Don't persist anything if the user skipped the question
            if _next == "skip":
                return self.navigation.proceed_to_next(reply)

            changed = self.set_answer_data(reply)

            if changed:
                self.session.touch()

            return self.navigation.proceed_to_next(reply)
        return self.index()
