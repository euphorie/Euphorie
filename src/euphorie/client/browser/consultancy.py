from AccessControl import Unauthorized
from euphorie.client import MessageFactory as _
from euphorie.client.browser.base import BaseView
from euphorie.client.model import Account
from euphorie.client.model import OrganisationMembership
from euphorie.client.utils import CreateEmailTo
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import html
import logging


logger = logging.getLogger(__name__)


class Consultancy(BrowserView):
    """ """

    variation_class = "variation-risk-assessment"

    @property
    @memoize
    def webhelpers(self):
        return api.content.get_view("webhelpers", self.context, self.request)

    @property
    def organisation(self):
        return self.webhelpers.traversed_session.session.account.organisation

    def __call__(self):
        if not self.webhelpers.can_view_session:
            return self.request.response.redirect(self.webhelpers.client_url)
        return self.index()


class PanelRequestValidation(BaseView):
    """ """

    default_target_view = "@@consultancy"
    email_template = ViewPageTemplateFile("templates/notify-request-validation.pt")

    @property
    @memoize
    def organisation(self):
        return self.context.session.account.organisation

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

    @property
    def is_admin(self):
        organisation_view = api.content.get_view(
            name="organisation",
            context=self.webhelpers.country_obj,
            request=self.request,
        )
        return organisation_view.get_member_role_id(
            self.organisation, self.webhelpers.get_current_account()
        ) in ["admin", "owner"]

    def handle_POST(self):
        """Handle the POST request."""
        self.context.session.consultant = self.consultant
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
