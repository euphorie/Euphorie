from plone.formwidget.namedfile.widget import NamedImageWidget
from z3c.form.widget import FieldWidget


class LogoWidget(NamedImageWidget):
    pass


def LogoFieldWidget(field, request):
    return FieldWidget(field, LogoWidget(request))
