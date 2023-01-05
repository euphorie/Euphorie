from plone.protect.auto import ProtectTransform
from zope.sqlalchemy.datamanager import SessionDataManager


class EuphorieProtectTransform(ProtectTransform):
    def _registered_objects(self):
        registered = super()._registered_objects()
        app = self.request.PARENTS[-1]
        for name, conn in app._p_jar.connections.items():
            if name == "temporary":
                continue
            for resource in conn.transaction_manager.get()._resources:
                if isinstance(resource, SessionDataManager):
                    registered.extend(resource.session.dirty)
                    registered.extend(resource.session.new)
                    registered.extend(resource.session.deleted)
        return registered
