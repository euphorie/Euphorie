import re
from zope.schema.interfaces import ITitledTokenizedTerm
from Acquisition import aq_parent
from plonetheme.nuplone.utils import checkPermission
from .. import MessageFactory as _


TAG = re.compile(u"<.*?>")

REGION_NAMES = {
        "eu": _(u"European Union"),
        
        # This are areas whose country codes have not stabilized enough
        # to have arrived in the Unicode consortiums translations,
        # or were we use and old/incorrect country code.
        "CS": _(u"Kosovo"),
        "ME": _(u"Montenegro"),
        "RS": _(u"Republic of Serbia"),
        }


def getSurvey(context):
    from euphorie.content.surveygroup import ISurveyGroup
    from euphorie.content.survey import ISurvey
    obj = context
    while obj and not ISurveyGroup.providedBy(obj):
        if ISurvey.providedBy(obj):
            return obj
        obj = aq_parent(obj)


def StripMarkup(markup):
    """Strip all markup from a HTML fragment."""
    if not markup:
        return u""

    return TAG.sub(u"", markup)


def getTermTitleByValue(field, token):
    try:
        term = field.vocabulary.getTerm(token)
    except LookupError:
        return token

    if ITitledTokenizedTerm.providedBy(term):
        return term.title
    else:
        return term.value


def getTermTitleByToken(field, token):
    try:
        term = field.vocabulary.getTermByToken(str(token))
    except LookupError:
        return token

    if ITitledTokenizedTerm.providedBy(term):
        return term.title
    else:
        return term.value


def getRegionTitle(request, id, default=None):
    names = request.locale.displayNames.territories
    getters = [REGION_NAMES.get, names.get]
    for getter in getters:
        title = getter(id.upper())
        if title is not None:
            return title
    return default if default is not None else id


def summarizeCountries(container, request, current_country=None,
        permission=None):
    from euphorie.content.country import ICountry
    result = {}
    for country in container.values():
        if not ICountry.providedBy(country):
            continue

        if permission and not checkPermission(country, permission):
            continue


        country_type = getattr(country, "country_type", "country")
        if country_type != 'region':
            country_type = 'country'
        countries = result.setdefault(country_type, [])
        countries.append({"id": country.id,
                          "title": getRegionTitle(request, country.id,
                                      country.title),
                          "url": country.absolute_url(),
                          "current": (current_country == country.id),
                          })
    for ct in result.values():
        ct.sort(key=lambda c: c["title"])

    return result
