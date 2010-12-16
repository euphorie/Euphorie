import datetime
import logging
import random
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from sqlalchemy import sql
from sqlalchemy.sql import functions
from sqlalchemy.ext import declarative
from euphorie.client.enum import Enum
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
import Acquisition
from AccessControl.PermissionRole import _what_not_even_god_should_do
import OFS.Traversable
from zope.interface import implements
from Products.PluggableAuthService.interfaces.authservice import IBasicUser

metadata = None

log = logging.getLogger(__name__)


def GenerateSecret(length=32):
    """Return random data."""
    secret=""
    for i in range(length):
        secret+=chr(random.getrandbits(8))

    return secret



class BaseObject(OFS.Traversable.Traversable, Acquisition.Implicit):
    """Zope 2-style base class for our models.

    This base class allows SQL based objects to act like normal Zope 2 objects.
    In particular it allows acquisition to find skin objects and keeps
    absolute_url() and getPhysicalPath() working.
    """
    __init__ = declarative._declarative_constructor
    __allow_access_to_unprotected_subobjects__ = True

    def getId(self):
        return str(self.id)


class SurveyTreeItem(BaseObject):
    """A tree of questions.

    The data is stored in the form of a materialized tree. The path is
    build using list of item numbers. Each item number has three digits and
    uses 0-prefixing to make sure we can use simple string sorting to produce a
    sorted tree.
    """
    __tablename__ = "tree"
    __table_args__ = schema.UniqueConstraint("session_id", "path")

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False, index=True)
    parent_id = schema.Column(types.Integer(),
        schema.ForeignKey("tree.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True, index=True)
    type = schema.Column(Enum(["risk", "module" ]),
            nullable=False, index=True)
    path = schema.Column(types.String(40), nullable=False, index=True)
    zodb_path = schema.Column(types.String(40), nullable=False)
    profile_index = schema.Column(types.Integer(), default=0, nullable=False)
    depth = schema.Column(types.Integer(), default=0, nullable=False, index=True)
    title = schema.Column(types.Unicode(512))
    postponed = schema.Column(types.Boolean())
    skip_children = schema.Column(types.Boolean(), default=False, nullable=False)

    __mapper_args__ = dict(polymorphic_on=type)

    session = orm.relation("SurveySession", cascade="all")
#    parent = orm.relation("SurveyTreeItem", uselist=False)

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
                path=path[3:]
        return slice(self.path)

    @property
    def number(self):
        return ".".join(self.short_path)


    def children(self, filter=None):
        query=Session.query(SurveyTreeItem)\
               .filter(SurveyTreeItem.session_id==self.session_id)\
               .filter(SurveyTreeItem.depth==self.depth+1)
        if self.path:
            query=query.filter(SurveyTreeItem.path.like(self.path+"%"))
        if filter is not None:
            query=query.filter(filter)

        return query.order_by(SurveyTreeItem.path)


    def siblings(self, klass=None, filter=None):
        if not self.path:
            return []

        if klass is None:
            klass=SurveyTreeItem

        query=Session.query(klass)\
                .filter(klass.session_id==self.session_id)\
                .filter(klass.parent_id==self.parent_id)
        if filter is not None:
            query=query.filter(sql.or_(klass.id==self.id, filter))

        return query.order_by(klass.path)


    def addChild(self, item):
        sqlsession=Session()
        query=sqlsession.query(SurveyTreeItem.path)\
                .filter(SurveyTreeItem.session_id==self.session_id)\
                .filter(SurveyTreeItem.depth==self.depth+1)
        if self.path:
            query=query.filter(SurveyTreeItem.path.like(self.path+"%"))

        last=query.order_by(SurveyTreeItem.path.desc()).first()
        if not last:
            index=1
        else:
            index=int(last[0][-3:])+1

        item.session=self.session
        item.depth=self.depth+1
        item.path=(self.path and self.path or "") + "%03d" % index
        item.parent_id=self.id
        sqlsession.add(item)
        self.session.touch()
        return item


    def removeChildren(self):
        session=Session()
        if self.path:
            filter=sql.and_(SurveyTreeItem.session_id==self.session_id,
                            SurveyTreeItem.path.like(self.path+"%"),
                            SurveyTreeItem.id!=self.id)
        else:
            filter=sql.and_(SurveyTreeItem.session_id==self.session_id,
                            SurveyTreeItem.id!=self.id)
        session.execute(SurveyTreeItem.__table__.delete().where(filter))
        self.session.touch()
        datamanager.mark_changed(session)



class Account(BaseObject):
    """A user account. Users have to register with euphorie before they can
    start a survey session. A single account can have multiple survey sessions.
    """
    implements(IBasicUser)

    __tablename__ = "account"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    loginname = schema.Column(types.String(255), nullable=False, index=True, unique=True)
    password = schema.Column(types.Unicode(64), nullable=False)
    tc_approved = schema.Column(types.Integer())

    @property
    def email(self):
        return self.loginname


    # PAS BasicUser implementation
    def getId(self):
        """Return the userid. For client accounts the login name is also
        used as userid."""
        return self.loginname

    def getUserName(self):
        """Return the login name."""
        return self.loginname

    def getRoles(self):
        """Return all global roles for this user."""

        return ("EuphorieUser",)

    def getRolesInContext(self, object):
        """Return the roles of the user in the current context."""
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
        return perm=="Euphorie: View a Survey"

    def allowed(self, object, object_roles=None):
        """Check if this account has any of the requested roles in the context
        of `object`."""
        if object_roles is _what_not_even_god_should_do:
            return False

        if object_roles is None:
            return True

        for role in [ "Anonymous", "Authenticated", "EuphorieUser"]:
            if role in object_roles:
                return True

        return False



class SurveySession(BaseObject):
    """Information about a users session.
    """

    __tablename__ = "session"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    account_id = schema.Column(types.Integer(),
            schema.ForeignKey(Account.id, onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False, index=True)
    title = schema.Column(types.Unicode(512))
    created = schema.Column(types.DateTime, nullable=False,
            default=functions.now())
    modified = schema.Column(types.DateTime, nullable=False,
            default=functions.now())
    zodb_path = schema.Column(types.String(128), nullable=False)

    report_comment = schema.Column(types.UnicodeText())

    account = orm.relation(Account,
            backref=orm.backref("sessions", order_by=modified,
                                cascade="all, delete, delete-orphan"))


    def hasTree(self):
        return bool(Session.query(SurveyTreeItem)
                .filter(SurveyTreeItem.session==self).count())


    def reset(self):
        Session.query(SurveyTreeItem)\
                .filter(SurveyTreeItem.session==self).delete()
        self.created=self.modified=datetime.datetime.now()


    def touch(self):
        self.modified=datetime.datetime.now()


    def addChild(self, item):
        sqlsession=Session()
        query=sqlsession.query(SurveyTreeItem.path)\
                .filter(SurveyTreeItem.session_id==self.id)\
                .filter(SurveyTreeItem.depth==1)\
                .order_by(SurveyTreeItem.path.desc())
        last=query.first()
        if not last:
            index=1
        else:
            index=int(last[0][-3:])+1

        item.session=self
        item.depth=1
        item.path="%03d" % index
        item.parent_id=None
        sqlsession.add(item)
        self.touch()
        return item


    def copySessionData(self, other):
        """Copy all user data from another session to this one.
        """
# XXX Rewrite UPDATE FROM as UPDATE .. WHERE x.id IN (select...) to make this work with SQLite
        statements=["""UPDATE tree
                       SET skip_children=old_tree.skip_children,
                           postponed=old_tree.postponed
                       FROM tree AS old_tree
                       WHERE tree.session_id=%(sessionid)d AND
                             old_tree.session_id=%(old_sessionid)d AND
                             tree.zodb_path=old_tree.zodb_path AND
                             tree.profile_index=old_tree.profile_index;
                    """,

                    """UPDATE risk
                       SET identification=old_risk.identification,
                           frequency=old_risk.frequency,
                           effect=old_risk.effect,
                           probability=old_risk.probability,
                           priority=old_risk.priority,
                           comment=old_risk.comment
                       FROM tree AS old_tree, tree AS new_tree, risk AS old_risk
                       WHERE new_tree.session_id=%(sessionid)d AND
                             new_tree.id=risk.id AND
                             old_tree.session_id=%(old_sessionid)s AND
                             old_tree.id=old_risk.id AND
                             new_tree.zodb_path=old_tree.zodb_path AND
                             new_tree.profile_index=old_tree.profile_index;
                    """,

                    """INSERT INTO action_plan (risk_id, action_plan, prevention_plan,
                                                requirements, responsible, budget,
                                                planning_start, planning_end)
                       SELECT action_plan.risk_id,
                              action_plan.action_plan,
                              action_plan.prevention_plan,
                              action_plan.requirements,
                              action_plan.responsible,
                              action_plan.budget,
                              action_plan.planning_start,
                              action_plan.planning_end
                       FROM action_plan JOIN risk ON action_plan.risk_id=risk.id
                                        JOIN tree ON tree.id=risk.id,
                            tree AS new_tree
                       WHERE tree.session_id=%(old_sessionid)d AND
                             new_tree.session_id=%(sessionid)d AND
                             tree.zodb_path=new_tree.zodb_path AND
                             tree.profile_index=new_tree.profile_index;
                    """,

                    """UPDATE company
                       SET session_id=%(sessionid)d
                       WHERE session_id=%(old_sessionid)d;
                    """,
                    ]

        parameters=dict(sessionid=self.id, old_sessionid=other.id)
        session=Session()
        for statement in statements:
            session.execute(statement % parameters)



class Company(BaseObject):
    """Information about a company."""
    __tablename__ = "company"
    __table_args__ = schema.UniqueConstraint("session_id", "path")

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(types.Integer(),
        schema.ForeignKey("session.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False, index=True)
    session = orm.relation("SurveySession",
            cascade="all,delete-orphan", single_parent=True,
            backref=orm.backref("company", uselist=False, cascade="all"))

    country = schema.Column(types.String(3))
    employees = schema.Column(Enum([None, "1-9", "10-49", "50-249", "250+"]))
    conductor = schema.Column(Enum([None, "staff", "third-party", "both"]))
    referer = schema.Column(Enum([None, "employers-organisation",
        "trade-union", "national-public-institution", "eu-institution",
        "health-safety-experts", "other"]))



class Module(SurveyTreeItem):
    """A module.

    This is a dummy object needed to be able to put modules in the
    survey tree.
    """
    __tablename__ = "module"
    __mapper_args__ = dict(polymorphic_identity="module")

    sql_module_id = schema.Column("id", types.Integer(),
            schema.ForeignKey(SurveyTreeItem.id, onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
    module_id = schema.Column(types.String(16), nullable=False)
    solution_direction = schema.Column(types.Boolean(), default=False)



class Risk(SurveyTreeItem):
    """Answer to risk."""

    __tablename__ = "risk"
    __mapper_args__ = dict(polymorphic_identity="risk")

    sql_risk_id = schema.Column("id", types.Integer(),
            schema.ForeignKey(SurveyTreeItem.id, onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
    risk_id = schema.Column(types.String(16), nullable=False)
    risk_type = schema.Column(Enum(["risk", "policy", "top5"]),
        default="risk", nullable=False, index=True)
    identification = schema.Column(Enum([None, u"yes", u"no", "n/a"]))
    frequency = schema.Column(types.Integer())
    effect = schema.Column(types.Integer())
    probability = schema.Column(types.Integer())
    priority = schema.Column(Enum([None, u"low", u"medium", u"high"]))
    comment = schema.Column(types.UnicodeText())



class ActionPlan(BaseObject):
    """Action plans for a known risk."""

    __tablename__ = "action_plan"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    risk_id = schema.Column(types.Integer(),
        schema.ForeignKey(Risk.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False, index=True)
    action_plan = schema.Column(types.UnicodeText())
    prevention_plan = schema.Column(types.UnicodeText())
    requirements = schema.Column(types.UnicodeText())
    responsible = schema.Column(types.Unicode(256))
    budget = schema.Column(types.Integer())
    planning_start = schema.Column(types.Date())
    planning_end = schema.Column(types.Date())

    risk = orm.relation(Risk,
            backref=orm.backref("action_plans",
                                cascade="all, delete, delete-orphan"))


_instrumented = False
if not _instrumented:
    metadata=schema.MetaData()
    metadata._decl_registry=dict()

    for cls in [ SurveyTreeItem, SurveySession, Module, Risk,
                 ActionPlan, Account, Company ]:
        declarative.instrument_declarative(cls, metadata._decl_registry, metadata)
    _instrumented = True


parent=orm.aliased(SurveyTreeItem)
# XXX This can be optimized by doing short-circuit on parent.type!=module
SKIPPED_PARENTS = \
    sql.exists().where(sql.and_(
        parent.session_id==SurveyTreeItem.session_id,
        SurveyTreeItem.depth>parent.depth,
        SurveyTreeItem.path.like(parent.path+"%"),
        parent.skip_children==True))
del parent

node=orm.aliased(SurveyTreeItem)

MODULE_WITH_RISK_FILTER = \
    sql.and_(SurveyTreeItem.type=="module",
             SurveyTreeItem.skip_children==False,
             sql.exists(sql.select([node.id]).where(sql.and_(
                   node.session_id==SurveyTreeItem.session_id,
                   node.id==Risk.sql_risk_id,
                   node.type=="risk",
                   Risk.identification=="no",
                   node.depth>SurveyTreeItem.depth,
                   node.path.like(SurveyTreeItem.path+"%")))))

MODULE_WITH_RISK_OR_TOP5_FILTER = \
    sql.and_(SurveyTreeItem.type=="module",
             SurveyTreeItem.skip_children==False,
             sql.exists(sql.select([node.id]).where(sql.and_(
                   node.session_id==SurveyTreeItem.session_id,
                   node.id==Risk.sql_risk_id,
                   node.type=="risk",
                   sql.or_(Risk.identification=="no", Risk.risk_type=="top5"),
                   node.depth>SurveyTreeItem.depth,
                   node.path.like(SurveyTreeItem.path+"%")))))

MODULE_WITH_RISK_NO_TOP5_NO_POLICY_FILTER = \
    sql.and_(SurveyTreeItem.type=="module",
             SurveyTreeItem.skip_children==False,
             sql.exists(sql.select([node.id]).where(sql.and_(
                   node.session_id==SurveyTreeItem.session_id,
                   node.id==Risk.sql_risk_id,
                   node.type=="risk",
                   sql.not_(Risk.risk_type.in_(["top5", "policy"])),
                   Risk.identification=="no",
                   node.depth>SurveyTreeItem.depth,
                   node.path.like(SurveyTreeItem.path+"%")))))

RISK_PRESENT_FILTER = \
      sql.and_(SurveyTreeItem.type=="risk",
               sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
                   Risk.sql_risk_id==SurveyTreeItem.id,
                   Risk.identification=="no"))))

RISK_PRESENT_OR_TOP5_FILTER = \
      sql.and_(SurveyTreeItem.type=="risk",
               sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
                   Risk.sql_risk_id==SurveyTreeItem.id,
                   sql.or_(Risk.identification=="no", Risk.risk_type=="top5")))))

RISK_PRESENT_NO_TOP5_NO_POLICY_FILTER = \
      sql.and_(SurveyTreeItem.type=="risk",
               sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
                   Risk.sql_risk_id==SurveyTreeItem.id,
                   sql.not_(Risk.risk_type.in_(['top5', 'policy'])),
                   Risk.identification=="no"))))
del node

__all__ = [ "SurveySession", "Module", "Risk", "ActionPlan",
            "SKIPPED_PARENTS","MODULE_WITH_RISK_FILTER",
            "RISK_PRESENT_FILTER", "RISK_PRESENT_NO_TOP5_NO_POLICY_FILTER" ]


