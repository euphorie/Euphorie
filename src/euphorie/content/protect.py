from plone.protect.authenticator import check
from plone.protect.auto import ProtectTransform
from zExceptions import Forbidden
from zope.globalrequest import getRequest
from zope.interface import Interface
from zope.sqlalchemy.datamanager import SessionDataManager

import logging
import os


logger = logging.getLogger(__name__)
SAFE_WRITE_KEY = "euphorie.protect.safe_sql_ids"
_marker = object()

# By default we disable CSRF protection for SQL writes, to avoid breaking
# existing code and tests.  Set the environment variable
# EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL=1 to enable CSRF protection
# for SQL writes.
EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL = os.getenv(
    "EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL", 0
)
try:
    from plone.base.utils import is_truthy

    EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL = is_truthy(
        EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL
    )
except ImportError:
    # BBB for Plone 6.1.1 and earlier
    EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL = bool(
        int(EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL)
    )


def _get_obj_key(obj):
    klass = obj.__class__
    try:
        obj_id = obj.id
    except AttributeError:
        # For example Group has group_id.
        # TODO There may be nicer ways to get the primary key.
        # Maybe somehow do that once for each table at startup,
        # or keep a small list in memory that we fill as needed.
        # Also, there could be multiple primary keys.
        primary_key = klass.__table__.primary_key.columns.keys()[0]
        obj_id = getattr(obj, primary_key)
    return (klass.__name__, obj_id)


def safeSQLWrite(obj, request=None):
    """Mark SQL object as safe to write, even in GET request.

    This is our SQLAlchemy variant of plone.protect.utils.safeWrite.

    Maybe we only need this on GET requests.  But plone.protect does it on all
    request types.  Oh, right: if you have a form that does a POST, but that form
    misses the CSRF token, you would also get a Forbidden.  So we do this on all
    requests as well.
    """
    if request is None:
        request = getRequest()
    if request is None or getattr(request, "environ", _marker) is _marker:
        # Request not found or it is a TestRequest without an environment.
        logger.debug("Could not mark object as a safe write: %s", obj)
        return
    if SAFE_WRITE_KEY not in request.environ:
        request.environ[SAFE_WRITE_KEY] = set()
    try:
        key = _get_obj_key(obj)
        if key not in request.environ[SAFE_WRITE_KEY]:
            request.environ[SAFE_WRITE_KEY].add(key)
    except AttributeError:
        logger.warning("Can't get object key to mark object as safe: %s", obj)


class IDisableCSRFProtectionForSQL(Interface):
    """Marker interface: disable auto CSRF on SQL objects in a request"""


class EuphorieProtectTransform(ProtectTransform):
    """plone.protect auto CSRF transform for Euphorie.

    The standard Plone auto CSRF protection works fine for standard Plone
    objects, but it ignores changes in SQLAlchemy items.
    This override adds such protection, but detecting changed SQLALchemy
    items, and adding them to the list of 'registered' Plone items that are
    changed by this transaction.

    These changes can be found in the session, in one of the attributes
    'dirty', 'new', 'deleted'.  For example 'dirty' may be:

        IdentitySet([<euphorie.client.model.SurveySession object at ...>])

    But when a flush of the session has happened, the changes from before the
    flush are not on the session, but are hidden in a transaction object,
    which is different:

        (Pdb) resource.tx._dirty
        <WeakKeyDictionary at 0x14aaaf390>
        (Pdb) !list(resource.tx._dirty)
        [<sqlalchemy.orm.state.InstanceState object at 0x14a7af410>]
        (Pdb) state = list(resource.tx._dirty)[0]
        (Pdb) state
        <sqlalchemy.orm.state.InstanceState object at 0x14a7af410>
        (Pdb) state.obj
        <weakref at 0x14ad29670; to 'SurveySession' at 0x14a7afcd0>
        (Pdb) state.obj()
        <euphorie.client.model.SurveySession object at 0x14a7afcd0>

    It should be fine to just add the InstanceState objects from the weak
    dictionary to the 'registered' list.  If anything is in this list on a
    GET request, we will get redirected to the confirm-action view.

    But it would be nice to add the actual SQLAlchemy items: they may have
    been marked by `plone.protect.auto.safeWrite`.

    Problem though: safeWrite fails when the object has no `_p_oid`.
    And if you would change that function, you would still need to change
    the `_check` method of the transform as it has this check:

        if getattr(obj, "_p_oid", False) in safe_oids:
            continue

    So we have created our own safeSQLWrite function and let this store the
    klass name and the id or other primary key of the sql object in a list
    in the request, similar to safe_oids list from plone.protect.
    Then we check this list of safe items below in our `_registered_objects`
    method: if an item is in the list, don't add it to the `registered` list.

    We have also defined a variant of IDisableCSRFProtection specific for
    SQLAlchemy items.  If that marker interface is set, we only return
    the `_registered_objects` of our super class, without checking for SQL
    items.  This may be needed in a few cases, at least temporarily: there may
    be some existing cases of a valid write without authenticator that worked
    so far, but that would break with our restored csrf protection.

    Note that the best way of preventing errors or warnings due to csrf
    protection, is by making sure that links and forms contain the
    authenticator.

    One more note of warning: on the client side I get a Forbidden when I
    get redirected to the confirm-action view on the Plone Site root.  A client
    side user does not have View permission there.  So we may need some changes
    there.
    """

    # Define variable in class so we can easily override it in tests.
    euphorie_enable_csrf_protection_for_sql = EUPHORIE_ENABLE_CSRF_PROTECTION_FOR_SQL

    @staticmethod
    def _get_real_objects(tx, name):
        return [state.obj() for state in getattr(tx, name, [])]

    def filter_on_safe_keys(self, registered):
        if not registered:
            return registered

        safe_keys = []
        if SAFE_WRITE_KEY in getattr(self.request, "environ", {}):
            safe_keys = self.request.environ[SAFE_WRITE_KEY]
        if not safe_keys:
            return registered

        filtered = []
        for obj in registered:
            try:
                key = _get_obj_key(obj)
            except AttributeError:
                logger.warning("Can't get object key: %s", obj)
                # If we can't get a key, it can't have been marked as safe
                # either, so we keep the object.
                filtered.append(obj)
                continue
            if key not in safe_keys:
                filtered.append(obj)
        return filtered

    def _registered_sql_objects(self):
        """Get changed SQLAlchemy objects in the current transaction.

        Here we don't care if SQL CSRF protection is enabled in general or not:
        we just return all changed SQL objects.
        But if it was explicitly disabled for this request by the marker
        interface, we return an empty list.
        """
        new_registered = []
        if IDisableCSRFProtectionForSQL.providedBy(self.request):
            return new_registered

        app = self.request.PARENTS[-1]
        for name, conn in app._p_jar.connections.items():
            if name == "temporary":
                continue
            for resource in conn.transaction_manager.get()._resources:
                if isinstance(resource, SessionDataManager):
                    # Get changed, new, and deleted items from the session.
                    for attr in ("dirty", "new", "deleted"):
                        new_registered.extend(getattr(resource.session, attr, []))
                    # Get changes that have been flushed already.
                    for attr in ("_dirty", "_new", "_deleted"):
                        new_registered.extend(self._get_real_objects(resource.tx, attr))
        return self.filter_on_safe_keys(new_registered)

    def _registered_objects(self):
        registered = super()._registered_objects()

        new_registered = self._registered_sql_objects()
        if not new_registered:
            # Return the original list.
            return registered

        if self.euphorie_enable_csrf_protection_for_sql:
            registered.extend(new_registered)
        else:
            # We still want to warn about this.  But that only makes sense
            # if the authenticator check fails.
            try:
                check(self.request, manager=self.key_manager)
            except Forbidden:
                logger.warning(
                    "CSRF protection for SQLAlchemy changes is not enabled, "
                    "allowing %d unauthenticated changes on %s request %s",
                    len(new_registered),
                    self.request.REQUEST_METHOD,
                    self.request.URL,
                )

        return registered
