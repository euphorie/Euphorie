"""
User
----

This provides the basic functionality for user-, login- and authentication
handling. It is used by :obj:`euphorie.content.sector` and
:obj:`euphorie.content.countrymanager`
"""

from .. import MessageFactory as _
from Acquisition import aq_base
from Acquisition import aq_chain
from euphorie.content.widgets.password import PasswordWithConfirmationFieldWidget
from plone import api
from plone.autoform import directives
from plone.supermodel import model
from plone.uuid.interfaces import IUUID
from Products.CMFCore.interfaces import ISiteRoot
from Products.membrane.interfaces import user as membrane
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.datamanager import AttributeField
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import IValidator
from z3c.form.validator import SimpleFieldValidator
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.event import notify
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema import ValidationError

import bcrypt
import logging
import re


log = logging.getLogger(__name__)
RE_LOGIN = re.compile(r"^[a-z][a-z0-9-]+$")


class DuplicateLoginError(ValidationError):
    __doc__ = _("error_existing_login", default="This login name is already taken.")


def validLoginValue(value):
    if not RE_LOGIN.match(value):
        raise Invalid(
            _(
                "error_invalid_login",
                default="A login name may only consist of lowercase letters "
                "and numbers.",
            )
        )
    return True


class LoginField(schema.TextLine):
    """A login name."""


def _check_password(value):
    """Check that the password satisfies our site policy."""
    if not value:
        return True
    regtool = api.portal.get_tool("portal_registration")
    err = regtool.pasValidation("password", value)
    if err:
        raise Invalid(err)
    # raise Invalid(_("Password doesn't compare with confirmation value"))
    return True


class IUser(model.Schema):
    title = schema.TextLine(title=_("label_user_title", default="Name"), required=True)

    contact_email = schema.TextLine(
        title=_("label_contact_email", default="Contact email address"), required=True
    )

    login = LoginField(
        title=_("label_login_name", default="Login name"),
        required=True,
        constraint=validLoginValue,
    )
    directives.write_permission(login="euphorie.content.ManageCountry")

    password = schema.Password(
        title=_("label_password", default="Password"),
        required=True,
        constraint=_check_password,
    )
    directives.widget(password=PasswordWithConfirmationFieldWidget)

    locked = schema.Bool(
        title=_("label_account_locked", default="Account is locked"),
        required=False,
        default=False,
    )
    directives.write_permission(locked="euphorie.content.ManageCountry")


class BaseValidator(SimpleFieldValidator):
    def __init__(self, context, request, view, field, widget):
        self.context = context
        self.request = request
        self.view = view
        self.field = field
        self.widget = widget


@adapter(Interface, Interface, IAddForm, LoginField, Interface)
@implementer(IValidator)
class UniqueLoginValidator(BaseValidator):
    def validate(self, value):
        """Ensure that there isn't already a user id isn't already in use.

        :raises: DuplicateLoginError
        """
        super().validate(value)
        site = getUtility(ISiteRoot)
        for parent in aq_chain(site):
            if hasattr(aq_base(parent), "acl_users"):
                if parent.acl_users.searchUsers(login=value, exact_match=True):
                    raise DuplicateLoginError(value)


@adapter(IUser)
class UserProvider:
    """Base class for membrane adapters for :obj:`IUser` instances.

    This base class implements the
    :obj:`Products.membrane.interfaces.IMembraneUserObject` interface which is
    responisble for generating an id for a user object.

    This adapter does not claim to implement the `IMembraneUserObject`
    interface itself, since that would complicate the registration of the other
    adapters a little bit (`zope.component` can no longer determine the
    interface provided by an adapter if it provides multiple interfaces, even
    if they are derived classes).
    """

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        uuid = IUUID(self.context, None)
        if uuid is None:
            # BBB for older instances
            return self.context.id
        return uuid

    def getUserName(self):
        return self.context.login


@adapter(IUser)
@implementer(membrane.IMembraneUserAuth)
class UserAuthentication(UserProvider):
    """Account authentication routines.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserAuth` interface. This
    interface is responsible for the authentication logic of accounts.
    """

    def authenticateCredentials(self, credentials):
        if self.context.locked:
            IStatusMessage(self.context.REQUEST).add(
                _(
                    "message_user_locked",
                    default='Account "${title}" has been locked.',
                    mapping=dict(title=self.context.title),
                ),
                "warn",
            )
            return None
        candidate = credentials.get("password", None)
        real = getattr(aq_base(self.context), "password", None)
        if candidate is None or real is None:
            return None
        max_attempts = api.portal.get_registry_record(
            "euphorie.max_login_attempts", default=0
        )

        if candidate == real:  # XXX: Plain passwords should be deprecated
            log.warning(
                "Passwords should not be stored unhashed. Please run "
                "the upgrade step to make sure all plaintext passwords are "
                "hashed."
            )
            self.context._v_login_attempts = 0
            return (self.getUserId(), self.getUserName())

        if bcrypt.hashpw(candidate, real) == real:
            self.context._v_login_attempts = 0
            return (self.getUserId(), self.getUserName())
        return self.applyLockoutPolicy(max_attempts)

    def applyLockoutPolicy(self, max_attempts):
        if not max_attempts:
            return
        if not hasattr(aq_base(self.context), "_v_login_attempts"):
            self.context._v_login_attempts = 0
        self.context._v_login_attempts += 1

        if self.context._v_login_attempts < max_attempts:
            IStatusMessage(self.context.REQUEST).add(
                _(
                    "message_lock_warn",
                    default="Please be aware that you have %s more login "
                    "attempts before your account will be locked."
                    % (max_attempts - self.context._v_login_attempts),
                ),
                "warn",
            )
        else:
            log.warning(
                "Account locked for %s, due to more than %s unsuccessful "
                "login attempts" % (self.getUserName(), max_attempts)
            )
            IStatusMessage(self.context.REQUEST).add(
                _(
                    "message_user_locked",
                    default='Account "${title}" has been locked.',
                    mapping=dict(title=self.context.title),
                ),
                "warn",
            )
            self.context.locked = True


@adapter(IUser)
@implementer(membrane.IMembraneUserChanger)
class UserChanger(UserProvider):
    """Account password changing.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserChanger` interface.
    This interface is responsible for changing a users password.
    """

    def doChangeUser(self, userid, password, **kwargs):
        """Set the login name and password for a user.

        Changing the username is not allowed, and any attempt to do so will
        raise a `ValueError`.

        The *password* parameter is the plaintext password.
        """
        if userid != self.getUserId():
            raise ValueError("Userid changes are not allowed")
        self.context.password = bcrypt.hashpw(password, bcrypt.gensalt())


@adapter(IUser, schema.interfaces.IPassword)
@implementer(IDataManager)
class PasswordDataManager(AttributeField):
    """Hash passwords before storing them."""

    def set(self, value):
        super().set(bcrypt.hashpw(value, bcrypt.gensalt()))


@adapter(IUser)
@implementer(membrane.IMembraneUserProperties)
class UserProperties(UserProvider):
    """User properties handling.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserProperties` interface.
    This interface is responsible all handling of member properties.

    The interface is based on the basic PAS plugin
    :obj:`Products.PluggableAuthService.interfaces.IMutablePropertiesPlugin`
    interface. As a result all methods take a `user` parameter, which should
    always be the same as the adapted object for membrane adapters.
    """

    # A mapping for IUser properties to Plone user properties
    property_map = [("title", "fullname"), ("contact_email", "email")]

    def getPropertiesForUser(self, user, request=None):
        properties = {}
        for content_prop, user_prop in self.property_map:
            value = getattr(self.context, content_prop)
            # None values are not allowed so replace those with an empty string
            properties[user_prop] = (value is not None) and value or ""
        return properties

    def setPropertiesForUser(self, user, propertysheet):
        marker = []
        changes = set()
        for content_prop, user_prop in self.property_map:
            value = propertysheet.getProperty(user_prop, default=marker)
            if value is not marker:
                setattr(self.context, content_prop, value)
                changes.add(content_prop)

        if changes:
            self.context.reindexObject(idxs=list(changes))
            notify(ObjectModifiedEvent(self.context))
