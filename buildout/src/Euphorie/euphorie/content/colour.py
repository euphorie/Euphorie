import re
from zope.interface import implements
from zope import schema
from zope.schema.interfaces import ValidationError
from zope.schema.interfaces import IBytesLine
from euphorie.content import MessageFactory as _

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
            v="#%s" % v

        self.validate(v)

        return v


from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.interfaces import IFormLayer
from z3c.form import widget
from z3c.form.browser import text
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementsOnly

class IColourWidget(ITextWidget):
    """Colour type widget."""

class ColourWidget(text.TextWidget):
    """Colour type widget implementation."""
    implementsOnly(IColourWidget)
    klass = u"colour-widget"

@adapter(IColour, IFormLayer)
@implementer(IFieldWidget)
def ColourFieldWidget(field, request):
    return widget.FieldWidget(field, ColourWidget(request))


