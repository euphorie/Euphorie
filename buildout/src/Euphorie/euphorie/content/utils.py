import re
from zope.schema.interfaces import ITitledTokenizedTerm
from euphorie.content import MessageFactory as _

TAG = re.compile(u"<.*?>")

REGION_NAMES = {
        "eu": _(u"European Union"),
        }


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


def getRegionTitle(request, id, default=None):
    names=request.locale.displayNames.territories
    getters=[REGION_NAMES.get, names.get]
    for getter in getters:
        title=getter(id.upper())
        if title is not None:
            return title
    return default if default is not None else id

