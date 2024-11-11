"""
Dependency
----------

Special fields that allow us to make use of NuPlone's dependency engine also
for validating required fields.
A required field only needs to be validated against being empty if the
condition is met, that means, if the checkbox that it depends on is ticked.
"""

from euphorie.content.user import BaseValidator
from euphorie.htmllaundry.z3cform import HtmlText
from euphorie.htmllaundry.z3cform import IHtmlText
from plonetheme.nuplone.z3cform.directives import Dependency
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer
from z3c.form.browser.text import TextWidget
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IForm
from z3c.form.interfaces import ITextAreaWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.interfaces import IValidator
from z3c.form.widget import FieldWidget
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementer_only
from zope.interface import Interface
from zope.schema.interfaces import IFromUnicode


class ConditionalField:
    """Marker class for conditional fields.

    FIXME: this class is used to register a custom validator adapter
    for the copnditional text input and textarea fields.

    We should avoid using this mixin class and
    use a proper common interface instead.
    """


# Interfaces
class IConditionalTextLine(IFromUnicode):
    """A Text line that is only shown under certain conditions."""


class IConditionalHtmlText(IHtmlText):
    """HTML Text field that is only shown under certain conditions."""


class IConditionalTextWidget(ITextWidget):
    """Text widget that is only shown under certain conditions."""


class IConditionalHtmlTextWidget(ITextAreaWidget):
    """Text area widget that is only shown under certain conditions."""


# Fields
@implementer(IConditionalTextLine)
class ConditionalTextLine(schema.TextLine, ConditionalField):
    """A Text line that is only shown under certain conditions."""


@implementer(IConditionalHtmlText)
class ConditionalHtmlText(HtmlText, ConditionalField):
    """HTML Text field that is only shown under certain conditions."""


# Widgets
@implementer_only(IConditionalTextWidget)
class ConditionalTextWidget(TextWidget):
    """Text widget that is only shown under certain conditions."""

    klass = "conditional-text-widget"


@implementer_only(IConditionalHtmlTextWidget)
class ConditionalHtmlTextWidget(TextAreaWidget):
    """Text area widget that is only shown under certain conditions."""

    klass = "conditional-textarea-widget"


# Field widget factories
@adapter(IConditionalTextLine, INuPloneFormLayer)
@implementer(IFieldWidget)
def ConditionalTextFieldWidget(field, request):
    return FieldWidget(field, ConditionalTextWidget(request))


@adapter(IConditionalHtmlText, INuPloneFormLayer)
@implementer(IFieldWidget)
def ConditionalHtmlTextFieldWidget(field, request):
    return FieldWidget(field, ConditionalHtmlText(request))


# Validator
@implementer(IValidator)
@adapter(Interface, Interface, IForm, ConditionalField, Interface)
class ConditionalFieldValidator(BaseValidator):
    def validate(self, value):
        """Only validate for required if the condition for the field is met.

        If the field that our widget depends on is not checked, set the
        flag for ignoring validation for required.
        """
        widget = self.widget
        dependencies = getattr(self.widget.field, "_dependencies", [])
        dependencies = [dep for dep in dependencies if isinstance(dep, Dependency)]
        if len(dependencies):
            widgets = widget.__parent__
            for dep in dependencies:
                # We only care about "on" type dependencies
                if dep.op != "on":
                    continue
                d_widget = widgets[dep.field]
                d_value = self.request.get(d_widget.name)
                # The magic happens here: the flag is set on self.widget, but
                # this is not persisted. Then the usual validation method
                # of z3c.form.validation is called, with the updated widget.
                self.widget.ignoreRequiredOnValidation = not d_value

        return super().validate(value)
