from Acquisition import aq_inner
from euphorie.client import model
from euphorie.client import utils
from euphorie.client.interfaces import CustomRisksModifiedEvent
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from euphorie.client.navigation import getTreeData
from euphorie.content.interfaces import ICustomRisksModule
from euphorie.content.profilequestion import IProfileQuestion
from logging import getLogger
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.event import notify


logger = getLogger(__name__)


class IdentificationView(BrowserView):
    """The introduction page for a module."""

    variation_class = "variation-risk-assessment"
    phase = "identification"
    question_filter = None
    template = ViewPageTemplateFile("templates/module_identification.pt")

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def survey(self):
        """This is the survey dexterity object."""
        return self.webhelpers._survey

    @property
    def tree(self):
        return getTreeData(self.request, self.context)

    @property
    @memoize
    def next_question(self):
        """Try to understand what the next question will be."""
        return FindNextQuestion(
            self.context,
            dbsession=self.context.aq_parent.session,
            filter=self.question_filter,
        )

    @property
    @memoize
    def previous_question(self):
        """Try to understand what the previous question will be."""
        return FindPreviousQuestion(
            self.context,
            dbsession=self.context.aq_parent.session,
            filter=self.question_filter,
        )

    @property
    @memoize
    def next_question_url(self):
        """Return the URL to the next question."""
        if not self.next_question:
            return ""
        return "{parent_url}/{next_question_path}/@@{view}".format(
            parent_url=self.webhelpers.traversed_session.absolute_url(),
            next_question_path="/".join(self.next_question.short_path),
            view=self.__name__,
        )

    @property
    @memoize
    def previous_question_url(self):
        """Return the URL to the previous question."""
        if not self.previous_question:
            return ""
        return "{parent_url}/{next_question_path}/@@{view}".format(
            parent_url=self.webhelpers.traversed_session.absolute_url(),
            next_question_path="/".join(self.previous_question.short_path),
            view=self.__name__,
        )

    @property
    @memoize
    def next_phase_url(self):
        """Return the URL to the next question."""
        if self.integrated_action_plan:
            return "{parent_url}/@@report".format(
                parent_url=self.context.aq_parent.absolute_url()
            )
        else:
            return "{parent_url}/@@actionplan".format(
                parent_url=self.context.aq_parent.absolute_url()
            )

    @property
    @memoize
    def integrated_action_plan(self):
        return self.webhelpers.integrated_action_plan

    def __call__(self):
        # Render the page only if the user has inspection rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_inspect_session:
            return self.request.response.redirect(
                self.context.aq_parent.absolute_url() + "/@@start"
            )

        if self.webhelpers.redirectOnSurveyUpdate():
            return

        context = aq_inner(self.context)
        utils.setLanguage(self.request, self.survey, self.survey.language)

        module = self.webhelpers.traversed_session.restrictedTraverse(
            context.zodb_path.split("/")
        )
        if self.request.environ["REQUEST_METHOD"] == "POST":
            return self.save_and_continue(module)

        if IProfileQuestion.providedBy(module) and context.depth == 2:
            if self.next_question is None:
                url = self.next_phase_url
            else:
                url = self.next_question_url
            return self.request.response.redirect(url)

        self.title = module.title
        self.module = module
        number_files = 0
        for i in range(1, 5):
            number_files += getattr(self.module, f"file{i}", None) and 1 or 0
        self.has_files = number_files > 0
        self.next_is_actionplan = not self.next_question
        if ICustomRisksModule.providedBy(module):
            template = ViewPageTemplateFile(
                "templates/module_identification_custom.pt"
            ).__get__(self, "")
        else:
            template = self.template
        return template()

    def save_and_continue(self, module):
        """We received a POST request.

        Submit the form and figure out where to go next.
        """
        context = aq_inner(self.context)
        reply = self.request.form
        _next = reply.get("next", None)
        # In Safari browser we get a list
        if isinstance(_next, list):
            _next = _next.pop()
        if module.optional and self.webhelpers.can_edit_session:
            if "skip_children" in reply:
                context.skip_children = reply.get("skip_children")
                context.postponed = False
            else:
                context.postponed = True
            self.context.session.touch()

        if _next == "previous":
            if self.previous_question is None:
                # We ran out of questions, step back to intro page
                url = "%s/@@identification" % self.context.aq_parent.absolute_url()
                self.request.response.redirect(url)
                return
            self.request.response.redirect(self.previous_question_url)
            return

        if ICustomRisksModule.providedBy(module):
            if _next == "add_custom_risk" and self.webhelpers.can_edit_session:
                self.add_custom_risk()
                notify(CustomRisksModifiedEvent(self.context))
                risk_id = self.context.children().count()
                url = "{parent_url}/{risk_id}/@@identification".format(
                    parent_url=self.context.absolute_url(),
                    risk_id=risk_id,
                )
                return self.request.response.redirect(url)
            # We ran out of questions, proceed to the action plan
            return self.request.response.redirect(self.next_phase_url)
        if self.next_question is None:
            # We ran out of questions, proceed to the action plan
            return self.request.response.redirect(self.next_phase_url)

        self.request.response.redirect(self.next_question_url)

    def add_custom_risk(self):
        sql_risks = self.context.children()
        if sql_risks.count():
            counter_id = (
                max([int(risk.zodb_path.split("/")[-1]) for risk in sql_risks.all()])
                + 1
            )
        else:
            counter_id = 1

        # Add a new risk
        risk = model.Risk(
            comment="",
            priority=None,
            risk_id=None,
            risk_type="risk",
            skip_evaluation=True,
            title="",
            identification=None,
            training_notes="",
            custom_description="",
        )
        risk.is_custom_risk = True
        risk.skip_children = False
        risk.postponed = False
        risk.has_description = None
        risk.zodb_path = "/".join(
            [self.context.zodb_path] + ["%d" % counter_id]
        )  # There's a constraint for unique zodb_path per session
        risk.profile_index = 0  # XXX: not sure what this is for
        self.context.addChild(risk)


class ActionPlanView(BrowserView):
    """The introduction page for an :obj:`euphorie.content.module` in an action
    plan."""

    variation_class = "variation-risk-assessment"
    phase = "actionplan"
    question_filter = model.ACTION_PLAN_FILTER

    @property
    @memoize
    def webhelpers(self):
        return self.context.restrictedTraverse("webhelpers")

    @property
    @memoize
    def survey(self):
        """This is the survey dexterity object."""
        return self.webhelpers._survey

    @property
    def use_solution_direction(self):
        return utils.HasText(getattr(self.module, "solution_direction", None))

    @property
    @memoize
    def module(self):
        return self.context.aq_parent.aq_parent.restrictedTraverse(
            self.context.zodb_path.split("/")
        )

    @property
    def tree(self):
        return getTreeData(
            self.request, self.context, filter=self.question_filter, phase=self.phase
        )

    def __call__(self):
        # Render the page only if the user has edit rights,
        # otherwise redirect to the start page of the session.
        if not self.webhelpers.can_edit_session:
            return self.request.response.redirect(
                self.context.aq_parent.aq_parent.absolute_url() + "/@@start"
            )
        if self.webhelpers.redirectOnSurveyUpdate():
            return

        context = aq_inner(self.context)
        utils.setLanguage(self.request, self.survey, self.survey.language)
        if (IProfileQuestion.providedBy(self.module) and context.depth == 2) or (
            ICustomRisksModule.providedBy(self.module) and self.phase == "actionplan"
        ):
            next_question = FindNextQuestion(
                context, self.context.session, filter=self.question_filter
            )
            if next_question is None:
                if self.phase == ("identification", "evaluation"):
                    url = (
                        self.webhelpers.traversed_session.absolute_url()
                        + "/@@actionplan"
                    )
                elif self.phase == "actionplan":
                    url = self.webhelpers.traversed_session.absolute_url() + "/@@report"
            else:
                url = "{session_url}/{path}/@@actionplan".format(
                    session_url=self.webhelpers.traversed_session.absolute_url(),
                    path="/".join(next_question.short_path),
                )
            return self.request.response.redirect(url)

        self.title = self.context.title
        previous = FindPreviousQuestion(
            self.context, self.context.session, filter=self.question_filter
        )
        if previous is None:
            self.previous_url = "{}/@@{}".format(
                self.context.aq_parent.absolute_url(),
                self.phase,
            )
        else:
            self.previous_url = "{session_url}/{path}/@@{phase}".format(
                session_url=self.webhelpers.traversed_session.absolute_url(),
                path="/".join(previous.short_path),
                phase=self.phase,
            )
        next_question = FindNextQuestion(
            self.context, self.context.session, filter=self.question_filter
        )
        if next_question is None:
            self.next_url = (
                self.webhelpers.traversed_session.absolute_url() + "/@@report"
            )
        else:
            self.next_url = "{session_url}/{path}/@@{phase}".format(
                session_url=self.webhelpers.traversed_session.absolute_url(),
                path="/".join(next_question.short_path),
                phase=self.phase,
            )
        return self.index()
