from plone.protect.auto import ProtectTransform
from zope.interface import Interface
from zope.sqlalchemy.datamanager import SessionDataManager


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

    We could create our own safeSQLWrite function and let this store for
    example the `id(sql_object)` in a similar safe_oids list in the request or
    maybe the session object.  Then check this list of safe identitites below
    in our `_registered_objects` method: if an item is in the list, don't add
    it to the `registered` list.

    But if you get the same sql_object by doing a new query, its identity will
    be different, so this would not work.  Maybe safeSQLWrite could write
    the model name and the primary key.  But then we would need to figure
    out which field per model is the primary key.  Could be doable.

    Simpler would be to add a variant of IDisableCSRFProtection specific for
    SQLAlchemy items.  If that marker interface is set, we would only return
    the `_registered_objects` of our super class, without checking for SQL
    items.  That seems simple enough.  And I think this might be needed in a
    few cases, at least temporarily: there may be some existing cases of a
    valid write-on-GET that worked so far, but that would break with our
    restored csrf protection.

    One more note of warning:: on the client side I get a Forbidden when I
    get redirected to the confirm-action view.  We may need some changes there.
    """

    def _get_real_objects(self, tx, name):
        return [state.obj() for state in getattr(tx, name, [])]

    def _registered_objects(self):
        registered = super()._registered_objects()
        if IDisableCSRFProtectionForSQL.providedBy(self.request):
            return registered

        app = self.request.PARENTS[-1]
        for name, conn in app._p_jar.connections.items():
            if name == "temporary":
                continue
            for resource in conn.transaction_manager.get()._resources:
                if isinstance(resource, SessionDataManager):
                    # Get changed, new, and deleted items from the session.
                    registered.extend(resource.session.dirty)
                    registered.extend(resource.session.new)
                    registered.extend(resource.session.deleted)
                    # Get changes that have been flushed already.
                    for attr in ("_dirty", "_new", "_deleted"):
                        registered.extend(self._get_real_objects(resource.tx, attr))

        return registered
