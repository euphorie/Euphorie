from euphorie.client import model
from euphorie.client.interfaces import CustomRisksModifiedEvent
from euphorie.client.navigation import FindNextQuestion
from euphorie.client.navigation import FindPreviousQuestion
from plone import api
from plone.memoize.instance import memoize
from Products.Five import BrowserView
from sqlalchemy import and_
from z3c.saconfig import Session
from zope.event import notify


class NavigationView(BrowserView):
    question_filter = None

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def session(self):
        return self.webhelpers.traversed_session.session

    @property
    @memoize
    def previous_question(self):
        return FindPreviousQuestion(
            self.context, dbsession=self.session, filter=self.question_filter
        )

    @property
    @memoize
    def next_question(self):
        return FindNextQuestion(
            self.context, dbsession=self.session, filter=self.question_filter
        )

    def proceed_to_next(self, reply):
        _next = reply.get("next", None)
        # In Safari browser we get a list
        if isinstance(_next, list):
            _next = _next.pop()
        if _next == "previous":
            target = self.previous_question
            if target is None:
                # We ran out of questions, step back to intro page
                url = "{session_url}/@@identification".format(
                    session_url=self.webhelpers.traversed_session.absolute_url()
                )
                return self.request.response.redirect(url)
        elif _next == "feedback":
            url = self.context.absolute_url() + "/@@identification_feedback"
            return self.request.response.redirect(url)
        elif _next in ("next", "skip"):
            target = self.next_question
            if target is None:
                # We ran out of questions, proceed to the action plan
                if self.webhelpers.use_action_plan_phase:
                    next_view_name = "@@actionplan"
                elif self.webhelpers.use_consultancy_phase:
                    next_view_name = "@@consultancy"
                else:
                    next_view_name = "@@report"
                base_url = self.webhelpers.traversed_session.absolute_url()
                url = f"{base_url}/{next_view_name}"
                return self.request.response.redirect(url)

        elif _next == "add_custom_risk" and self.webhelpers.can_edit_session:
            sql_module = (
                Session.query(model.Module)
                .filter(
                    and_(
                        model.SurveyTreeItem.session == self.session,
                        model.Module.zodb_path == "custom-risks",
                    )
                )
                .first()
            )
            if not sql_module:
                url = self.context.absolute_url() + "/@@identification"
                return self.request.response.redirect(url)

            view = api.content.get_view("identification", sql_module, self.request)
            view.add_custom_risk()
            notify(CustomRisksModifiedEvent(self.context.aq_parent))
            risk_id = self.context.aq_parent.children().count()
            # Construct the path to the newly added risk: We know that there
            # is only one custom module, so we can take its id directly. And
            # to that we can append the risk id.
            url = "{session_url}/{module}/{risk}/@@identification".format(
                session_url=self.webhelpers.traversed_session.absolute_url(),
                module=sql_module.getId(),
                risk=risk_id,
            )
            return self.request.response.redirect(url)
        elif _next == "actionplan":
            url = self.webhelpers.traversed_session.absolute_url() + "/@@actionplan"
            return self.request.response.redirect(url)
        # stay on current risk
        else:
            target = self.context
        url = ("{session_url}/{path}/@@identification").format(
            session_url=self.webhelpers.traversed_session.absolute_url(),
            path="/".join(target.short_path),
        )
        return self.request.response.redirect(url)
