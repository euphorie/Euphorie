from plone.app.event.base import first_weekday
from plone.app.z3cform.widget import DateWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.pagetemplate.interfaces import IPageTemplate


class EuphorieDateWidget(DateWidget):
    """Date widget for z3c.form in the Euphorie context: better display
    mode."""

    def render(self):
        """Render widget.

        :returns: Widget's HTML.
        :rtype: string
        """
        if self.mode != "input":
            return super().render()
        template = getMultiAdapter(
            (self.context, self.request, self.form, self.field, self),
            IPageTemplate,
            name=self.mode,
        )
        return template(self)


@implementer(IFieldWidget)
def EuphorieDateFieldWidget(field, request):
    """This is identicall to the equivalent in plone.app.z3cform but needs a
    customization to use the EuphorieDateWidget class."""
    widget = FieldWidget(field, EuphorieDateWidget(request))
    widget.pattern_options.setdefault("date", {})
    try:
        widget.pattern_options["date"]["firstDay"] = first_weekday()
    except ComponentLookupError:
        pass
    return widget
