"""
Colour
------

Defines a colour field, with a validator.
"""

from .. import MessageFactory as _
from zope import schema
from zope.interface import implementer
from zope.schema.interfaces import IBytesLine
from zope.schema.interfaces import ValidationError

import re


VALID_COLOUR = re.compile(r"^#?[0-9a-f]+$")


class InvalidColour(ValidationError):
    __doc__ = _(u"The specified colour is not valid.")


class IColour(IBytesLine):
    """A field for a colour."""


@implementer(IColour)
class Colour(schema.BytesLine):
    """Colour selector field."""

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
