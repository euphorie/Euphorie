from .. import MessageFactory as _
from z3c.form.browser.password import PasswordWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IPasswordWidget
from z3c.form.interfaces import IValidator
from z3c.form.validator import SimpleFieldValidator
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementer_only
from zope.interface import Interface
from zope.schema.interfaces import IField
from zope.schema.interfaces import ValidationError


class PasswordComparisonError(ValidationError):
    __doc__ = _("Password doesn't compare with confirmation value")


class IPasswordWithConfirmationWidget(IPasswordWidget):
    """Password with confirmation widget."""


@implementer_only(IPasswordWithConfirmationWidget)
class PasswordWithConfirmationWidget(PasswordWidget):
    """Password with confirmation widget."""


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def PasswordWithConfirmationFieldWidget(field, request):
    """IFieldWidget factory for WysiwygWidget."""
    return FieldWidget(field, PasswordWithConfirmationWidget(request))


@adapter(Interface, Interface, Interface, Interface, IPasswordWithConfirmationWidget)
@implementer(IValidator)
class PasswordWithConfirmationValidator(SimpleFieldValidator):
    def validate(self, value):
        """Check that the password value is equl to the confirmation value.

        This has been inspired by p01.widget.password
        """
        if value and self.request.get(self.widget.name + ".confirm") != value:
            raise PasswordComparisonError()
        return super(self.__class__, self).validate(value)
