"""
Dependency
----------

Special fields that allow us to make use of NuPlone's dependency engine also
for validating required fields.
A required field only needs to be validated against being empty if the
condition is met, that means, if the checkbox that it depends on is ticked.
"""

from euphorie.content.user import BaseValidator
from five import grok
from htmllaundry.z3cform import HtmlText
from plonetheme.nuplone.z3cform.directives import Dependency
from z3c.form.interfaces import IForm
from z3c.form.interfaces import IValidator
from zope import schema
from zope.interface import Interface


class ConditionalField(object):
    """Marker class for conditional fields"""


class ConditionalTextLine(schema.TextLine, ConditionalField):
    """ A Text line that is only shown under certain conditions """


class ConditionalHtmlText(HtmlText, ConditionalField):
    """ HTML Text field that is only shown under certain conditions """


class ConditionalFieldValidator(grok.MultiAdapter, BaseValidator):
    grok.implements(IValidator)
    grok.adapts(Interface, Interface, IForm, ConditionalField, Interface)

    def validate(self, value):
        """
        Only validate for required if the condition for the field is met.
        If the field that our widget depends on is not checked, set the
        flag for ignoring validation for required.
        """
        widget = self.widget
        dependencies = getattr(self.widget.field, "_dependencies", [])
        dependencies = [
            dep for dep in dependencies if isinstance(dep, Dependency)]
        if len(dependencies):
            widgets = widget.__parent__
            for dep in dependencies:
                # We only care about "on" type dependencies
                if dep.op != 'on':
                    continue
                d_widget = widgets[dep.field]
                d_value = self.request.get(d_widget.name)
                # The magic happens here: the flag is set on self.widget, but
                # this is not persisted. Then the usual validation method
                # of z3c.form.validation is called, with the updated widget.
                self.widget.ignoreRequiredOnValidation = not d_value

        return super(ConditionalFieldValidator, self).validate(value)
