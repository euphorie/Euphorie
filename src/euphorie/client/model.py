"""
Model
-----

Mainly: the connection between the ZODB-based content of the backend and the
SQL-based individual session content of the client users.
Also: PAS-based user account for users of the client
"""

import datetime
import logging
import random
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from sqlalchemy import sql
from sqlalchemy.sql import functions
from sqlalchemy.ext import declarative
from z3c.saconfig import Session
from zope.sqlalchemy import datamanager
from zope.interface import implements
import Acquisition
import OFS.Traversable
from AccessControl.PermissionRole import _what_not_even_god_should_do
from zope.component.hooks import getSite
from Products.PluggableAuthService.interfaces.authservice import IBasicUser
from euphorie.client.enum import Enum


metadata = schema.MetaData()

log = logging.getLogger(__name__)


def GenerateSecret(length=32):
    """Return random data."""
    secret = ""
    for i in range(length):
        secret += chr(random.getrandbits(8))
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

    The data is stored in the form of a materialized tree. The path is built
    using a list of item numbers. Each item number has three digits and uses
    0-prefixing to make sure we can use simple string sorting to produce a
    sorted tree.
    """
    __tablename__ = "tree"
    __table_args__ = (schema.UniqueConstraint("session_id", "path"),
                      schema.UniqueConstraint("session_id",
                          "zodb_path", "profile_index"),
                      {})

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(types.Integer(),
        schema.ForeignKey("session.id",
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False, index=True)
    parent_id = schema.Column(types.Integer(),
        schema.ForeignKey("tree.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True, index=True)
    type = schema.Column(Enum(["risk", "module"]),
            nullable=False, index=True)
    path = schema.Column(types.String(40), nullable=False, index=True)
    has_description = schema.Column(types.Boolean(), default=False, index=True)
    zodb_path = schema.Column(types.String(512), nullable=False)
    profile_index = schema.Column(types.Integer(), default=0, nullable=False)
    depth = schema.Column(types.Integer(), default=0, nullable=False,
            index=True)
    title = schema.Column(types.Unicode(512))
    postponed = schema.Column(types.Boolean())
    skip_children = schema.Column(types.Boolean(), default=False,
            nullable=False)

    __mapper_args__ = dict(polymorphic_on=type)

    session = orm.relation("SurveySession", cascade="all")
#    parent = orm.relation("SurveyTreeItem", uselist=False)

    @property
    def parent(self):
# XXX Evil! Figure out why the parent relation does not work
        return self.parent_id and \
                Session.query(SurveyTreeItem).get(self.parent_id)

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
        return '.'.join(self.short_path)

    def children(self, filter=None):
        query = Session.query(SurveyTreeItem)\
            .filter(SurveyTreeItem.session_id == self.session_id)\
            .filter(SurveyTreeItem.depth == self.depth + 1)
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
        query = Session.query(klass)\
            .filter(klass.session_id == self.session_id)\
            .filter(klass.parent_id == self.parent_id)
        if filter is not None:
            query = query.filter(sql.or_(klass.id == self.id, filter))
        return query.order_by(klass.path)

    def addChild(self, item):
        sqlsession = Session()
        query = sqlsession.query(SurveyTreeItem.path)\
            .filter(SurveyTreeItem.session_id == self.session_id)\
            .filter(SurveyTreeItem.depth == self.depth + 1)
        if self.path:
            query = query.filter(SurveyTreeItem.path.like(self.path + "%"))

        last = query.order_by(SurveyTreeItem.path.desc()).first()
        if not last:
            index = 1
        else:
            index = int(last[0][-3:]) + 1

        item.session = self.session
        item.depth = self.depth + 1
        item.path = (self.path and self.path or "") + "%03d" % index
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
                        sql.not_(SurveyTreeItem.id.in_(excluded))
                    )
        else:
            filter = sql.and_(
                        SurveyTreeItem.session_id == self.session_id,
                        sql.not_(SurveyTreeItem.id.in_(excluded))
                    )
        removed = session.query(SurveyTreeItem).filter(filter).all()
        session.execute(SurveyTreeItem.__table__.delete().where(filter))
        self.session.touch()
        datamanager.mark_changed(session)
        return removed


class Account(BaseObject):
    """A user account. Users have to register with euphorie before they can
    start a survey session. A single account can have multiple survey sessions.
    """
    implements(IBasicUser)

    __tablename__ = "account"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    loginname = schema.Column(
        types.String(255),
        nullable=False,
        index=True,
        unique=True
    )
    password = schema.Column(types.Unicode(64))
    tc_approved = schema.Column(types.Integer())
    account_type = schema.Column(
            Enum([u"guest", u"converted", None]), default=None, nullable=True)

    @property
    def email(self):
        """Email addresses are used for login, return the login.
        """
        return self.loginname

    @property
    def login(self):
        """This synchs naming with :obj:`euphorie.content.user.IUser` and is
        needed by the authentication tools.
        """
        return self.loginname

    def getUserName(self):
        """Return the login name."""
        return self.loginname

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

    def allowed(self, object, object_roles=None):
        """Check if this account has any of the requested roles in the context
        of `object`."""
        if object_roles is _what_not_even_god_should_do:
            return False

        if object_roles is None:
            return True

        for role in ["Anonymous", "Authenticated", "EuphorieUser"]:
            if role in object_roles:
                return True

        return False


class AccountChangeRequest(BaseObject):
    __tablename__ = "account_change"

    id = schema.Column(types.String(16), primary_key=True, nullable=False)
    account_id = schema.Column(types.Integer(),
            schema.ForeignKey(Account.id,
                onupdate="CASCADE", ondelete="CASCADE"),
            nullable=False, unique=True)
    account = orm.relation(Account,
            backref=orm.backref("change_request",
                                uselist=False,
                                cascade="all, delete, delete-orphan"))
    value = schema.Column(types.String(255), nullable=False)
    expires = schema.Column(types.DateTime(),
            nullable=False)


class SurveySession(BaseObject):
    """Information about a user's session.
    """
    __tablename__ = "session"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    account_id = schema.Column(types.Integer(),
            schema.ForeignKey(Account.id,
                onupdate="CASCADE", ondelete="CASCADE"),
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
                .filter(SurveyTreeItem.session == self).count())

    def reset(self):
        Session.query(SurveyTreeItem)\
                .filter(SurveyTreeItem.session == self).delete()
        self.created = self.modified = datetime.datetime.now()

    def touch(self):
        self.modified = datetime.datetime.now()

    def addChild(self, item):
        sqlsession = Session()
        query = sqlsession.query(SurveyTreeItem.path)\
                .filter(SurveyTreeItem.session_id == self.id)\
                .filter(SurveyTreeItem.depth == 1)\
                .order_by(SurveyTreeItem.path.desc())
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
        query = Session.query(SurveyTreeItem)\
            .filter(SurveyTreeItem.session_id == self.id)\
            .filter(SurveyTreeItem.depth == 1)
        if filter is not None:
            query = query.filter(filter)
        return query.order_by(SurveyTreeItem.path)

    def copySessionData(self, other):
        """Copy all user data from another session to this one.
        """
        session = Session()

        # Copy all tree data to the new session (skip_children and postponed)
        old_tree = orm.aliased(SurveyTreeItem, name='old_tree')
        in_old_tree = sql.and_(
                old_tree.session_id == other.id,
                SurveyTreeItem.zodb_path == old_tree.zodb_path,
                SurveyTreeItem.profile_index == old_tree.profile_index)
        skip_children = sql.select([old_tree.skip_children], in_old_tree)
        postponed = sql.select([old_tree.postponed], in_old_tree)
        new_items = session.query(SurveyTreeItem)\
                    .filter(SurveyTreeItem.session == self)\
                    .filter(sql.exists(
                        sql.select([old_tree.id]).where(in_old_tree)))
        new_items.update({'skip_children': skip_children,
                          'postponed': postponed},
                         synchronize_session=False)

        # Mandatory modules must have skip_children=False. It's possible that
        # the module was optional with skip_children=True and now after the
        # update it's mandatory. So we must check and correct.
        # In case a risk was marked as "always present", be sure its
        # identification gets set to 'no'
        preset_to_no = []
        survey = getSite()['client'].restrictedTraverse(self.zodb_path)
        for item in new_items.all():
            if item.type == 'risk':
                if item.identification == u'no':
                    preset_to_no.append(item.risk_id)

            elif item.type == 'module':
                module = survey.restrictedTraverse(item.zodb_path.split("/"))
                if not module.optional:
                    item.skip_children = False

# Copy all risk data to the new session
# This triggers a "Only update via a single table query is currently supported"
# error with SQLAlchemy 0.6.6
#        old_risk = orm.aliased(Risk.__table__, name='old_risk')
#        is_old_risk = sql.and_(in_old_tree, old_tree.id == old_risk.id)
#        identification = sql.select([old_risk.identification], is_old_risk)
#        new_risks = session.query(Risk)\
#                .filter(Risk.session == self)\
#                .filter(sql.exists(
#                    sql.select([SurveyTreeItem.id]).where(sql.and_(
#                            SurveyTreeItem.id == Risk.id,
#                            sql.exists([old_tree.id]).where(sql.and_(
#                                in_old_tree, old_tree.type == 'risk'))))))
#        new_risks.update({'identification': identification},
#                synchronize_session=False)

        skip_preset_to_no_clause = ""
        if len(preset_to_no):
            skip_preset_to_no_clause = "old_risk.risk_id not in %s AND" % (
                str([str(x) for x in preset_to_no]).replace('[', '(').replace(']', ')')
            )
        statement = """\
        UPDATE RISK
        SET identification = old_risk.identification,
            frequency = old_risk.frequency,
            effect = old_risk.effect,
            probability = old_risk.probability,
            priority = old_risk.priority,
            comment = old_risk.comment
        FROM risk AS old_risk JOIN tree AS old_tree ON old_tree.id=old_risk.id, tree
        WHERE tree.id=risk.id AND
              %(skip_preset_to_no_clause)s
              tree.session_id=%(new_sessionid)s AND
              old_tree.session_id=%(old_sessionid)s AND
              old_tree.zodb_path=tree.zodb_path AND
              old_tree.profile_index=tree.profile_index;
        """ % dict(
            old_sessionid=other.id, new_sessionid=self.id,
            skip_preset_to_no_clause=skip_preset_to_no_clause)
        session.execute(statement)

        statement = """\
        INSERT INTO action_plan (risk_id, action_plan, prevention_plan,
                                        requirements, responsible, budget,
                                        planning_start, planning_end)
               SELECT new_tree.id,
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
                     new_tree.session_id=%(new_sessionid)d AND
                     tree.zodb_path=new_tree.zodb_path AND
                     tree.profile_index=new_tree.profile_index;
            """ % {'old_sessionid': other.id, 'new_sessionid': self.id}
        session.execute(statement)

        session.query(Company)\
            .filter(Company.session == other)\
            .update({'session_id': self.id},
                    synchronize_session=False)


class Company(BaseObject):
    """Information about a company."""
    __tablename__ = "company"

    id = schema.Column(types.Integer(), primary_key=True, autoincrement=True)
    session_id = schema.Column(types.Integer(),
        schema.ForeignKey("session.id",
            onupdate="CASCADE", ondelete="CASCADE"),
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
    workers_participated = schema.Column(types.Boolean())
    needs_met = schema.Column(types.Boolean())
    recommend_tool = schema.Column(types.Boolean())


class Module(SurveyTreeItem):
    """A module.

    This is a dummy object needed to be able to put modules in the
    survey tree.
    """
    __tablename__ = "module"
    __mapper_args__ = dict(polymorphic_identity="module")

    sql_module_id = schema.Column("id", types.Integer(),
            schema.ForeignKey(SurveyTreeItem.id,
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
    module_id = schema.Column(types.String(16), nullable=False)
    solution_direction = schema.Column(types.Boolean(), default=False)


class Risk(SurveyTreeItem):
    """Answer to risk."""

    __tablename__ = "risk"
    __mapper_args__ = dict(polymorphic_identity="risk")

    sql_risk_id = schema.Column("id", types.Integer(),
            schema.ForeignKey(SurveyTreeItem.id,
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
    risk_id = schema.Column(types.String(16), nullable=True)
    risk_type = schema.Column(Enum([u"risk", u"policy", u"top5"]),
        default=u"risk", nullable=False, index=True)
    #: Skip-evaluation flag. This is only used to indicate if the sector
    #: set the evaluation method to `fixed`, not for policy behaviour
    #: such as not evaluation top-5 risks. That policy behaviour is
    #: handled via the question_filter on client views so it can be modified
    #: in custom deployments.
    skip_evaluation = schema.Column(types.Boolean(), default=False, nullable=False)
    is_custom_risk = schema.Column(types.Boolean(), default=False, nullable=False)
    identification = schema.Column(Enum([None, u"yes", u"no", "n/a"]))
    frequency = schema.Column(types.Integer())
    effect = schema.Column(types.Integer())
    probability = schema.Column(types.Integer())
    priority = schema.Column(Enum([None, u"low", u"medium", u"high"]))
    comment = schema.Column(types.UnicodeText())
    existing_measures = schema.Column(types.UnicodeText())


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
    reference = schema.Column(types.Text())

    risk = orm.relation(Risk,
            backref=orm.backref(
                "action_plans",
                order_by=id,
                cascade="all, delete, delete-orphan"))


_instrumented = False
if not _instrumented:
    metadata._decl_registry = {}
    for cls in [SurveyTreeItem, SurveySession, Module, Risk,
                ActionPlan, Account, AccountChangeRequest, Company]:
        declarative.instrument_declarative(cls,
                metadata._decl_registry, metadata)
    _instrumented = True


schema.Index('tree_session_path',
        SurveyTreeItem.session_id, SurveyTreeItem.path)
schema.Index('tree_zodb_path',
        SurveyTreeItem.session_id, SurveyTreeItem.profile_index,
        SurveyTreeItem.zodb_path)


parent = orm.aliased(SurveyTreeItem)
# XXX This can be optimized by doing short-circuit on parent.type!=module
SKIPPED_PARENTS = \
    sql.exists().where(sql.and_(
        parent.session_id == SurveyTreeItem.session_id,
        SurveyTreeItem.depth > parent.depth,
        SurveyTreeItem.path.like(parent.path + "%"),
        parent.skip_children == True))
del parent


child_node = orm.aliased(SurveyTreeItem)

NO_CUSTOM_RISKS_FILTER = \
    sql.not_(sql.and_(
        SurveyTreeItem.type == "risk",
        sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
            Risk.sql_risk_id == SurveyTreeItem.id,
            Risk.is_custom_risk == True))
    )))

RISK_OR_MODULE_WITH_DESCRIPTION_FILTER = \
    sql.or_(SurveyTreeItem.type != "module",
            SurveyTreeItem.has_description)

# Used by tno.euphorie
MODULE_WITH_RISK_FILTER = \
    sql.and_(SurveyTreeItem.type == "module",
             SurveyTreeItem.skip_children == False,
             sql.exists(sql.select([child_node.id]).where(sql.and_(
                 child_node.session_id == SurveyTreeItem.session_id,
                 child_node.id == Risk.sql_risk_id,
                 child_node.type == u"risk",
                 Risk.identification == u"no",
                 child_node.depth > SurveyTreeItem.depth,
                 child_node.path.like(SurveyTreeItem.path + "%")))))

MODULE_WITH_RISK_OR_TOP5_FILTER = \
    sql.and_(SurveyTreeItem.type == u"module",
             SurveyTreeItem.skip_children == False,
             sql.exists(sql.select([child_node.id]).where(sql.and_(
                 child_node.session_id == SurveyTreeItem.session_id,
                 child_node.id == Risk.sql_risk_id,
                 child_node.type == "risk",
                 sql.or_(Risk.identification == u"no",
                     Risk.risk_type == u"top5"),
                 child_node.depth > SurveyTreeItem.depth,
                 child_node.path.like(SurveyTreeItem.path + "%")))))

MODULE_WITH_RISK_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER = \
    sql.and_(SurveyTreeItem.type == "module",
             SurveyTreeItem.skip_children == False,
             sql.exists(sql.select([child_node.id]).where(sql.and_(
                 child_node.session_id == SurveyTreeItem.session_id,
                 child_node.id == Risk.sql_risk_id,
                 child_node.type == u"risk",
                 sql.not_(Risk.risk_type.in_([u"top5", u"policy"])),
                 sql.not_(Risk.skip_evaluation == True),
                 Risk.identification == u"no",
                 child_node.depth > SurveyTreeItem.depth,
                 child_node.path.like(SurveyTreeItem.path + "%")))))

# Used by tno.euphorie
RISK_PRESENT_FILTER = \
    sql.and_(SurveyTreeItem.type == "risk",
            sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
                Risk.sql_risk_id == SurveyTreeItem.id,
                Risk.identification == u"no"))))

RISK_PRESENT_OR_TOP5_FILTER = \
    sql.and_(SurveyTreeItem.type == "risk",
            sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
                Risk.sql_risk_id == SurveyTreeItem.id,
                sql.or_(Risk.identification == u"no",
                    Risk.risk_type == u"top5")))))

RISK_PRESENT_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER = \
    sql.and_(SurveyTreeItem.type == "risk",
            sql.exists(sql.select([Risk.sql_risk_id]).where(sql.and_(
                Risk.sql_risk_id == SurveyTreeItem.id,
                sql.not_(Risk.risk_type.in_([u'top5', u'policy'])),
                sql.not_(Risk.skip_evaluation == True),
                Risk.identification == u"no"))))

EVALUATION_FILTER = \
    sql.or_(MODULE_WITH_RISK_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER,
            RISK_PRESENT_NO_TOP5_NO_POLICY_DO_EVALUTE_FILTER)


ACTION_PLAN_FILTER = \
        sql.or_(MODULE_WITH_RISK_OR_TOP5_FILTER,
                RISK_PRESENT_OR_TOP5_FILTER)

del child_node

__all__ = ["SurveySession", "Module", "Risk", "ActionPlan",
           "SKIPPED_PARENTS", "MODULE_WITH_RISK_FILTER",
           "RISK_PRESENT_FILTER", "RISK_PRESENT_NO_TOP5_NO_POLICY_FILTER"]
