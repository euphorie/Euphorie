import martian
from five import grok
from zExceptions import Unauthorized
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import Invalid
from zope.security.interfaces import IPermission
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from Products.CMFCore.permissions import ModifyPortalContent
from AccessControl import getSecurityManager
from euphorie.json import JsonView as BaseJsonView
from .interfaces import ICMSAPISkinLayer


def get_write_permissions(schema):
    """Collect all write permissions set via plone.directives.form on a schema.
    """
    # We have to walk over all base classes of the schema since
    # queryTaggedValue does not check base classes itself.
    todo = [schema]
    permissions = {}
    while todo:
        iface = todo.pop()
        if not issubclass(iface, Interface):
            continue
        permissions.update(iface.queryTaggedValue(WRITE_PERMISSIONS_KEY, {}))
        todo.extend(iface.__bases__)
    return permissions


class JsonView(BaseJsonView):
    martian.baseclass()
    grok.layer(ICMSAPISkinLayer)

    _security_manager = None

    def has_permission(self, permission, context=None):
        if context is None:
            context = self.context
        if self._security_manager is None:
            self._security_manager = getSecurityManager()
        return self._security_manager.checkPermission(permission, context)

    def update_object(self, attributes, schema, context=None, input=None):
        if context is None:
            context = self.context
        if input is None:
            input = self.input
        permissions = get_write_permissions(schema)
        try:
            for (field, attribute, getter) in attributes:
                value = getter(input, field)
                if value is None:
                    continue
                ztk_permission = permissions.get(attribute, None)
                if ztk_permission is not None:
                    permission = getUtility(IPermission, name=ztk_permission).title
                else:
                    permission = ModifyPortalContent
                if not self.has_permission(permission, context):
                    raise Unauthorized()
                schema[attribute].validate(value)
                setattr(context, attribute, value)
        except Invalid as e:
            raise ValueError(str(e))
