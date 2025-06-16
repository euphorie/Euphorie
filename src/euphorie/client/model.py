"""
Model
-----

Mainly: the connection between the ZODB-based content of the backend and the
SQL-based individual session content of the client users.
Also: PAS-based user account for users of the client
"""

from AccessControl.interfaces import IUser
from AccessControl.PermissionRole import _what_not_even_god_should_do
from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from collections import defaultdict
from euphorie.client.client import IClient
from euphorie.client.config import LOCKING_ACTIONS
from euphorie.client.config import LOCKING_SET_ACTIONS
from euphorie.client.enum import Enum
from OFS.interfaces import IApplication
from plone import api
from plone.app.event.base import localized_now
from plone.base.utils import safe_text
from plone.memoize import ram
from plone.memoize.instance import memoize
from Products.Five import BrowserView
from sqlalchemy import func
from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import sql
from sqlalchemy import types
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative.extensions import instrument_declarative
from sqlalchemy.orm.decl_base import _declarative_constructor
from sqlalchemy.sql import functions
from z3c.saconfig import Session
from zope.component.hooks import getSite
from zope.deprecation import deprecate
from zope.interface import implementer
from zope.interface import Interface
from zope.sqlalchemy import datamanager

import Acquisition
import bcrypt
import datetime
import logging
import OFS.Traversable
import pytz
import random
import re


BCRYPTED_PATTERN = re.compile(r"^\$2[aby]?\$\d{1,2}\$[.\/A-Za-z0-9]{53}$")

metadata = schema.MetaData()

log = logging.getLogger(__name__)


def _forever_cache_key(func, self, *args):
    """Cache this function call forever."""
    return (func.__name__, self.password, args)


def GenerateSecret(length=32):
    """Return random data."""
    secret = ""
    for i in range(length):
        secret += chr(random.getrandbits(8))
    return secret


class BaseObject(OFS.Traversable.Traversable, Acquisition.Implicit):
    """Zope 2-style base class for our models.

    This base class allows SQL based objects to act like normal Zope 2
    objects. In particular it allows acquisition to find skin objects
    and keeps absolute_url() and getPhysicalPath() working.
    """

    __init__ = _declarative_constructor
    __allow_access_to_unprotected_subobjects__ = True
    __new__ = object.__new__

    security = ClassSecurityInfo()

    def getId(self):
        return str(self.id)

    @security.public
    def getPhysicalPath(self):
        # Get the physical path of the object.
        #
        # We need to override this because the new Zope implementations
        # uses self.id instead of self.getId, which make a big difference in our case
        id = self.getId()

        path = (id,)
        p = aq_parent(aq_inner(self))
        if p is None:
            return path

        func = self.getPhysicalPath.__func__
        while p is not None:
            if func is p.getPhysicalPath.__func__:
                pid = p.getId()
                path = (pid,) + path
                p = aq_parent(aq_inner(p))
            else:
                if IApplication.providedBy(p):
                    path = ("",) + path
                else:
                    path = p.getPhysicalPath() + path
                break

        return path


class SurveyTreeItem(BaseObject):
    """A tree of questions.

    The data is stored in the form of a materialized tree. The path is
    built using a list of item numbers. Each item number has three
    digits and uses 0-prefixing to make sure we can use simple string
    sorting to produce a sorted tree.
    """

    __tablename__ = "tree"
    __table_args__ = (
        schema.UniqueConstraint("session_id", "path"),
        schema.UniqueConstraint("session_id", "zodb_path", "profile_index"),
        {},
    )

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(
        types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    parent_id = schema.Column(
        types.Integer(),
        schema.ForeignKey("tree.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    type = schema.Column(
        Enum(["risk", "module"]),
        nullable=False,
        index=True,
    )
    path = schema.Column(
        types.String(40),
        nullable=False,
        index=True,
    )
    has_description = schema.Column(
        types.Boolean(),
        default=False,
        index=True,
    )
    zodb_path = schema.Column(
        types.String(512),
        nullable=False,
    )
    profile_index = schema.Column(
        types.Integer(),
        default=0,
        nullable=False,
    )
    depth = schema.Column(
        types.Integer(),
        default=0,
        nullable=False,
        index=True,
    )
    title = schema.Column(types.Unicode(512))
    postponed = schema.Column(types.Boolean())
    skip_children = schema.Column(
        types.Boolean(),
        default=False,
        nullable=False,
    )

    __mapper_args__ = dict(polymorphic_on=type)

    session = orm.relationship(
        "SurveySession",
        cascade="all",
    )
    #    parent = orm.relationship("SurveyTreeItem", uselist=False)

    @property
    def parent(self):
        # XXX Evil! Figure out why the parent relation does not work
        return self.parent_id and Session.query(SurveyTreeItem).get(self.parent_id)

    def getId(self):
        return self.path[-3:].lstrip("0")

    @property
    def short_path(self):
        def slice(path):
            while path:
                yield path[:3].lstrip("0")
                path = path[3:]

        return slice(self.path)

    @property
    def number(self):
        return ".".join(self.short_path)

    def children(self, filter=None):
        query = (
            Session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session_id == self.session_id)
            .filter(SurveyTreeItem.depth == self.depth + 1)
        )
        if self.path:
            query = query.filter(SurveyTreeItem.path.like(self.path + "%"))
        if filter is not None:
            query = query.filter(filter)
        return query.order_by(SurveyTreeItem.path)

    def siblings(self, klass=None, filter=None):
        if not self.path:
            return []
        if klass is None:
            klass = SurveyTreeItem
        query = (
            Session.query(klass)
            .filter(klass.session_id == self.session_id)
            .filter(klass.parent_id == self.parent_id)
        )
        if filter is not None:
            query = query.filter(sql.or_(klass.id == self.id, filter))
        return query.order_by(klass.path)

    def addChild(self, item):
        sqlsession = Session()
        query = (
            sqlsession.query(SurveyTreeItem.path)
            .filter(SurveyTreeItem.session_id == self.session_id)
            .filter(SurveyTreeItem.depth == self.depth + 1)
        )
        if self.path:
            query = query.filter(SurveyTreeItem.path.like(self.path + "%"))

        last = query.order_by(SurveyTreeItem.path.desc()).first()
        if not last:
            index = 1
        else:
            index = int(last[0][-3:]) + 1

        item.session = self.session
        item.depth = self.depth + 1
        item.path = (self.path or "") + "%03d" % index
        item.parent_id = self.id
        if self.profile_index != -1:
            item.profile_index = self.profile_index
        sqlsession.add(item)
        self.session.touch()
        return item

    def removeChildren(self, excluded=[]):
        if self.id not in excluded:
            excluded.append(self.id)
        session = Session()
        if self.path:
            filter = sql.and_(
                SurveyTreeItem.session_id == self.session_id,
                SurveyTreeItem.path.like(self.path + "%"),
                sql.not_(SurveyTreeItem.id.in_(excluded)),
            )
        else:
            filter = sql.and_(
                SurveyTreeItem.session_id == self.session_id,
                sql.not_(SurveyTreeItem.id.in_(excluded)),
            )
        removed = session.query(SurveyTreeItem).filter(filter).all()
        session.execute(SurveyTreeItem.__table__.delete().where(filter))
        self.session.touch()
        datamanager.mark_changed(session)
        return removed


class Group(BaseObject):
    __tablename__ = "group"

    group_id = schema.Column(
        types.Unicode(32),
        primary_key=True,
    )
    parent_id = schema.Column(
        types.Unicode(32),
        schema.ForeignKey("group.group_id"),
    )
    short_name = schema.Column(
        types.Unicode(32),
    )
    long_name = schema.Column(
        types.Unicode(256),
    )
    responsible_id = schema.Column(
        types.Unicode(32),
    )
    responsible_fullname = schema.Column(
        types.Unicode(32),
    )

    deactivated = schema.Column(
        types.DateTime,
        nullable=True,
        default=None,
    )

    parent = orm.relationship(
        "Group",
        back_populates="children",
        remote_side=[group_id],
    )

    children = orm.relationship(
        "Group",
        back_populates="parent",
        remote_side=[parent_id],
    )

    accounts = orm.relationship(
        "Account",
        back_populates="group",
    )

    brand = schema.Column(types.String(64))

    sessions = orm.relationship(
        "SurveySession",
        back_populates="group",
        order_by="SurveySession.modified",
        cascade="all, delete-orphan",
    )

    # Allow this class to be subclassed in other projects
    __mapper_args__ = {
        "polymorphic_identity": "euphorie",
        "polymorphic_on": brand,
        "with_polymorphic": "*",
    }

    @property
    def fullname(self):
        """This is the name that will be display in the selectors and in the
        tree widget."""
        title = "{obs}{name}".format(
            obs="[obs.] " if not self.deactivated else "",
            name=self.short_name or self.group_id,
        )
        if self.responsible_fullname:
            title += f", {self.responsible_fullname}"
        return title

    @property
    def descendantids(self):
        """Return all the groups in the hierarchy flattened."""
        structure = self._group_structure
        ids = []

        def get_ids(groupid):
            new_ids = structure[groupid]
            if not new_ids:
                return
            ids.extend(new_ids)
            tuple(map(get_ids, new_ids))

        get_ids(self.group_id)
        return ids

    @property
    def descendants(self):
        """Return all the groups in the hierarchy flattened."""
        return list(
            Session.query(self.__class__).filter(
                self.__class__.group_id.in_(self.descendantids)
            )
        )

    @property
    def parents(self):
        """Return all the groups in the hierarchy flattened."""
        group = self
        parents = []
        while True:
            parent = group.parent
            if not parent:
                return parents
            parents.append(parent)
            group = parent

    @property
    @memoize
    def _group_structure(self):
        """Return a dict like structure with the group ids as keys and the
        children group ids as values."""
        tree = defaultdict(set)
        for groupid, parentid in Session.query(Group.group_id, Group.parent_id).filter(
            Group.parent_id != None  # noqa: E711
        ):
            tree[parentid].add(groupid)
        return tree

    @property
    def acquired_sessions(self):
        """All the session relative to this group and its children."""
        group_ids = [self.group_id]
        group_ids.extend(g.group_id for g in self.descendants)
        return (
            Session.query(SurveySession)
            .filter(SurveySession.group_id.in_(group_ids))
            .all()
        )


class Consultancy(BaseObject):
    """Information about consultancy on a session."""

    __tablename__ = "consultancy"

    session_id = schema.Column(
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    account_id = schema.Column(
        schema.ForeignKey("account.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    session = orm.relationship(
        "SurveySession",
        uselist=False,
        back_populates="consultancy",
    )
    account = orm.relationship(
        "Account",
        uselist=False,
        back_populates="consultancy",
    )

    status = schema.Column(
        types.Unicode(255),
        default="pending",
    )


@implementer(IUser)
class Account(BaseObject):
    """A user account.

    Users have to register with euphorie before they can start a survey
    session. A single account can have multiple survey sessions.
    """

    __tablename__ = "account"

    id = schema.Column(
        types.Integer(),
        primary_key=True,
        autoincrement=True,
    )
    loginname = schema.Column(
        types.String(255),
        nullable=False,
        index=True,
        unique=True,
    )
    password = schema.Column(types.Unicode(64))
    tc_approved = schema.Column(types.Integer())
    account_type = schema.Column(
        Enum(["guest", "converted", "full"]),
        default="full",
        nullable=True,
    )
    group_id = schema.Column(
        types.Unicode(32),
        schema.ForeignKey("group.group_id"),
    )

    created = schema.Column(
        types.DateTime,
        nullable=True,
        default=functions.now(),
    )

    last_login = schema.Column(
        types.DateTime,
        nullable=True,
        default=None,
    )

    first_name = schema.Column(
        types.Unicode(),
        nullable=True,
        default=None,
    )
    last_name = schema.Column(
        types.Unicode(),
        nullable=True,
        default=None,
    )
    consultancy = orm.relationship(
        "Consultancy",
        uselist=False,
        back_populates="account",
    )

    group = orm.relationship(
        Group,
        back_populates="accounts",
    )

    @property
    def groups(self):
        group = self.group
        if not group:
            return []
        groups = [group]
        groups.extend(group.descendants)
        return groups

    @property
    def acquired_sessions(self):
        """The session the account acquires because he belongs to a group."""
        group = self.group
        if not group:
            return []
        return list(group.acquired_sessions)

    @property
    def group_sessions(self):
        """The session the account acquires because he belongs to a group."""
        group = self.group
        if not group:
            return []
        return list(group.sessions)

    @property
    def email(self):
        """Email addresses are used for login, return the login."""
        return self.loginname

    @property
    def login(self):
        """This synchs naming with :obj:`euphorie.content.user.IUser` and is
        needed by the authentication tools."""
        return self.loginname

    @property
    def title(self):
        """Return the joined first_name and last_name of the account if
        present.

        If they are not fallback to the loginname
        """
        return (
            " ".join((self.first_name or "", self.last_name or "")).strip()
            or self.loginname
        )

    def getUserName(self):
        """Return the login name."""
        return self.loginname

    def getGroups(self):
        return ["AuthenticatedUsers"]

    def getRoles(self):
        """Return all global roles for this user."""

        return ("EuphorieUser",)

    def getRolesInContext(self, object):
        """Return the roles of the user in the current context (same as
        :obj:`getRoles`).
        """
        return self.getRoles()

    def getDomains(self):
        return []

    def addPropertysheet(self, propfinder_id, data):
        pass

    def _addGroups(self, group_ids):
        pass

    def _addRoles(self, role_ids):
        pass

    def has_permission(self, perm, context):
        """Check if the user has a permission in a context."""
        return perm == "Euphorie: View a Survey"

    def allowed(self, context, object_roles=None):
        """Check if this account has any of the requested roles in the context
        of `object`."""
        if object_roles is _what_not_even_god_should_do:
            return False

        if object_roles is None:
            return True

        for obj in aq_chain(aq_inner(context)):
            if IClient.providedBy(obj):
                allowed_roles = {"Anonymous", "Authenticated", "EuphorieUser", "Reader"}
                return bool(allowed_roles & set(object_roles))

        return False

    @ram.cache(_forever_cache_key)
    def verify_password(self, password):
        """Verify the given password against the one stored in the account
        table."""
        if not password:
            return False
        if not isinstance(password, str):
            return False
        if password == self.password:
            return True
        password = safe_text(password)
        return bcrypt.checkpw(password, self.password)

    def hash_password(self):
        """Hash the account password using bcrypt."""
        try:
            password = self.password
        except AttributeError:
            return
        if not password:
            return
        password = safe_text(password)
        if BCRYPTED_PATTERN.match(password):
            # The password is already encrypted, do not encrypt it again
            # XXX this is broken with passwords that are actually an hash
            return
        self.password = safe_text(
            bcrypt.hashpw(
                password,
                bcrypt.gensalt(),
            )
        )


def account_before_insert_subscriber(mapper, connection, account):
    account.hash_password()


account_before_update_subscriber = account_before_insert_subscriber

listen(Account, "before_insert", account_before_insert_subscriber)
listen(Account, "before_update", account_before_update_subscriber)


class AccountChangeRequest(BaseObject):
    __tablename__ = "account_change"

    id = schema.Column(types.String(16), primary_key=True, nullable=False)
    account_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    account = orm.relationship(
        Account,
        back_populates="change_request",
    )
    value = schema.Column(
        types.String(255),
        nullable=False,
    )
    expires = schema.Column(
        types.DateTime(),
        nullable=False,
    )


Account.change_request = orm.relationship(
    AccountChangeRequest,
    back_populates="account",
    cascade="all, delete-orphan",
    uselist=False,
)


class ISurveySession(Interface):
    """Marker interface for a SurveySession object."""


@implementer(ISurveySession)
class SurveySession(BaseObject):
    """Information about a user's session."""

    __tablename__ = "session"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    brand = schema.Column(types.String(64))
    account_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    last_modifier_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=False,
    )
    last_publisher_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=False,
    )
    group_id = schema.Column(
        types.Unicode(32),
        schema.ForeignKey("group.group_id"),
    )
    title = schema.Column(types.Unicode(512))
    created = schema.Column(
        types.DateTime,
        nullable=False,
        default=functions.now(),
    )
    modified = schema.Column(
        types.DateTime,
        nullable=False,
        default=functions.now(),
    )
    refreshed = schema.Column(
        types.DateTime,
        nullable=False,
        default=functions.now(),
    )

    published = schema.Column(
        types.DateTime,
        nullable=True,
        default=None,
    )

    archived = schema.Column(
        types.DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    zodb_path = schema.Column(types.String(512), nullable=False)

    report_comment = schema.Column(types.UnicodeText())

    account = orm.relationship(
        Account,
        back_populates="sessions",
        foreign_keys=[account_id],
    )
    last_modifier = orm.relationship(
        Account,
        foreign_keys=[last_modifier_id],
    )
    last_publisher = orm.relationship(
        Account,
        foreign_keys=[last_publisher_id],
    )

    group = orm.relationship(
        Group,
        back_populates="sessions",
    )

    consultancy = orm.relationship(
        "Consultancy",
        uselist=False,
        back_populates="session",
    )

    migrated = schema.Column(
        types.DateTime,
        nullable=False,
        default=functions.now(),
    )

    # Allow this class to be subclassed in other projects
    __mapper_args__ = {
        "polymorphic_identity": "euphorie",
        "polymorphic_on": brand,
        "with_polymorphic": "*",
    }

    @property
    def is_archived(self):
        archived = self.archived
        if not archived:
            return False
        return archived <= localized_now()

    @property
    def last_locking_event(self):
        """Return the last event relative to locking"""
        query = (
            Session.query(SessionEvent)
            .filter(
                SessionEvent.action.in_(LOCKING_ACTIONS),
                SessionEvent.session_id == self.id,
            )
            .order_by(SessionEvent.time.desc())
        )
        return query.first()

    @property
    def last_validation_event(self):
        """Return the last event relative to validation"""
        query = (
            Session.query(SessionEvent)
            .filter(
                SessionEvent.action.in_(
                    (
                        "validation_requested",
                        "validated",
                        "invalidated",
                    )
                ),
                SessionEvent.session_id == self.id,
            )
            .order_by(SessionEvent.time.desc())
        )
        return query.first()

    @property
    def is_validated(self):
        """Check if the session is validated."""
        event = self.last_validation_event
        if not event:
            return False
        return event.action == "validated"

    @property
    def is_locked(self):
        """Check if the session is locked."""
        if self.is_validated:
            return True

        event = self.last_locking_event
        if not event:
            return False
        return event.action in LOCKING_SET_ACTIONS

    @property
    @deprecate(
        "Deprecated in version 15.0.0.dev0. "
        "You might want to use self.is_locked instead."
    )
    def review_state(self):
        """Check if it the published column.

        If it has return 'published' otherwise return 'private'
        """
        return "published" if self.is_locked else "private"

    def hasTree(self):
        return bool(
            Session.query(SurveyTreeItem).filter(SurveyTreeItem.session == self).count()
        )

    def reset(self):
        Session.query(SurveyTreeItem).filter(SurveyTreeItem.session == self).delete()
        self.created = self.modified = datetime.datetime.now()

    def touch(self):
        self.last_modifier = get_current_account()
        self.modified = datetime.datetime.now()

    def refresh_survey(self, survey=None):
        """Mark the session with the current date to indicate that is has been
        refreshed with the latest version of the Survey (from Zope).

        If survey is passed, update all titles in the tree, based on the
        CMS version of the survey, i.e. update all titles of modules and
        risks. Those are used in the navigation. If a title change is
        the only change in the CMS, the survey session is not re-
        created. Therefore this method ensures that the titles are
        updated where necessary.
        """
        if survey:
            query = Session.query(SurveyTreeItem).filter(
                SurveyTreeItem.session_id == self.id
            )
            tree = query.all()
            for item in tree:
                if item.zodb_path.find("custom-risks") >= 0:
                    continue
                zodb_item = survey.restrictedTraverse(item.zodb_path.split("/"), None)
                # Don't update session-specific instances of profilequestions
                if (
                    zodb_item.portal_type == "euphorie.profilequestion"
                    and item.profile_index > -1
                ):
                    continue
                if zodb_item and zodb_item.title != item.title:
                    item.title = zodb_item.title
        self.refreshed = datetime.datetime.now()

    def update_measure_types(self, survey):
        """Update measure types in the session according to changes in the
        tool.

        Specifically, if an `in_place_standard` measure is deleted in
        the tool, it disappears from the identification phase of the
        session unless we change its type to `in_place_custom`.
        """
        in_place_standard_measures = (
            Session.query(Risk, ActionPlan)
            .filter(Risk.id == ActionPlan.risk_id)
            .filter(Risk.session_id == self.id)
            .filter(ActionPlan.plan_type == "in_place_standard")
            .all()
        )
        for risk, measure in in_place_standard_measures:
            risk_zodb = survey.restrictedTraverse(risk.zodb_path.split("/"))
            solution_ids_zodb = [sol.id for sol in risk_zodb._solutions]
            if measure.solution_id not in solution_ids_zodb:
                # The measure is in the session but not in the tool. It has probably
                # been deleted. Keep it visible by making it a custom measure.
                measure.plan_type = "in_place_custom"

    def addChild(self, item):
        sqlsession = Session()
        query = (
            sqlsession.query(SurveyTreeItem.path)
            .filter(SurveyTreeItem.session_id == self.id)
            .filter(SurveyTreeItem.depth == 1)
            .order_by(SurveyTreeItem.path.desc())
        )
        last = query.first()
        if not last:
            index = 1
        else:
            index = int(last[0][-3:]) + 1

        item.session = self
        item.depth = 1
        item.path = "%03d" % index
        item.parent_id = None
        sqlsession.add(item)
        self.touch()
        return item

    def children(self, filter=None):
        query = (
            Session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session_id == self.id)
            .filter(SurveyTreeItem.depth == 1)
        )
        if filter is not None:
            query = query.filter(filter)
        return query.order_by(SurveyTreeItem.path)

    def copySessionData(self, other):
        """Copy all user data from another session to this one."""
        session = Session()

        # Copy all tree data to the new session (skip_children and postponed)
        old_tree = orm.aliased(SurveyTreeItem, name="old_tree")
        in_old_tree = sql.and_(
            old_tree.session_id == other.id,
            SurveyTreeItem.zodb_path == old_tree.zodb_path,
            SurveyTreeItem.profile_index == old_tree.profile_index,
        )
        skip_children = sql.select([old_tree.skip_children], in_old_tree).limit(1)
        postponed = sql.select([old_tree.postponed], in_old_tree).limit(1)
        new_items = (
            session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session == self)
            .filter(sql.exists(sql.select([old_tree.id]).where(in_old_tree)))
        )
        new_items.update(
            {"skip_children": skip_children, "postponed": postponed},
            synchronize_session=False,
        )

        # Mandatory modules must have skip_children=False. It's possible that
        # the module was optional with skip_children=True and now after the
        # update it's mandatory. So we must check and correct.
        # In case a risk was marked as "always present", be sure its
        # identification gets set to 'no'
        preset_to_no = []
        survey = getSite()["client"].restrictedTraverse(self.zodb_path)
        for item in new_items.all():
            if item.type == "risk":
                if item.identification == "no":
                    preset_to_no.append(item.risk_id)

            elif item.type == "module":
                module = survey.restrictedTraverse(item.zodb_path.split("/"))
                if not module.optional:
                    item.skip_children = False

        # Copy all risk data to the new session
        # This triggers a "Only update via a single table query is currently
        # supported" error with SQLAlchemy 0.6.6
        # old_risk = orm.aliased(Risk.__table__, name='old_risk')
        # is_old_risk = sql.and_(in_old_tree, old_tree.id == old_risk.id)
        # identification = sql.select([old_risk.identification], is_old_risk)
        # new_risks = session.query(Risk)\
        #         .filter(Risk.session == self)\
        #         .filter(sql.exists(
        #             sql.select([SurveyTreeItem.id]).where(sql.and_(
        #                     SurveyTreeItem.id == Risk.id,
        #                     sql.exists([old_tree.id]).where(sql.and_(
        #                         in_old_tree, old_tree.type == 'risk'))))))
        # new_risks.update({'identification': identification},
        #         synchronize_session=False)

        skip_preset_to_no_clause = ""
        if len(preset_to_no):
            skip_preset_to_no_clause = "old_risk.risk_id not in %s AND" % (
                str([str(x) for x in preset_to_no]).replace("[", "(").replace("]", ")")
            )
        statement = """\
        UPDATE RISK
        SET identification = old_risk.identification,
            frequency = old_risk.frequency,
            effect = old_risk.effect,
            probability = old_risk.probability,
            priority = old_risk.priority,
            existing_measures = old_risk.existing_measures,
            comment = old_risk.comment,
            scaled_answer = old_risk.scaled_answer
        FROM risk AS old_risk JOIN tree AS old_tree ON old_tree.id=old_risk.id, tree
        WHERE tree.id=risk.id AND
              %(skip_preset_to_no_clause)s
              tree.session_id=%(new_sessionid)s AND
              old_tree.session_id=%(old_sessionid)s AND
              old_tree.zodb_path=tree.zodb_path AND
              old_tree.profile_index=tree.profile_index;
        """ % dict(  # noqa: E501
            old_sessionid=other.id,
            new_sessionid=self.id,
            skip_preset_to_no_clause=skip_preset_to_no_clause,
        )
        session.execute(statement)

        statement = """\
        INSERT INTO action_plan (risk_id, action_plan, prevention_plan, action,
                                        requirements, responsible, budget, plan_type,
                                        planning_start, planning_end,
                                        solution_id, used_in_training)
               SELECT new_tree.id,
                      action_plan.action_plan,
                      action_plan.prevention_plan,
                      action_plan.action,
                      action_plan.requirements,
                      action_plan.responsible,
                      action_plan.budget,
                      action_plan.plan_type,
                      action_plan.planning_start,
                      action_plan.planning_end,
                      action_plan.solution_id,
                      action_plan.used_in_training
               FROM action_plan JOIN risk ON action_plan.risk_id=risk.id
                                JOIN tree ON tree.id=risk.id,
                    tree AS new_tree
               WHERE tree.session_id=%(old_sessionid)d AND
                     new_tree.session_id=%(new_sessionid)d AND
                     tree.zodb_path=new_tree.zodb_path AND
                     tree.profile_index=new_tree.profile_index;
            """ % {
            "old_sessionid": other.id,
            "new_sessionid": self.id,
        }
        session.execute(statement)

        # Copy over previous session metadata. Specifically, we don't want to
        # create a new modification timestamp, just because the underlying
        # survey was updated.
        statement = """\
        UPDATE session
        SET
            modified = old_session.modified,
            created = old_session.created,
            last_modifier_id = old_session.last_modifier_id
        FROM session as old_session
        WHERE
            old_session.id=%(old_sessionid)d AND
            session.id=%(new_sessionid)d
        """ % {
            "old_sessionid": other.id,
            "new_sessionid": self.id,
        }
        session.execute(statement)

        session.query(Company).filter(Company.session == other).update(
            {"session_id": self.id}, synchronize_session=False
        )

    @classmethod
    def get_account_filter(cls, account=None):
        """Filter only the sessions for the given account.

        :param acount: True means current account.
            A falsish value means do not filter.
            Otherwise try to interpret the user input:
            a string or an int means the account_id should be that value,
            an object account will be used to extract the account id,
            from an iterable we will try to extract the account ids
        """
        # TODO: this is too complex
        include_organisation_members = False
        if account is True:
            include_organisation_members = True
            account = get_current_account()

        if isinstance(account, Account):
            account = account.id

        if not account:
            return False

        if not include_organisation_members and isinstance(account, (int, (str,))):
            return cls.account_id == account

        if include_organisation_members:
            account_ids = {account}
            # Add the owner id of the organisations where the account is member of
            owner_memberships = Session.query(OrganisationMembership.owner_id).filter(
                OrganisationMembership.member_id == account
            )
            account_ids.update(membership.owner_id for membership in owner_memberships)
        else:
            try:
                # This works when we pass an iterable of accounts or ids
                account_ids = {getattr(item, "id", item) for item in account}
            except TypeError:
                # this happens when account is not an iterable
                log.error("Cannot understand the account parameter: %r", account)
                raise
            account_ids = {
                item for item in account_ids if item and isinstance(item, (int, (str,)))
            }

        if not account_ids:
            return False

        if len(account_ids) == 1:
            for account_id in account_ids:
                return cls.get_account_filter(account_id)

        return cls.account_id.in_(account_ids)

    @classmethod
    def get_group_filter(cls, group=None):
        """Filter only the sessions for the given group.

        :param group: True means the current account's group.
            A falsish value means do not filter.
            Otherwise try to interpret the user input:
            a string or an int means the group_id should be that value,
            an object group will be used to extract the group id,
            and from an iterable we will try to extract the group ids
        """
        if group is True:
            group = getattr(get_current_account(), "group_id", None)

        if isinstance(group, Group):
            group = group.group_id

        if not group:
            return False

        if isinstance(group, (int, (str,))):
            return cls.group_id == group

        try:
            group_ids = {getattr(item, "group_id", item) for item in group}
        except TypeError:
            log.error("Cannot understand the group parameter: %r", group)
            raise

        group_ids = {
            item for item in group_ids if item and isinstance(item, (int, (str,)))
        }
        if not group_ids:
            return False

        if len(group_ids) == 1:
            for group_id in group_ids:
                return cls.get_group_filter(group_id)

        return cls.group_id.in_(group_ids)

    @classmethod
    def get_archived_filter(cls):
        """Filter out sessions that are archived."""
        return sql.or_(
            cls.archived >= localized_now(), cls.archived == None  # noqa: E711
        )

    @classmethod
    def _get_context_tools(cls, context):
        """Return the set of tools we can find under this context."""
        if not context:
            return set()

        # Check the path relative to the client folder
        if context.portal_type == "Plone Site":
            context = context.client

        if context.portal_type == "euphorie.survey":
            return {context}

        portal_type_filter = {
            "portal_type": [
                "euphorie.clientcountry",
                "euphorie.clientsector",
                "euphorie.survey",
            ]
        }

        surveys = set()

        def _add_survey(container):
            for obj in container.listFolderContents(portal_type_filter):
                if obj.portal_type == "euphorie.survey":
                    surveys.add(obj)
                else:
                    _add_survey(obj)

        _add_survey(context)
        return surveys

    @classmethod
    def get_context_filter(cls, context):
        """Filter sessions under this context using the zodb_path column."""
        surveys = cls._get_context_tools(context)
        if not surveys:
            return False

        return cls.zodb_path.in_(
            {safe_text("/".join(survey.getPhysicalPath()[-3:])) for survey in surveys}
        )

    @property
    def tool(self):
        client = api.portal.get().client
        return client.restrictedTraverse(str(self.zodb_path), None)

    @property
    def traversed_session(self):
        return self.tool.restrictedTraverse("++session++%s" % self.id)

    def absolute_url(self):
        """The URL for this session is based on the tool's URL.

        To it (if it can be fetched) we add a traverser with the session
        id.
        """
        client = api.portal.get().client
        tool = client.unrestrictedTraverse(self.zodb_path, None)
        if tool is None:
            raise ValueError("No tool found for session %s" % self.id)
        return f"{tool.absolute_url()}/++session++{self.id}"

    @property
    def country(self):
        return str(self.zodb_path).split("/")[0]

    @property
    def completion_percentage(self):
        module_query = (
            Session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session_id == self.id)
            .filter(SurveyTreeItem.type == "module")
        ).order_by(SurveyTreeItem.path)

        good_module_ids = set()
        bad_module_ids = set()
        for module in module_query:
            if module.parent_id in bad_module_ids or module.skip_children:
                bad_module_ids.add(module.id)
            else:
                good_module_ids.add(module.id)

        if not good_module_ids:
            return 0

        total_risks_query = Session.query(Risk).filter(
            Risk.parent_id.in_(good_module_ids)
        )
        total = total_risks_query.count()

        if not total:
            return 0

        answered = float(
            total_risks_query.filter(Risk.identification != None).count()  # noqa: E711
        )

        completion_percentage = int(round(answered / total * 100.0))
        return completion_percentage


Account.sessions = orm.relationship(
    SurveySession,
    back_populates="account",
    foreign_keys=[SurveySession.account_id],
    cascade="all, delete-orphan",
)


class SessionEvent(BaseObject):
    """Data table to record events happening on sessions."""

    __tablename__ = "session_event"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    time = schema.Column(types.DateTime(), nullable=False, default=func.now())
    account_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE"),
        nullable=True,
    )
    account = orm.relationship(Account)
    session_id = schema.Column(
        types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    session = orm.relationship(SurveySession, back_populates="events")
    action = schema.Column(types.Unicode(32))
    note = schema.Column(types.Unicode)


Account.session_events = orm.relationship(SessionEvent, back_populates="account")


SurveySession.events = orm.relationship(
    SessionEvent, back_populates="session", cascade="all,delete-orphan"
)


class SessionRedirect(BaseObject):
    """Mapping of old deleted sessions to their new rebuilt counterparts"""

    __tablename__ = "session_redirect"

    old_session_id = schema.Column(types.Integer(), primary_key=True, nullable=False)
    new_session_id = schema.Column(types.Integer(), nullable=False)


class Company(BaseObject):
    """Information about a company."""

    __tablename__ = "company"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(
        types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session = orm.relationship(SurveySession, back_populates="company")

    country = schema.Column(types.String(3))
    employees = schema.Column(Enum([None, "1-9", "10-49", "50-249", "250+"]))
    conductor = schema.Column(Enum([None, "staff", "third-party", "both"]))
    referer = schema.Column(
        Enum(
            [
                None,
                "employers-organisation",
                "trade-union",
                "national-public-institution",
                "eu-institution",
                "health-safety-experts",
                "other",
            ]
        )
    )
    workers_participated = schema.Column(types.Boolean())
    needs_met = schema.Column(types.Boolean())
    recommend_tool = schema.Column(types.Boolean())
    timestamp = schema.Column(types.DateTime(), nullable=True)


SurveySession.company = orm.relationship(
    Company, back_populates="session", cascade="all,delete-orphan", uselist=False
)


class Module(SurveyTreeItem):
    """A module.

    This is a dummy object needed to be able to put modules in the
    survey tree.
    """

    __tablename__ = "module"
    __mapper_args__ = dict(polymorphic_identity="module")

    sql_module_id = schema.Column(
        "id",
        types.Integer(),
        schema.ForeignKey(SurveyTreeItem.id, onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    module_id = schema.Column(types.String(16), nullable=False)
    solution_direction = schema.Column(types.Boolean(), default=False)


class Risk(SurveyTreeItem):
    """Answer to risk."""

    __tablename__ = "risk"
    __mapper_args__ = dict(polymorphic_identity="risk")

    sql_risk_id = schema.Column(
        "id",
        types.Integer(),
        schema.ForeignKey(SurveyTreeItem.id, onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    risk_id = schema.Column(types.String(16), nullable=True)
    risk_type = schema.Column(
        Enum(["risk", "policy", "top5"]), default="risk", nullable=False, index=True
    )
    #: Skip-evaluation flag. This is only used to indicate if the sector
    #: set the evaluation method to `fixed`, not for policy behaviour
    #: such as not evaluation top-5 risks. That policy behaviour is
    #: handled via the question_filter on client views so it can be modified
    #: in custom deployments.
    skip_evaluation = schema.Column(types.Boolean(), default=False, nullable=False)
    is_custom_risk = schema.Column(types.Boolean(), default=False, nullable=False)
    identification = schema.Column(Enum([None, "yes", "no", "n/a"]))
    frequency = schema.Column(types.Integer())
    effect = schema.Column(types.Integer())
    probability = schema.Column(types.Integer())
    priority = schema.Column(Enum([None, "low", "medium", "high"]))
    comment = schema.Column(types.UnicodeText())
    existing_measures = schema.Column(types.UnicodeText())
    training_notes = schema.Column(types.UnicodeText())
    custom_description = schema.Column(types.UnicodeText())
    image_data = schema.Column(types.LargeBinary())
    image_data_scaled = schema.Column(types.LargeBinary())
    image_filename = schema.Column(types.UnicodeText())
    scaled_answer = schema.Column(types.UnicodeText())

    @memoize
    def measures_of_type(self, plan_type):
        query = (
            Session.query(ActionPlan)
            .filter(
                sql.and_(ActionPlan.risk_id == self.id),
                ActionPlan.plan_type == plan_type,
            )
            .order_by(ActionPlan.id)
        )
        return query.all()

    @property
    def standard_measures(self):
        return self.measures_of_type("measure_standard")

    @property
    def custom_measures(self):
        return self.measures_of_type("measure_custom")

    @property
    def in_place_standard_measures(self):
        return self.measures_of_type("in_place_standard")

    @property
    def in_place_custom_measures(self):
        return self.measures_of_type("in_place_custom")


class ActionPlan(BaseObject):
    """Action plans for a known risk."""

    __tablename__ = "action_plan"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    risk_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Risk.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    action_plan = schema.Column(types.UnicodeText())
    prevention_plan = schema.Column(types.UnicodeText())
    # The column "action" is the synthesis of "action_plan" and "prevention_plan"
    action = schema.Column(types.UnicodeText())
    requirements = schema.Column(types.UnicodeText())
    responsible = schema.Column(types.Unicode(256))
    budget = schema.Column(types.Integer())
    planning_start = schema.Column(types.Date())
    planning_end = schema.Column(types.Date())
    reference = schema.Column(types.Text())
    plan_type = schema.Column(
        Enum(
            [
                "measure_custom",
                "measure_standard",
                "in_place_standard",
                "in_place_custom",
            ]
        ),
        nullable=False,
        index=True,
        default="measure_custom",
    )
    solution_id = schema.Column(types.Unicode(20))
    used_in_training = schema.Column(
        types.Boolean(),
        default=True,
        index=True,
    )

    risk = orm.relationship(Risk, back_populates="action_plans")


Risk.action_plans = orm.relationship(
    ActionPlan, back_populates="risk", cascade="all, delete-orphan"
)


class Training(BaseObject):
    """Data table to record trainings."""

    __tablename__ = "training"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    time = schema.Column(types.DateTime(), nullable=True, default=func.now())
    account_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    account = orm.relationship(Account, back_populates="trainings")
    session_id = schema.Column(
        types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    session = orm.relationship(
        "SurveySession",
        back_populates="trainings",
    )
    answers = schema.Column(types.Unicode, default="[]")
    status = schema.Column(types.Unicode)


Account.trainings = orm.relationship(
    Training, back_populates="account", cascade="all, delete-orphan"
)


SurveySession.trainings = orm.relationship(
    Training, back_populates="session", cascade="all, delete-orphan"
)


class Organisation(BaseObject):
    """A table to store some data about an organisation."""

    __tablename__ = "organisation"

    organisation_id = schema.Column(
        types.Integer(),
        primary_key=True,
        autoincrement=True,
    )
    owner_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    title = schema.Column(types.UnicodeText())
    image_data = schema.Column(types.LargeBinary())
    image_data_scaled = schema.Column(types.LargeBinary())
    image_filename = schema.Column(types.UnicodeText())
    owner = orm.relationship(Account, back_populates="organisation")


Account.organisation = orm.relationship(
    Organisation, back_populates="owner", cascade="all, delete-orphan", uselist=False
)


class OrganisationMembership(BaseObject):
    """This table wants to mimic the concept of an organisation for Euphorie.

    The goal is to share permissions to work on sessions from another
    user.
    """

    __tablename__ = "organisation_membership"

    organisation_id = schema.Column(
        types.Integer(),
        primary_key=True,
        autoincrement=True,
    )
    owner_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    member_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    member_role = schema.Column(types.UnicodeText())


class NotificationSubscription(BaseObject):
    __tablename__ = "notification_subscription"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    account_id = schema.Column(
        types.Integer(),
        schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    category = schema.Column(types.String(512), nullable=False)
    enabled = schema.Column(types.Boolean(), nullable=False, default=False)


_instrumented = False
if not _instrumented:
    metadata._decl_registry = {}
    for cls in [
        Consultancy,
        SurveyTreeItem,
        SurveySession,
        SessionEvent,
        SessionRedirect,
        Module,
        Risk,
        ActionPlan,
        Group,
        Account,
        AccountChangeRequest,
        Company,
        Training,
        Organisation,
        OrganisationMembership,
        NotificationSubscription,
    ]:
        instrument_declarative(cls, metadata._decl_registry, metadata)
    orm.configure_mappers()
    _instrumented = True

schema.Index("tree_session_path", SurveyTreeItem.session_id, SurveyTreeItem.path)
schema.Index(
    "tree_zodb_path",
    SurveyTreeItem.session_id,
    SurveyTreeItem.profile_index,
    SurveyTreeItem.zodb_path,
)


def _SKIPPED_PARENTS_factory():
    # XXX This can be optimized by doing short-circuit on parent.type!=module
    parent = orm.aliased(SurveyTreeItem)
    return sql.exists().where(
        sql.and_(
            parent.session_id == SurveyTreeItem.session_id,
            SurveyTreeItem.depth > parent.depth,
            SurveyTreeItem.path.like(parent.path + "%"),
            parent.skip_children == True,  # noqa: E712
        )
    )


SKIPPED_PARENTS = _SKIPPED_PARENTS_factory()


NO_CUSTOM_RISKS_FILTER = sql.not_(
    sql.and_(
        SurveyTreeItem.type == "risk",
        sql.exists(
            sql.select([Risk.sql_risk_id]).where(
                sql.and_(
                    Risk.sql_risk_id == SurveyTreeItem.id,
                    Risk.is_custom_risk == True,  # noqa: E712
                )
            )
        ),
    )
)

RISK_OR_MODULE_WITH_DESCRIPTION_FILTER = sql.or_(
    SurveyTreeItem.type != "module", SurveyTreeItem.has_description
)


# Used by tno.euphorie
def _MODULE_WITH_RISK_FILTER_factory():
    child_node = orm.aliased(SurveyTreeItem)
    return sql.and_(
        SurveyTreeItem.type == "module",
        SurveyTreeItem.skip_children == False,  # noqa: E712
        sql.exists(
            sql.select([child_node.id]).where(
                sql.and_(
                    child_node.session_id == SurveyTreeItem.session_id,
                    child_node.id == Risk.sql_risk_id,
                    child_node.type == "risk",
                    Risk.identification == "no",
                    child_node.depth > SurveyTreeItem.depth,
                    child_node.path.like(SurveyTreeItem.path + "%"),
                )
            )
        ),
    )


MODULE_WITH_RISK_FILTER = _MODULE_WITH_RISK_FILTER_factory()


def _MODULE_WITH_RISK_OR_TOP5_FILTER_factory():
    child_node = orm.aliased(SurveyTreeItem)
    return sql.and_(
        SurveyTreeItem.type == "module",
        SurveyTreeItem.skip_children == False,  # noqa: E712
        sql.exists(
            sql.select([child_node.id]).where(
                sql.and_(
                    child_node.session_id == SurveyTreeItem.session_id,
                    child_node.id == Risk.sql_risk_id,
                    child_node.type == "risk",
                    sql.or_(Risk.identification == "no", Risk.risk_type == "top5"),
                    child_node.depth > SurveyTreeItem.depth,
                    child_node.path.like(SurveyTreeItem.path + "%"),
                )
            )
        ),
    )


MODULE_WITH_RISK_OR_TOP5_FILTER = _MODULE_WITH_RISK_OR_TOP5_FILTER_factory()


def _MODULE_WITH_RISK_TOP5_TNO_FILTER_factory():
    child_node = orm.aliased(SurveyTreeItem)
    return sql.and_(
        SurveyTreeItem.type == "module",
        SurveyTreeItem.skip_children == False,  # noqa: E712
        sql.exists(
            sql.select([child_node.id]).where(
                sql.and_(
                    child_node.session_id == SurveyTreeItem.session_id,
                    child_node.id == Risk.sql_risk_id,
                    child_node.type == "risk",
                    sql.or_(
                        Risk.identification == "no",
                        sql.and_(
                            Risk.risk_type == "top5",
                            sql.or_(
                                sql.not_(Risk.identification.in_(["n/a", "yes"])),
                                Risk.identification is None,
                            ),
                        ),
                    ),
                    child_node.depth > SurveyTreeItem.depth,
                    child_node.path.like(SurveyTreeItem.path + "%"),
                )
            )
        ),
    )


# Used by tno.euphorie
MODULE_WITH_RISK_TOP5_TNO_FILTER = _MODULE_WITH_RISK_TOP5_TNO_FILTER_factory()


def _MODULE_WITH_RISK_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER_factory():
    child_node = orm.aliased(SurveyTreeItem)
    return sql.and_(
        SurveyTreeItem.type == "module",
        SurveyTreeItem.skip_children == False,  # noqa: E712
        sql.exists(
            sql.select([child_node.id]).where(
                sql.and_(
                    child_node.session_id == SurveyTreeItem.session_id,
                    child_node.id == Risk.sql_risk_id,
                    child_node.type == "risk",
                    sql.not_(Risk.risk_type.in_(["top5", "policy"])),
                    sql.not_(Risk.skip_evaluation is True),
                    Risk.identification == "no",
                    child_node.depth > SurveyTreeItem.depth,
                    child_node.path.like(SurveyTreeItem.path + "%"),
                )
            )
        ),
    )


MODULE_WITH_RISK_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER = (
    _MODULE_WITH_RISK_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER_factory()
)

# Used by tno.euphorie
RISK_PRESENT_FILTER = sql.and_(
    SurveyTreeItem.type == "risk",
    sql.exists(
        sql.select([Risk.sql_risk_id]).where(
            sql.and_(Risk.sql_risk_id == SurveyTreeItem.id, Risk.identification == "no")
        )
    ),
)


def _RISK_PRESENT_FILTER_TOP5_TNO_FILTER_factory():
    Risk_ = orm.aliased(Risk)
    return sql.and_(
        SurveyTreeItem.type == "risk",
        sql.exists(
            sql.select([Risk_.sql_risk_id]).where(
                sql.and_(
                    Risk_.sql_risk_id == SurveyTreeItem.id,
                    sql.or_(
                        Risk_.identification == "no",
                        sql.and_(
                            Risk_.risk_type == "top5",
                            sql.or_(
                                sql.not_(Risk_.identification.in_(["n/a", "yes"])),
                                Risk_.identification == None,  # noqa: E711
                            ),
                        ),
                    ),
                )
            )
        ),
    )


RISK_PRESENT_FILTER_TOP5_TNO_FILTER = _RISK_PRESENT_FILTER_TOP5_TNO_FILTER_factory()


def _RISK_PRESENT_OR_TOP5_FILTER_factory():
    Risk_ = orm.aliased(Risk)
    return sql.and_(
        SurveyTreeItem.type == "risk",
        sql.exists(
            sql.select([Risk_.sql_risk_id]).where(
                sql.and_(
                    Risk_.sql_risk_id == SurveyTreeItem.id,
                    sql.or_(
                        Risk_.identification == "no",
                        Risk_.risk_type == "top5",
                    ),
                )
            )
        ),
    )


RISK_PRESENT_OR_TOP5_FILTER = _RISK_PRESENT_OR_TOP5_FILTER_factory()

RISK_PRESENT_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER = sql.and_(
    SurveyTreeItem.type == "risk",
    sql.exists(
        sql.select([Risk.sql_risk_id]).where(
            sql.and_(
                Risk.sql_risk_id == SurveyTreeItem.id,
                sql.not_(Risk.risk_type.in_(["top5", "policy"])),
                sql.not_(Risk.skip_evaluation == True),  # noqa: E712
                Risk.identification == "no",
            )
        )
    ),
)

EVALUATION_FILTER = sql.or_(
    MODULE_WITH_RISK_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER,
    RISK_PRESENT_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER,
)

ACTION_PLAN_FILTER = sql.or_(
    MODULE_WITH_RISK_OR_TOP5_FILTER,
    RISK_PRESENT_OR_TOP5_FILTER,
)


def _SKIPPED_MODULE_factory():
    child_node = orm.aliased(SurveyTreeItem)
    sql.exists().where(
        sql.and_(
            SurveyTreeItem.type == "module",
            child_node.session_id == SurveyTreeItem.session_id,
            child_node.skip_children == True,  # noqa: E712
        )
    )


SKIPPED_MODULE = _SKIPPED_MODULE_factory()


def _UNANSWERED_RISKS_FILTER_factory():
    Risk_ = orm.aliased(Risk)
    return sql.and_(
        SurveyTreeItem.type == "risk",
        sql.exists(
            sql.select([Risk_.sql_risk_id]).where(
                sql.and_(
                    Risk_.sql_risk_id == SurveyTreeItem.id,
                    Risk_.identification == None,  # noqa: E711
                )
            )
        ),
    )


UNANSWERED_RISKS_FILTER = _UNANSWERED_RISKS_FILTER_factory()


def _MODULE_WITH_UNANSWERED_RISKS_FILTER_factory():
    child_node = orm.aliased(SurveyTreeItem)
    return sql.and_(
        SurveyTreeItem.type == "module",
        SurveyTreeItem.skip_children == False,  # noqa: E712
        sql.exists(
            sql.select([child_node.id]).where(
                sql.and_(
                    child_node.session_id == SurveyTreeItem.session_id,
                    child_node.id == Risk.sql_risk_id,
                    child_node.type == "risk",
                    Risk.identification is None,
                    child_node.depth > SurveyTreeItem.depth,
                    child_node.path.like(SurveyTreeItem.path + "%"),
                )
            )
        ),
    )


MODULE_WITH_UNANSWERED_RISKS_FILTER = _MODULE_WITH_UNANSWERED_RISKS_FILTER_factory()


def _MODULE_WITH_RISKS_NOT_PRESENT_FILTER_factory():
    child_node = orm.aliased(SurveyTreeItem)
    return sql.and_(
        SurveyTreeItem.type == "module",
        SurveyTreeItem.skip_children == False,  # noqa: E712
        sql.exists(
            sql.select([child_node.id]).where(
                sql.and_(
                    child_node.session_id == SurveyTreeItem.session_id,
                    child_node.id == Risk.sql_risk_id,
                    child_node.type == "risk",
                    Risk.identification == "yes",
                    child_node.depth > SurveyTreeItem.depth,
                    child_node.path.like(SurveyTreeItem.path + "%"),
                )
            )
        ),
    )


MODULE_WITH_RISKS_NOT_PRESENT_FILTER = _MODULE_WITH_RISKS_NOT_PRESENT_FILTER_factory()


def RISK_NOT_PRESENT_FILTER_factory():
    Risk_ = orm.aliased(Risk)
    return sql.and_(
        SurveyTreeItem.type == "risk",
        sql.exists(
            sql.select([Risk_.sql_risk_id]).where(
                sql.and_(
                    Risk_.sql_risk_id == SurveyTreeItem.id,
                    Risk_.identification == "yes",
                )
            )
        ),
    )


RISK_NOT_PRESENT_FILTER = RISK_NOT_PRESENT_FILTER_factory()


def get_current_account():
    """XXX this would be better placed in an api module, but we need to avoid
    circular dependencies.

    :return: The current Account instance if a user can be found,
             otherwise None
    """
    user_id = api.user.get_current().getId()
    if user_id is None:
        return
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        # If we pass a user id that can't be transformed to an integer,
        # we get a "DataError (psycopg2.errors.InvalidTextRepresentation)
        # invalid input syntax for type integer.""  When that happens, you get
        # tracebacks like this when another SQL query is done in the same Zope
        # transaction:
        # "psycopg2.errors.InFailedSqlTransaction: current transaction is
        # aborted, commands ignored until end of transaction block"
        # So we prevent this problem by not executing such a query.
        log.warning("Unable to fetch account for non-integer user id: %r", user_id)
        return
    try:
        return Session.query(Account).filter(Account.id == user_id).first()
    except Exception:
        log.warning("Unable to fetch account for user id: %r", user_id)


class DefaultView(BrowserView):
    """Default @@index_html view for the objects in the model."""

    def __call__(self):
        """Somebody called the default view for this object:

        we do not want this to happen so we display a message and
        redirect the user to the session start page
        """
        api.portal.show_message(
            "Wrong URL: %s" % self.request.getURL(), self.request, "warning"
        )
        webhelpers = api.content.get_view("webhelpers", self.context, self.request)
        target = webhelpers.traversed_session.absolute_url() + "/@@start"
        return self.request.response.redirect(target)


@ram.cache(lambda _: "show_timezone_cache_key")
def show_timezone():
    timezone = Session.execute("SHOW TIMEZONE").first()
    return pytz.timezone(timezone[0])


__all__ = [
    "SurveySession",
    "Module",
    "Risk",
    "ActionPlan",
    "SKIPPED_PARENTS",
    "MODULE_WITH_RISK_FILTER",
    "MODULE_WITH_RISK_TOP5_TNO_FILTER",
    "RISK_PRESENT_FILTER",
    "RISK_PRESENT_FILTER_TOP5_TNO_FILTER",
    "get_current_account",
]
