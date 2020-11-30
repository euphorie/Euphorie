from Acquisition import aq_parent
from z3c.form.datamanager import AttributeField
from zope.security.checker import canAccess
from zope.security.checker import canWrite
from zope.security.checker import Proxy


class ParentAttributeField(AttributeField):
    parent_mapping = {}

    @property
    def adapted_context(self):
        return self.context

    def _name_and_context(self):
        name = self.field.__name__
        context = self.adapted_context
        if name in self.parent_mapping:
            context = aq_parent(context)
            name = self.parent_mapping[name]
        return (name, context)

    def get(self):
        (name, context) = self._name_and_context()
        return getattr(context, name)

    def set(self, value):
        if self.field.readonly:
            raise TypeError(
                "Can't set values on read-only fields "
                "(name=%s, class=%s.%s)"
                % (
                    self.field.__name__,
                    self.context.__class__.__module__,
                    self.context.__class__.__name__,
                )
            )
        (name, context) = self._name_and_context()
        setattr(context, name, value)

    def canAccess(self):
        (name, context) = self._name_and_context()
        if isinstance(context, Proxy):
            return canAccess(context, name)
        return True

    def canWrite(self):
        (name, context) = self._name_and_context()
        if isinstance(context, Proxy):
            return canWrite(context, name)
        return True
