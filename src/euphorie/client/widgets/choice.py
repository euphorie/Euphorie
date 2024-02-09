from functools import cached_property
from z3c.form.browser.select import SelectWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer


class EuphorieChoiceWidget(SelectWidget):
    """Select widget for z3c.form in the Euphorie context: better display
    mode."""

    @cached_property
    def title_value(self):
        if self.name in self.request.form:
            token = self.request.form[self.name]
            vocabulary = self.field.source(self.context)
            try:
                return vocabulary.getTermByToken(token).value
            except LookupError:
                return

        return getattr(self.context.session, self.field.__name__, None)

    def isSelected(self, term):
        return term.title == self.title_value


@implementer(IFieldWidget)
def EuphorieChoiceFieldWidget(field, request):
    """This is identicall to the equivalent in plone.app.z3cform but needs a
    customization to use the EuphorieSelectWidget class."""
    widget = FieldWidget(field, EuphorieChoiceWidget(request))
    return widget
