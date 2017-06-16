"""
User
----

This provides the basic functionality for user-, login- and authentication
handling. It is used by :obj:`euphorie.content.sector` and
:obj:`euphorie.content.countrymanager`
"""

import re
import bcrypt
import logging
from .. import MessageFactory as _
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.Archetypes.BaseObject import shasattr
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFCore.interfaces import ISiteRoot
from Products.membrane.interfaces import user as membrane
from Products.statusmessages.interfaces import IStatusMessage
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.uuid.interfaces import IUUID
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plone import api
from z3c.appconfig.interfaces import IAppConfig
from z3c.form.datamanager import AttributeField
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import IForm
from z3c.form.interfaces import IValidator
from z3c.form.validator import SimpleFieldValidator
from zExceptions import Unauthorized
from zope import schema
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.event import notify
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema import ValidationError
from p01.widget.password.interfaces import IPasswordConfirmationWidget
from p01.widget.password.widget import PasswordConfirmationValidator

log = logging.getLogger(__name__)
RE_LOGIN = re.compile(r"^[a-z][a-z0-9-]+$")


class DuplicateLoginError(ValidationError):
    __doc__ = _("error_existing_login",
            default=u"This login name is already taken.")


class InvalidPasswordError(ValidationError):
    def __init__(self, value, doc):
        self.value = value
        self._doc = doc

    def doc(self):
        return self._doc


def validLoginValue(value):
    if not RE_LOGIN.match(value):
        raise Invalid(_("error_invalid_login",
            default=u"A login name may only consist of lowercase letters "
                    u"and numbers."))
    return True


class LoginField(schema.TextLine):
    """A login name."""


class IUser(form.Schema):
    title = schema.TextLine(
            title=_("label_user_title", default=u"Name"),
            required=True)

    contact_email = schema.TextLine(
            title=_("label_contact_email", default=u"Contact email address"),
            required=True)

    login = LoginField(
            title=_("label_login_name", default=u"Login name"),
            required=True,
            constraint=validLoginValue)
    dexterity.write_permission(login="euphorie.content.ManageCountry")

    password = schema.Password(
            title=_("label_password", default=u"Password"),
            required=True)

    locked = schema.Bool(
            title=_("label_account_locked", default=u"Account is locked"),
            required=False,
            default=False)
    dexterity.write_permission(locked="euphorie.content.ManageCountry")


class BaseValidator(SimpleFieldValidator):

    def __init__(self, context, request, view, field, widget):
        self.context = context
        self.request = request
        self.view = view
        self.field = field
        self.widget = widget

class UniqueLoginValidator(grok.MultiAdapter, BaseValidator):
    grok.implements(IValidator)
    grok.adapts(Interface, Interface, IAddForm, LoginField, Interface)

    def validate(self, value):
        """ Ensure that there isn't already a user id isn't already in use.

        :raises: DuplicateLoginError
        """
        super(UniqueLoginValidator, self).validate(value)
        site = getUtility(ISiteRoot)
        for parent in aq_chain(site):
            if hasattr(aq_base(parent), "acl_users"):
                if parent.acl_users.searchUsers(login=value, exact_match=True):
                    raise DuplicateLoginError(value)


class PasswordValidator(grok.MultiAdapter, PasswordConfirmationValidator):
    grok.implements(IValidator)
    grok.adapts(Interface, Interface, IForm, schema.Password, IPasswordConfirmationWidget)

    def validate(self, value):
        """ Ensure that the password complies with the policy configured in
        portal_registration.

        :raises: InvalidPasswordError
        """
        super(PasswordValidator, self).validate(value)
        regtool = api.portal.get_tool('portal_registration')
        err = regtool.pasValidation('password', value)
        if err:
            raise InvalidPasswordError(value, err)


class UserProvider(object):
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
    adapts(IUser)

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


class UserAuthentication(grok.Adapter, UserProvider):
    """Account authentication routines.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserAuth` interface. This
    interface is responsible for the authentication logic of accounts.
    """
    grok.context(IUser)
    grok.implements(membrane.IMembraneUserAuth)

    def authenticateCredentials(self, credentials):
        if self.context.locked:
            IStatusMessage(self.context.REQUEST).add(
                _("message_user_locked",
                default=u'Account "${title}" has been locked.',
                mapping=dict(title=self.context.title)
                ), "warn"
            )
            return None
        candidate = credentials.get("password", None)
        real = getattr(aq_base(self.context), "password", None)
        if candidate is None or real is None:
            return None
        conf = getUtility(IAppConfig).get("euphorie", {})
        max_attempts = int(conf.get('max_login_attempts', '0').strip())

        if candidate == real: # XXX: Plain passwords should be deprecated
            log.warn("Passwords should not be stored unhashed. Please run "
                "the upgrade step to make sure all plaintext passwords are "
                "hashed.")
            self.context._v_login_attempts = 0
            return (self.getUserId(), self.getUserName())

        if bcrypt.hashpw(candidate, real) == real:
            self.context._v_login_attempts = 0
            return (self.getUserId(), self.getUserName())
        return self.applyLockoutPolicy(max_attempts)

    def applyLockoutPolicy(self, max_attempts):
        if not max_attempts:
            return
        if not shasattr(self.context, '_v_login_attempts'):
            self.context._v_login_attempts = 0
        self.context._v_login_attempts += 1

        if self.context._v_login_attempts < max_attempts:
            IStatusMessage(self.context.REQUEST).add(
                _("message_lock_warn",
                    default=u"Please be aware that you have %s more login " \
                            u"attempts before your account will be locked." \
                            % (max_attempts-self.context._v_login_attempts),
                ), "warn"
            )
        else:
            log.warn("Account locked for %s, due to more than %s unsuccessful "
                    "login attempts" % (self.getUserName(), max_attempts))
            IStatusMessage(self.context.REQUEST).add(
                _("message_user_locked",
                default=u'Account "${title}" has been locked.',
                mapping=dict(title=self.context.title)
                ), "warn"
            )
            self.context.locked = True


class UserChanger(grok.Adapter, UserProvider):
    """Account password changing.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserChanger` interface.
    This interface is responsible for changing a users password.
    """
    grok.context(IUser)
    grok.implements(membrane.IMembraneUserChanger)

    def doChangeUser(self, userid, password, **kwargs):
        """Set the login name and password for a user.

        Changing the username is not allowed, and any attempt to do so will
        raise a `ValueError`.

        The *password* parameter is the plaintext password.
        """
        if userid != self.getUserId():
            raise ValueError("Userid changes are not allowed")
        self.context.password = bcrypt.hashpw(password, bcrypt.gensalt())


class PasswordDataManager(AttributeField, grok.MultiAdapter):
    """ Hash passwords before storing them
    """
    grok.implements(IDataManager)
    grok.adapts(IUser, schema.interfaces.IPassword)

    def set(self, value):
        super(PasswordDataManager, self).set(
            bcrypt.hashpw(value, bcrypt.gensalt())
        )


class UserProperties(grok.Adapter, UserProvider):
    """User properties handling.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserProperties` interface.
    This interface is responsible all handling of member properties.

    The interface is based on the basic PAS plugin
    :obj:`Products.PluggableAuthService.interfaces.IMutablePropertiesPlugin`
    interface. As a result all methods take a `user` parameter, which should
    always be the same as the adapted object for membrane adapters.
    """
    grok.context(IUser)
    grok.implements(membrane.IMembraneUserProperties)

    # A mapping for IUser properties to Plone user properties
    property_map = [("title", "fullname"),
                    ("contact_email", "email")]

    def getPropertiesForUser(self, user, request=None):
        properties = {}
        for (content_prop, user_prop) in self.property_map:
            value = getattr(self.context, content_prop)
            # None values are not allowed so replace those with an empty string
            properties[user_prop] = (value is not None) and value or u""
        return properties

    def setPropertiesForUser(self, user, propertysheet):
        marker = []
        changes = set()
        for (content_prop, user_prop) in self.property_map:
            value = propertysheet.getProperty(user_prop, default=marker)
            if value is not marker:
                setattr(self.context, content_prop, value)
                changes.add(content_prop)

        if changes:
            self.context.reindexObject(idxs=list(changes))
            notify(ObjectEditedEvent(self.context))


class Lock(grok.View):
    """ Lock or unlock a User account.

    View name: @@lock
    """
    grok.context(IUser)
    grok.require("euphorie.content.ManageCountry")
    grok.layer(NuPloneSkin)
    grok.name("lock")

    def render(self):
        if self.request.method != "POST":
            raise Unauthorized
        authenticator = getMultiAdapter((self.context, self.request),
                name=u"authenticator")
        if not authenticator.verify():
            raise Unauthorized

        self.context.locked = locked = \
                (self.request.form.get("action", "lock") == "lock")
        flash = IStatusMessage(self.request).addStatusMessage
        if locked:
            flash(_("message_user_locked",
                    default=u'Account "${title}" has been locked.',
                    mapping=dict(title=self.context.title)), "success")
        else:
            flash(_("message_user_unlocked",
                    default=u'Account "${title}" has been unlocked.',
                    mapping=dict(title=self.context.title)), "success")

        country = aq_parent(aq_inner(self.context))
        self.request.response.redirect(
                "%s/@@manage-users" % country.absolute_url())
