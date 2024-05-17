from euphorie.htmllaundry.utils import sanitize
from z3c.form.converter import FieldDataConverter
from z3c.form.interfaces import IWidget
from zope.component import adapter
from zope.interface import implementer
from zope.schema import Text
from zope.schema.interfaces import IText


class IHtmlText(IText):
    pass


@implementer(IHtmlText)
class HtmlText(Text):
    """A HTML field. This is similar to a standard Text field, but will
    sanitize all markup passed into it.
    """

    pass


@adapter(IHtmlText, IWidget)
class HtmlDataConverter(FieldDataConverter):
    """z3c.form data convertor for HTML forms. This convertor
    sanitizes all input, guaranteeing simple and valid markup
    as a result.
    """

    def toFieldValue(self, value):
        data = super().toFieldValue(value)
        if data:
            data = sanitize(data)
        return data
