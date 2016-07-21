"""
Colour
------

Defines a colour field, with a validator.
"""

import re
from zope.interface import implements
from zope import schema
from zope.schema.interfaces import ValidationError
from zope.schema.interfaces import IBytesLine
from .. import MessageFactory as _

VALID_COLOUR = re.compile(r"^#?[0-9a-f]+$")


class InvalidColour(ValidationError):
    __doc__ = _(u"The specified colour is not valid.")


class IColour(IBytesLine):
    """A field for a colour."""


class Colour(schema.BytesLine):
    """Colour selector field.
    """

    implements(IColour)

    _type = str

    def _validate(self, value):
        super(Colour, self)._validate(value)
        if not VALID_COLOUR.match(value):
            raise InvalidColour(value)

    def fromUnicode(self, u):
        v = str(u)
        if not v.startswith("#"):
            v = "#%s" % v

        self.validate(v)

        return v
