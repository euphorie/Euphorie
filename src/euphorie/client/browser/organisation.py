from BTrees.OOBTree import OOBTree
from copy import deepcopy
from euphorie.client import MessageFactory as _
from euphorie.client.browser.base import BaseView
from euphorie.client.model import Account
from euphorie.client.model import Organisation
from euphorie.client.model import OrganisationMembership
from euphorie.client.utils import CreateEmailTo
from plone import api
from plone.memoize.view import memoize
from plone.memoize.view import memoize_contextless
from plone.protect.auto import safeWrite
from plone.protect.interfaces import IDisableCSRFProtection
from plone.scale.scale import scaleImage
from plone.uuid.interfaces import IUUIDGenerator
from Products.CMFPlone.utils import getAllowedSizes
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sqlalchemy import sql
from textwrap import dedent
from time import time
from urllib.parse import quote
from zExceptions import NotFound
from zExceptions import Unauthorized
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import logging


logger = logging.getLogger(__name__)


class OrganisationBaseView(BaseView):
    """Base class for all organisation views."""

    default_target_view = "@@organisation"

    @property
    def _known_roles(self):
        roles = [
            {
                "value": "member",
                "label": _("Member"),
            },
            # XXX commented for the moment because it is still under discussion
            # {
            #     "value": "manager",
            #     "label": _("Manager/Policy maker"),
            # },
            {
                "value": "admin",
                "label": _("Administrator"),
            },
        ]

        if self.webhelpers.use_consultancy_phase:
            roles.insert(
                1,
                {
                    "value": "consultant",
                    "label": _("label_role_consultant", default="Consultant"),
                },
            )
        return roles

    @property
    def is_training_enabled(self):
        return self.webhelpers.use_training_module

    @property
    def default_organisation_title(self):
        """Return the default title for a new organisation or an orgasination
        without a title set."""
        account = self.webhelpers.get_current_account()
        name = account.first_name or account.loginname
        return api.portal.translate(
            _(
                "default_organisation_title",
                default="Organisation of ${name}",
                mapping={"name": name},
            )
        )

    def get_organisation_title(self, organisation):
        """Return the title of the organisation."""
        if not organisation:
            return "TODO: FIXME"
        return organisation.title or self.default_organisation_title

    @property
    @memoize
    def organisation_title(self):
        """The title of the organisation bound to this account (if it exists)
        or the account login name."""
        return self.get_organisation_title(self.organisation)

    def get_member_role_id(self, organization, user):
        """Return the role of the user in the organization."""
        if organization.owner_id == user.id:
            return "owner"
        membership = (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                OrganisationMembership.owner_id == organization.owner_id,
                OrganisationMembership.member_id == user.id,
            )
            .first()
        )
        if not membership:
            return None
        return membership.member_role

    @memoize_contextless
    def translate_role_id(self, role_id):
        """Return the translated role value."""
        for role in self._known_roles:
            if role["value"] == role_id:
                return api.portal.translate(role["label"])
        return role_id

    @property
    @memoize
    def organisations(self):
        account = self.webhelpers.get_current_account()
        if not account:
            return []

        organisations = []
        if not account.organisation:
            organisation = Organisation(
                owner_id=account.id, title=self.default_organisation_title
            )
            alsoProvides(self.request, IDisableCSRFProtection)
            self.sqlsession.add(organisation)
            account.organisation = organisation

        organisations.append(account.organisation)

        # Extend with the organisation the account is member of
        organisations.extend(
            sorted(
                self.sqlsession.query(Organisation)
                .join(
                    OrganisationMembership,
                    Organisation.owner_id == OrganisationMembership.owner_id,
                )
                .filter(OrganisationMembership.member_id == account.id),
                key=self.get_organisation_title,
            )
        )
        return organisations


class View(OrganisationBaseView):
    @memoize
    def get_memberships(self, organisation):
        return (
            self.sqlsession.query(Account, OrganisationMembership)
            .join(
                OrganisationMembership,
                OrganisationMembership.member_id == Account.id,
            )
            .filter(OrganisationMembership.owner_id == organisation.owner_id)
            .order_by(Account.loginname)
            .all()
        )


class PanelAddOrganisation(OrganisationBaseView):
    def handle_POST(self):
        """Handle the POST request."""
        title = self.request.form.get("title")
        if not title:
            return self.redirect(
                msg=_("You need to specify a title for the organisation.")
            )
        account = self.webhelpers.get_current_account()
        if account.organisation:
            return self.redirect(msg=_("You already have an organisation."))

        organisation = Organisation(owner_id=account.id, title=title)
        self.sqlsession.add(organisation)

        logo = self.request.form.get("logo")
        if logo:
            organisation.image_data = logo.read()
            organisation.image_filename = logo.filename
            # The scale will be recreated on the fly
            organisation.image_data_scaled = None
        return self.redirect(msg=_("Organisation added"))


@implementer(IPublishTraverse)
class PanelAddUser(OrganisationBaseView):
    """Panel to add a new user to an organisation."""

    storage_key = "euphorie.add_user_to_organisation_tokens"
    days_to_keep = 5

    organisation_id_key = "organisation_id"

    def publishTraverse(self, request, organisation_id):
        request.set(self.organisation_id_key, organisation_id)
        return self

    @property
    def role_options(self):
        """Return a list of options for the role field."""
        options = deepcopy(self._known_roles)
        options[0]["checked"] = "checked"
        return options

    @property
    @memoize_contextless
    def organisation(self):
        """Get the organisation requested, defaults to the current user
        organisation."""
        organisation_id = self.request.get(self.organisation_id_key)
        account = self.webhelpers.get_current_account()
        if not organisation_id:
            return account.organisation

        organisation = self.sqlsession.query(Organisation).get(
            self.request.get(self.organisation_id_key)
        )
        if not organisation:
            return

        # Check if the user can manage users to the current organisation
        account_id = account.id
        if organisation.owner_id == account_id:
            # The user is the owner, return the organisation
            return organisation

        if (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                sql.and_(
                    OrganisationMembership.owner_id == organisation.owner_id,
                    OrganisationMembership.member_id == account_id,
                    OrganisationMembership.member_role == "admin",
                )
            )
            .count()
        ):
            # The user is a member, return the organisation
            return organisation

        raise Unauthorized("You are not allowed to edit this organisation")

    @property
    def subject(self):
        return api.portal.translate(
            _(
                "subject_add_user_to_organisation_email",
                default="Confirm OiRA membership to ’${organisation}’",
                mapping={"organisation": self.organisation_title},
            )
        )

    @property
    def body(self):
        """The mail body.

        This has to be quite simple because it is used in a mailto link.
        """
        body = _(
            "body_add_user_to_organisation_email",
            default="""
            I hereby invite you to join our organisation on OiRA.
            Once you've accepted your membership,
            we can collaborate on risk assessments.

            Please log in or register via the link below
            and accept your membership.
            This link will stay valid for ${days_to_keep} days.

            ${link}
            """,
            mapping={
                "days_to_keep": self.days_to_keep,
                "link": (
                    f"{self.context.absolute_url()}/"
                    f"@@confirm-organisation-invite/{self.token}"
                ),
            },
        )
        return dedent(api.portal.translate(body)).strip()

    @property
    @memoize_contextless
    def storage(self):
        annotations = IAnnotations(api.portal.get())
        if self.storage_key not in annotations:
            safeWrite(annotations)
            annotations[self.storage_key] = OOBTree()
        return annotations[self.storage_key]

    @property
    @memoize_contextless
    def token(self):
        storage = self.storage
        safeWrite(storage)

        # clean up expired tokens
        now = time()
        expires = now + self.days_to_keep * 86400

        for key, value in storage.items():
            if value.get("expires", 0) < now:
                storage.pop(key)

        uuid_generator = getUtility(IUUIDGenerator)
        token = uuid_generator()
        storage[token] = {
            "userid": self.webhelpers.get_current_account().id,
            "organisation_id": self.organisation.organisation_id,
            "expires": expires,
            "role": self.request.form.get("role", "member"),
        }
        return token

    def handle_POST(self):
        """Handle the POST request."""
        role = self.request.get("role")
        if role not in [_["value"] for _ in self._known_roles]:
            return self.redirect(msg=_("The role is invalid"), meg_type="error")

        # Note urllib.parse.urlencode does not work with every mailclient
        target = f"mailto:?subject={quote(self.subject)}&body={quote(self.body)}"
        return self.redirect(target)


@implementer(IPublishTraverse)
class ConfirmInvite(BaseView):
    """Confirm the invite to join an organisation."""

    storage_key = PanelAddUser.storage_key
    email_template = ViewPageTemplateFile("templates/notify-invite-accept.pt")

    def publishTraverse(self, request, token):
        self.request.set(self.storage_key, token)
        return self

    @property
    @memoize_contextless
    def storage(self):
        annotations = IAnnotations(api.portal.get())
        storage = annotations.get(self.storage_key, {})
        return storage

    @property
    @memoize_contextless
    def token_value(self):
        token = self.request.get(self.storage_key)
        if not token:
            raise NotFound("Token not found")
        return self.storage.get(token)

    @property
    @memoize_contextless
    def organisation(self):
        if not self.token_value:
            return
        return self.sqlsession.query(Organisation).get(
            self.token_value["organisation_id"]
        )

    @property
    @memoize_contextless
    def inviter(self):
        if not self.token_value:
            return None
        userid = self.token_value["userid"]
        try:
            user = self.sqlsession.query(Account).filter(Account.id == userid).first()
        except Exception:
            logger.warning("Unable to fetch account for username:")
            logger.warning(userid)
            return None
        return user

    @property
    def inviter_fullname(self):
        user = self.inviter
        if user is None:
            return ""
        return user.title

    @property
    def inviter_firstname(self):
        user = self.inviter
        if user is None:
            return ""
        return user.first_name or user.title

    @property
    def default_target_view(self):
        view = "@@organisation"
        organisation = self.organisation
        if not self.organisation:
            return view
        account = self.webhelpers.get_current_account()
        if account.organisation == organisation or (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                sql.and_(
                    OrganisationMembership.owner_id == organisation.owner_id,
                    OrganisationMembership.member_id == account.id,
                )
            )
            .count()
        ):
            # The user is a member, return the organisation
            return f"{view}#org-{organisation.organisation_id}"
        return view

    @property
    def email_from_name(self):
        return api.portal.get_registry_record("plone.email_from_name")

    @property
    def email_from_address(self):
        return api.portal.get_registry_record("plone.email_from_address")

    def notify_inviter(self):
        invitee = self.webhelpers.get_current_account()
        invitee_firstname = invitee.first_name or invitee.title
        body = self.email_template(
            inviter=self.inviter_firstname,
            invitee=invitee_firstname,
            organisation=self.organisation.title,
        )
        subject = api.portal.translate(
            _(
                "subject_notify_invite_accept",
                default="Membership to your organisation accepted",
            )
        )
        mail = CreateEmailTo(
            self.email_from_name,
            self.email_from_address,
            invitee.email,
            subject,
            body,
        )

        api.portal.send_email(
            body=mail,
            recipient=self.inviter.email,
            sender=self.email_from_address,
            subject=subject,
        )
        logger.info("Sent email confirmation to %s", self.inviter.email)

    def lookup_token_and_redirect(self):
        """Check that:

        - we have the token
        - the token is valid
        - the token is not expired
        - the owner of the organisation is not adding himself
        - the user is not already a member of the organisation

        If that works, add the user to the organisation
        """
        value = self.token_value
        if not value:
            return self.redirect(
                msg=_(
                    "message_add_user_to_organisation_invalid",
                    default="We could not find the invitation you are looking for.",
                )
            )

        organisation = self.organisation
        organisation_title = organisation.title

        if value["expires"] < time():
            return self.redirect(
                msg=_(
                    "message_add_user_to_organisation_expired",
                    default=(
                        "The invitation from the ${name} "
                        "organisation is not valid anymore."
                    ),
                    mapping={"name": organisation_title},
                )
            )

        current_account = self.webhelpers.get_current_account()
        if current_account.id == organisation.owner_id:
            return self.redirect(
                msg=_(
                    "message_add_user_to_organisation_self",
                    default="You cannot add yourself to your organisation.",
                )
            )

        if (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                sql.and_(
                    OrganisationMembership.owner_id == organisation.owner_id,
                    OrganisationMembership.member_id == current_account.id,
                )
            )
            .count()
        ):
            return self.redirect(
                msg=_(
                    "message_add_user_to_organisation_already_member",
                    default="You are already a member of the ${name} organisation.",
                    mapping={"name": organisation_title},
                )
            )

        obj = OrganisationMembership(
            owner_id=organisation.owner_id,
            member_id=current_account.id,
            member_role=value["role"],
        )
        alsoProvides(self.request, IDisableCSRFProtection)
        self.sqlsession.add(obj)
        self.notify_inviter()

        return self.redirect(
            msg=_(
                "message_add_user_to_organisation_success",
                default="You have been added to the ${name} organisation.",
                mapping={"name": organisation_title},
            )
        )

    def handle_POST(self):
        if self.request.form.get("submit", "") == "accept":
            self.lookup_token_and_redirect()
        else:
            return self.redirect(
                msg=_(
                    "message_add_user_to_organisation_declined",
                    default=(
                        "You have declined the invitation to the ${name} "
                        "organisation."
                    ),
                    mapping={"name": self.organisation.title},
                ),
                target=f"{self.context.absolute_url()}",
            )


@implementer(IPublishTraverse)
class PanelEditOrganisation(OrganisationBaseView):
    """Panel to edit a user organisation."""

    organisation_id_key = "organisation_id"

    def publishTraverse(self, request, token):
        self.request.set(self.organisation_id_key, token)
        return self

    @property
    @memoize_contextless
    def organisation(self):
        """Get the organisation requested, defaults to the current user
        organisation."""
        organisation_id = self.request.get(self.organisation_id_key)
        account = self.webhelpers.get_current_account()
        if not organisation_id:
            return account.organisation

        organisation = self.sqlsession.query(Organisation).get(
            self.request.get(self.organisation_id_key)
        )
        if not organisation:
            return

        # Check if the organisation should be workable for the current account
        account_id = account.id
        if organisation.owner_id == account_id:
            # The user is the owner, return the organisation
            return organisation

        if (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                sql.and_(
                    OrganisationMembership.owner_id == organisation.owner_id,
                    OrganisationMembership.member_id == account_id,
                    OrganisationMembership.member_role == "admin",
                )
            )
            .count()
        ):
            # The user is a member, return the organisation
            return organisation

        raise Unauthorized("You are not allowed to edit this organisation")

    @property
    @memoize
    def has_logo(self):
        return self.organisation and self.organisation.image_data is not None

    def handle_POST(self):
        """Handle the POST request."""
        organisation = self.organisation
        if not organisation:
            organisation = Organisation(
                owner_id=self.webhelpers.get_current_account().id
            )
            self.sqlsession.add(organisation)
        organisation.title = self.request.form.get("title")
        logo_operation = self.request.form.get("logo_operation")
        if logo_operation in ("upload", "replace"):
            logo = self.request.form.get("logo")
            if logo:
                organisation.image_data = logo.read()
                organisation.image_filename = logo.filename
                # The scale will be recreated on the fly
                organisation.image_data_scaled = None
        elif logo_operation == "remove":
            organisation.image_data = None
            organisation.image_data_scaled = None
            organisation.image_filename = None
        self.redirect(target=f"{self.context.absolute_url()}/@@organisation")


@implementer(IPublishTraverse)
class OrganisationLogo(OrganisationBaseView):
    """View to serve the organisation logo."""

    organisation_id_key = "organisation_id"

    def publishTraverse(self, request, token):
        self.request.set(self.organisation_id_key, token)
        return self

    @property
    @memoize_contextless
    def organisation(self):
        """Get the organisation requested, defaults to the current user
        organisation."""
        organisation_id = self.request.get(self.organisation_id_key)
        account = self.webhelpers.get_current_account()
        if not organisation_id:
            return account.organisation

        organisation = self.sqlsession.query(Organisation).get(
            self.request.get(self.organisation_id_key)
        )
        if not organisation:
            return

        return organisation

    def get_or_create_image_scaled(self):
        """Get the image scaled."""
        organisation = self.organisation
        if organisation.image_data_scaled:
            return organisation.image_data_scaled
        scale = getAllowedSizes().get("preview", (400, 400))
        scaled_image_io = scaleImage(organisation.image_data, width=scale[0])[0]
        alsoProvides(self.request, IDisableCSRFProtection)
        if isinstance(scaled_image_io, bytes):
            organisation.image_data_scaled = scaled_image_io
        else:
            organisation.image_data_scaled = scaled_image_io.getvalue()
        return organisation.image_data_scaled

    def __call__(self):
        organisation = self.organisation

        if not organisation:
            raise NotFound("Organisation not found")

        if not organisation.image_data:
            raise NotFound("Organisation logo not found")

        self.request.response.setHeader(
            "Content-Type",
            (
                "image/png"
                if organisation.image_filename.endswith(".png")
                else "image/jpeg"
            ),
        )
        self.request.response.setHeader(
            "Content-Disposition",
            f"inline; filename={organisation.image_filename}",
        )
        return self.get_or_create_image_scaled()


@implementer(IPublishTraverse)
class MemberMoreMenu(OrganisationBaseView):
    def publishTraverse(self, request, membership_id):
        request.set("membership_id", membership_id)
        return self


@implementer(IPublishTraverse)
class PanelMemberEdit(OrganisationBaseView):
    """Panel to edit a member in the context of this organisation."""

    def publishTraverse(self, request, membership_id):
        request.set("membership_id", membership_id)
        return self

    @property
    @memoize
    def membership(self):
        """Return the role of the member in the organisation."""
        membership_id = self.request.get("membership_id")
        account = self.webhelpers.get_current_account()
        membership = (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                OrganisationMembership.organisation_id == membership_id,
                sql.or_(
                    OrganisationMembership.owner_id == account.id,
                    sql.and_(
                        OrganisationMembership.member_id == account.id,
                        OrganisationMembership.member_role == "admin",
                    ),
                ),
            )
            .first()
        )
        if not membership:
            raise Unauthorized("You cannot edit this organisation")
        return membership

    @property
    @memoize
    def organisation(self):
        return (
            self.sqlsession.query(Organisation)
            .filter(Organisation.owner_id == self.membership.owner_id)
            .first()
        )

    @property
    @memoize
    def edited_member(self):
        """Return the member to edit."""
        return self.sqlsession.query(Account).get(self.membership.member_id)

    @property
    def role_options(self):
        """Return a list of options for the role field."""
        options = deepcopy(self._known_roles)
        current_value = self.membership.member_role
        for option in options:
            if option["value"] == current_value:
                option["checked"] = "checked"
        return options

    def validate(self):
        if not self.membership:
            raise NotFound("Member not found")

    def handle_POST(self):
        """Handle the POST request."""
        new_role = self.request.form.get("role")
        # Validate that the role is something allowed
        if new_role != self.membership.member_role:
            if new_role not in [_["value"] for _ in self._known_roles]:
                return self.redirect(msg=_("The role is invalid"), meg_type="error")
            self.membership.member_role = new_role
            return self.redirect(msg=_("Member updated"))
        return self.redirect()


@implementer(IPublishTraverse)
class PanelMemberRemove(OrganisationBaseView):
    """Panel to remove a member from this organisation."""

    def publishTraverse(self, request, membership_id):
        request.set("membership_id", membership_id)
        return self

    @property
    @memoize
    def membership(self):
        """Return the role of the member in the organisation."""
        membership_id = self.request.get("membership_id")
        account = self.webhelpers.get_current_account()
        membership = (
            self.sqlsession.query(OrganisationMembership)
            .filter(
                OrganisationMembership.organisation_id == membership_id,
                sql.or_(
                    OrganisationMembership.owner_id == account.id,
                    sql.and_(
                        OrganisationMembership.member_id == account.id,
                        OrganisationMembership.member_role == "admin",
                    ),
                ),
            )
            .first()
        )
        if not membership:
            raise Unauthorized("You cannot edit this organisation")
        return membership

    @property
    @memoize
    def organisation(self):
        return (
            self.sqlsession.query(Organisation)
            .filter(Organisation.owner_id == self.membership.owner_id)
            .first()
        )

    @property
    @memoize
    def member_to_remove(self):
        return self.sqlsession.query(Account).get(self.membership.member_id)

    def validate(self):
        if not self.membership:
            raise NotFound("Member not found")

    def handle_POST(self):
        """Handle the POST request."""
        self.sqlsession.delete(self.membership)
        return self.redirect(msg=_("Member removed"))
