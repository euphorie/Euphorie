# -*- coding: utf-8 -*-
from .. import MessageFactory as _
from Acquisition import aq_parent
from plonetheme.nuplone import MessageFactory as NuPloneMessageFactory
from plonetheme.nuplone.utils import checkPermission
from zope.i18n import translate
from zope.i18nmessageid.message import Message
from zope.schema.interfaces import ITitledTokenizedTerm
import re


TAG = re.compile(u"<.*?>")
UNWANTED = re.compile(u"(\r|&#13;)")
WHITE = re.compile(' +')

REGION_NAMES = {
    "eu": _(u"European Union"),
}

CUSTOM_COUNTRY_NAMES = {
    # This are areas whose country codes have not stabilized enough
    # to have arrived in the Unicode consortiums translations,
    # or where we use and old/incorrect country code.
    "CS": _(u"Kosovo"),
    "ME": _(u"Montenegro"),
    "RS": _(u"Republic of Serbia"),
    # Political issue, Macedonia can't be called Macedonia...
    "MK": _(u"F.Y.R. Macedonia"),
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

    txt = TAG.sub(u" ", markup)
    return WHITE.sub(u" ", txt).strip()


def StripUnwanted(text):
    """Strip unwanted elements from a text fragment"""
    if not text:
        return u""

    return UNWANTED.sub(u"", text)


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
    getters = [REGION_NAMES.get, CUSTOM_COUNTRY_NAMES.get, names.get]
    for getter in getters:
        title = getter(id.upper())
        if title is not None:
            if isinstance(title, Message):
                title = translate(title, context=request)
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


class DragDropHelper(object):

    def sortable_explanation(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        # Special handling for Flemish, for which LANGUAGE is "nl-be". For
        # translating the date under plone locales, we reduce to generic "nl".
        # For the specific oira translation, we rewrite to "nl_BE"
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        return translate(NuPloneMessageFactory(
            u"Change order of items by dragging the handle",
            default=u"Change order of items by dragging the handle"),
            target_language=lang)
