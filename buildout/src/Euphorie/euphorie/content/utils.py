import re
from zope.schema.interfaces import ITitledTokenizedTerm

TAG = re.compile(u"<.*?>")

def StripMarkup(markup):
    """Strip all markup from a HTML fragment."""
    if not markup:
        return u""

    return TAG.sub(u"", markup)


def getTermTitle(field, token):
    try:
        term=field.vocabulary.getTermByToken(str(token))
    except LookupError:
        return token

    if ITitledTokenizedTerm.providedBy(term):
        return term.title
    else:
        return term.value
