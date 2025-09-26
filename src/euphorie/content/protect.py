from plone.protect.auto import ProtectTransform
from zope.sqlalchemy.datamanager import SessionDataManager


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
                    if self.request.get("write"):
                        print(f"        resource.session={resource.session}:")
                        print(f"            dirty? {resource.session.dirty}")
                        print(f"            new? {resource.session.new}")
                        print(f"            deleted? {resource.session.deleted}")
                    orig = len(registered)
                    registered.extend(resource.session.dirty)
                    registered.extend(resource.session.new)
                    registered.extend(resource.session.deleted)
                    if len(registered) != orig:
                        print(f"      added {len(registered) - orig} objects")
                    else:
                        print("      no new objects added")
        return registered
