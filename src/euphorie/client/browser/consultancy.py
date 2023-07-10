from AccessControl import Unauthorized
from datetime import timezone
from euphorie.client import MessageFactory as _
from euphorie.client.browser.base import BaseView
from euphorie.client.model import Account
from euphorie.client.model import Consultancy
from euphorie.client.model import OrganisationMembership
from euphorie.client.model import SessionEvent
from euphorie.client.utils import CreateEmailTo
from json import JSONDecodeError
from plone import api
from plone.memoize import instance
from plone.memoize.view import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import html
import json
import logging


logger = logging.getLogger(__name__)


class ConsultancyBaseView(BaseView):
    @property
    def organisation(self):
        return self.context.session.account.organisation

    @property
    def is_admin(self):
        if not self.organisation:
            return False
        organisation_view = api.content.get_view(
            name="organisation",
            context=self.webhelpers.country_obj,
            request=self.request,
        )
        return organisation_view.get_member_role_id(
            self.organisation, self.webhelpers.get_current_account()
        ) in ["admin", "owner"]

    @property
    def consultants(self):
        if not self.organisation:
            return []
        return (
            self.sqlsession.query(Account)
            .join(
                OrganisationMembership,
                OrganisationMembership.member_id == Account.id,
            )
            .filter(OrganisationMembership.owner_id == self.organisation.owner_id)
            .filter(OrganisationMembership.member_role == "consultant")
            .order_by(Account.loginname)
            .all()
        )


# TODO make this an adapter
class SessionValidated:
    def __init__(self, context):
        self.context = context

    @property
    @instance.memoize
    def note(self):
        try:
            return json.loads(self.context.note)
        except JSONDecodeError:
            logger.warning(
                "Could not load note for session_event %r (%r)",
                self.context.id,
                self.context.note,
            )
            return {}

    @property
    def raw_time(self):
        return self.context.time.replace(tzinfo=timezone.utc)

    @property
    def consultant_email(self):
        return self.note["consultant_email"]

    @property
    def consultant_name(self):
        return self.note["consultant_name"]


class ConsultancyView(ConsultancyBaseView):
    """ """

    variation_class = "variation-risk-assessment"

    @property
    @memoize
    def validated_info(self):
        events = (
            self.sqlsession.query(SessionEvent)
            .filter(SessionEvent.session_id == self.context.session.id)
            .filter(SessionEvent.action == "validated")
            .order_by(SessionEvent.time.desc())
        )
        event = events.first()
        return SessionValidated(event)

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        return super().__call__()


class PanelRequestValidation(ConsultancyBaseView):
    """ """

    default_target_view = "@@consultancy"
    email_template = ViewPageTemplateFile("templates/notify-request-validation.pt")

    @property
    @memoize
    def consultant(self):
        consultant_id = self.request.form.get("consultant")
        consultant = (
            self.sqlsession.query(Account).filter(Account.id == consultant_id).one()
        )
        return consultant

    def notify_consultant(self):
        consultant = self.consultant
        requester = self.webhelpers.get_current_account()
        session = self.context
        body = html.unescape(
            self.email_template(
                consultant=self.consultant.first_name or consultant.title,
                requester=requester.title,
                assessment_title=session.title,
                assessment_link=f"{session.absolute_url()}/@@start",
            )
        )
        subject = api.portal.translate(
            _(
                "subject_request_validation",
                default="Risk assessment validation request",
            )
        )
        email_from_name = api.portal.get_registry_record("plone.email_from_name")
        email_from_address = api.portal.get_registry_record("plone.email_from_address")
        mail = CreateEmailTo(
            email_from_name,
            email_from_address,
            consultant.email,
            subject,
            body,
        )

        api.portal.send_email(
            body=mail,
            recipient=self.consultant.email,
            sender=email_from_address,
            subject=subject,
        )
        logger.info("Sent validation request email to %s", self.consultant.email)

    def handle_POST(self):
        """Handle the POST request."""
        consultancy = Consultancy(
            account=self.consultant,
            session=self.context.session,
        )
        self.context.session.consultancy = consultancy
        event = SessionEvent(
            account_id=self.webhelpers.get_current_account().id,
            session_id=self.context.session.id,
            action="validation_requested",
        )
        self.sqlsession.add(event)

        self.notify_consultant()
        self.redirect()

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        if not self.is_admin:
            raise Unauthorized(
                "Only organisation administrators can request validation"
            )
        return super().__call__()


class PanelValidateRiskAssessment(ConsultancyBaseView):
    """ """

    default_target_view = "@@consultancy"
    email_template = ViewPageTemplateFile("templates/notify-assessment-validated.pt")

    @property
    def organisation_admins(self):
        organisation_view = api.content.get_view(
            name="organisation",
            context=self.webhelpers.country_obj,
            request=self.request,
        )
        for account, membership in organisation_view.get_memberships(self.organisation):
            if membership.member_role == "admin":
                yield account
        yield self.sqlsession.query(Account).filter(
            Account.id == self.organisation.owner_id
        ).one()

    def notify_admins(self):
        consultant = self.webhelpers.get_current_account()
        subject = api.portal.translate(
            _(
                "subject_assessment_validated",
                default="Risk assessment validated",
            )
        )
        email_from_name = api.portal.get_registry_record("plone.email_from_name")
        email_from_address = api.portal.get_registry_record("plone.email_from_address")
        for admin in self.organisation_admins:
            body = self.email_template(
                consultant=consultant.title,
                requester=admin.first_name or admin.title,
                assessment_link=f"{self.context.absolute_url()}/@@consultancy",
            )
            mail = CreateEmailTo(
                email_from_name,
                email_from_address,
                admin.email,
                subject,
                body,
            )

            api.portal.send_email(
                body=mail,
                recipient=admin.email,
                sender=email_from_address,
                subject=subject,
            )
        logger.info("Sent validation confirmation email to organisation admins")

    def handle_POST(self):
        """Handle the POST request."""
        if self.request.form.get("approved", False):
            consultant = self.webhelpers.get_current_account()
            if not self.context.session.is_locked:
                # Lock the assessment in addition to validating it to make sure that it
                # goes back to the locked state when invalidating it
                locked_event = SessionEvent(
                    account_id=api.user.get_current().id,
                    session_id=self.context.session.id,
                    action="lock_set",
                )
                self.sqlsession.add(locked_event)
            validated_event = SessionEvent(
                account_id=consultant.id,
                session_id=self.context.session.id,
                action="validated",
                note=json.dumps(
                    {
                        "consultant_id": consultant.id,
                        "consultant_email": consultant.email,
                        "consultant_name": consultant.title,
                    }
                ),
            )
            self.sqlsession.add(validated_event)
            self.context.session.consultancy.status = "validated"
            self.notify_admins()
        self.redirect()

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        consultancy = self.context.session.consultancy
        if not consultancy or (
            self.webhelpers.get_current_account() != consultancy.account
        ):
            raise Unauthorized(
                "Only the consultant assigned to a risk assessment can validate it"
            )
        return super().__call__()


class PanelInvalidateRiskAssessment(ConsultancyBaseView):
    """ """

    default_target_view = "@@consultancy"

    def handle_POST(self):
        """Handle the POST request."""
        invalidated_event = SessionEvent(
            account_id=api.user.get_current().id,
            session_id=self.context.session.id,
            action="invalidated",
        )
        self.sqlsession.add(invalidated_event)
        self.sqlsession.delete(self.context.session.consultancy)
        self.redirect()

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        if not self.is_admin:
            raise Unauthorized(
                "Only organisation administrators can invalidate an assessment"
            )
        return super().__call__()


class Consultants(BrowserView):
    """Show a country/language specific page about finding consultants"""

    variation_class = "variation-risk-assessment"  # to show left-hand navigation

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    @memoize
    def content(self):
        help_folder = self.webhelpers.content_country_obj.help
        for lang in self.webhelpers._getLanguages():
            docs = help_folder.get(lang, None)
            if docs is None:
                continue
            consultants = docs.get("consultants", None)
            if consultants is not None:
                return consultants.body
        # fall back to any available language
        for docs in help_folder.objectValues():
            consultants = docs.get("consultants", None)
            if consultants is not None:
                return consultants.body

        return ""
