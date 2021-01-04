# coding=utf-8
from sqlalchemy.orm.instrumentation import ClassManager


def new_instance(self, state=None):
    # Original: instance = self.class_.__new__(self.class_)
    # leads to: TypeError: Acquirer.__new__(Account) is not safe, use object.__new__()
    # Apparently because our classes in client.model subclass Acquisition.Implicit
    instance = object.__new__(self.class_)
    if state is None:
        state = self._state_constructor(instance, self)
    self._state_setter(instance, state)
    return instance


ClassManager.new_instance = new_instance
