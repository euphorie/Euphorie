import martian
from five import grok
from AccessControl import getSecurityManager
from euphorie.json import JsonView as BaseJsonView
from .interfaces import ICMSAPISkinLayer


class JsonView(BaseJsonView):
    martian.baseclass()
    grok.layer(ICMSAPISkinLayer)

    _security_manager = None

    def has_permission(self, permission):
        if self._security_manager is None:
            self._security_manager = getSecurityManager()
        return self._security_manager.checkPermission(permission, self.context)
