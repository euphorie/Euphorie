from plone.protect.auto import ProtectTransform
from zope.sqlalchemy.datamanager import SessionDataManager

import logging


logger = logging.getLogger(__name__)


class EuphorieProtectTransform(ProtectTransform):
    def _registered_objects(self):
        print("EuphorieProtectTransform._registered_objects")
        registered = super()._registered_objects()
        if registered:
            print(f"  initially {len(registered)} registered objects:")
            print(registered)
        else:
            print("  initially no registered objects")
        app = self.request.PARENTS[-1]
        for name, conn in app._p_jar.connections.items():
            print(f"  connection: {name}")
            if name == "temporary":
                continue
            for resource in conn.transaction_manager.get()._resources:
                if isinstance(resource, SessionDataManager):
                    print(f"    resource: {resource}")
                    if "write" in self.request.URL or self.request.get("write"):
                        print(f"        resource.session={resource.session}:")
                        print(f"            dirty? {resource.session.dirty}")
                        print(f"            new? {resource.session.new}")
                        print(f"            deleted? {resource.session.deleted}")
                        print("        Resource TRANSACTION:")
                        print(f"             dirty? {bool(resource.tx._dirty)}")
                        print(f"             new? {bool(resource.tx._new)}")
                        print(f"             deleted? {bool(resource.tx._deleted)}")
                    orig = len(registered)
                    registered.extend(resource.session.dirty)
                    registered.extend(resource.session.new)
                    registered.extend(resource.session.deleted)
                    # Some changes may have been flushed already, but not yet
                    # committed.  This is because in z3c.saconfig by default
                    # autoflush is true.  This means you get a flush on every query.
                    # Solution (hopefully): check the dirty/new/deleted state
                    # of the transaction object of the resource.
                    try:
                        registered.extend(resource.tx._dirty)
                        registered.extend(resource.tx._new)
                        registered.extend(resource.tx._deleted)
                    except AttributeError:
                        # We access private attributes, so let's catch exceptions.
                        # Otherwise valid transactions may be aborted.
                        logger.warning(
                            "Could not access private attributes of resource.tx."
                        )

                    if len(registered) != orig:
                        print(f"      added {len(registered) - orig} objects")
                    else:
                        print("      no new objects added")
        return registered
