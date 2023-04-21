from euphorie.client.browser.base import BaseView
from euphorie.client.model import Account
from euphorie.client.model import OrganisationMembership
from plone import api
from plone.memoize.view import memoize
from Products.Five import BrowserView


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

    @property
    @memoize
    def organisation(self):
        return self.webhelpers.traversed_session.session.account.organisation

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

    def handle_POST(self):
        """Handle the POST request."""
        consultant_id = self.request.form.get("consultant")
        consultant = (
            self.sqlsession.query(Account).filter(Account.id == consultant_id).one()
        )
        self.webhelpers.traversed_session.session.consultant = consultant
        # XXX send mail
        self.redirect()
