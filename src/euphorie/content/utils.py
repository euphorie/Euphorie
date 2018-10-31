# -*- coding: utf-8 -*-
from .. import MessageFactory as _
from Acquisition import aq_inner
from Acquisition import aq_parent
from collections import OrderedDict
from plonetheme.nuplone import MessageFactory as NuPloneMessageFactory
from plonetheme.nuplone.utils import checkPermission
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from StringIO import StringIO
from zope.component import queryUtility
from zope.i18n import translate
from zope.i18nmessageid.message import Message
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import csv
import re

csv.register_dialect(
    'bilbomatica', delimiter=',', doublequote=False,
    quoting=csv.QUOTE_ALL,
)

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

# New concept: "Type" or "Flavour" of an OiRA tool. Apart from the "Classic"
# one, we add the type "With measures that are already in place".
TOOL_TYPES = OrderedDict([
    ("classic", {
        "title": _(
            u"Classic OiRA Tool with positive and negative statements."),
        "description": "",
        "intro_extra": "",
        "button_add_extra": "",
        "button_remove_extra": "",
        "placeholder_add_extra": "",
        "intro_questions": "",
        "answer_yes": _("label_yes", default=u"Yes"),
        "answer_no": _("label_no", default=u"No"),
        "answer_na": _("label_not_applicable", default=u"Not applicable"),
    }),
    ("existing_measures", {
        "title": _(
            u'OiRA Tool where "Measures that are already in place" can be '
            u'defined.'),
        "description": "",
        "intro_extra": _(
            "select_add_existing_measure",
            default=u"Select or add any measures that are <strong>already in "
            u"place</strong>."),
        "button_add_extra": _(
            "button_add_existing_measure",
            default=u"Add a missing measure"),
        "button_remove_extra": _(
            "button_remove_existing_measure",
            default=u"Remove this existing measure"),
        "placeholder_add_extra": _(
            "placeholder_new_existing",
            default=u"Describe a measure that is already in place but not yet "
            u"listed here."),
        "intro_questions": _(
            "Are the measures that are selected above sufficient?"),
        "answer_yes": _(
            "label_yes_sufficient",
            default=u"Yes, the remaining risk is acceptable"),
        "answer_no": _(
            "label_not_sufficient",
            default=u"No, more measures are required"),
        "answer_na": _("label_not_applicable", default=u"Not applicable"),
    }),
])


class IToolTypesInfo(Interface):

    def __call__():
        """ Returns info (data-structure) about available tool types"""

    def types_existing_measures():
        """ Returns all tool type names that use the "Measures already in
        place" feature"""

    def default_tool_type():
        """ Returns the default type of tool, valid for this installation"""


@implementer(IToolTypesInfo)
class ToolTypesInfo(object):

    def __call__(self):
        return TOOL_TYPES

    @property
    def types_existing_measures(self):
        return ['existing_measures']

    @property
    def default_tool_type(self):
        # The one defined as first option wins
        return TOOL_TYPES.keys()[0]


def get_tool_type_default():
    tti = queryUtility(IToolTypesInfo)
    if tti is not None:
        return tti.default_tool_type
    return "classic"


@implementer(IVocabularyFactory)
class ToolTypesVocabulary(object):

    def __call__(self, context):
        tti = queryUtility(IToolTypesInfo)
        terms = []
        if tti is not None:
            for (key, val) in tti().items():
                terms.append(SimpleTerm(key, title=val['title']))
        return SimpleVocabulary(terms)

ToolTypesVocabularyFactory = ToolTypesVocabulary()


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


def summarizeCountries(
        container, request, current_country=None, permission=None):
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
                          "title": getRegionTitle(
                              request, country.id, country.title),
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


class UserExport(BrowserView):

    def __call__(self):
        ret = u"<html><body><h1>User Export</h1>"
        from euphorie.content.countrymanager import ICountryManager
        from euphorie.content.sector import ISector
        for id, country in aq_inner(self.context).objectItems():
            if len(id) != 2:
                continue
            managers = [
                item for item in country.values()
                if ICountryManager.providedBy(item)]
            sectors = [
                item for item in country.values()
                if ISector.providedBy(item)]
            if len(managers) + len(sectors) == 0:
                continue
            ret += u"<h2>{}</h2>".format(country.title)
            ret += u"<h3>Country managers</h3><ul>"
            for manager in managers:
                ret += u"<li>{}, {}</li>".format(
                    manager.title, manager.contact_email)
            ret += u"</ul>"
            ret += u"<h3>Sector managers</h3><dl>"
            for sector in sectors:
                ret += u"<dt><strong>Sector: {}</strong></dt><dd>{}, {}</dd>".format(  # noqa
                    sector.title, sector.contact_name, sector.contact_email)
            ret += u"</dl>"

        ret += u"</body></html>"
        return ret


class UserExportCSV(BrowserView):

    def __call__(self):
        from euphorie.content.countrymanager import ICountryManager
        from euphorie.content.sector import ISector
        fieldnames = ["fullname", "email"]
        buffer = StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=fieldnames,
            dialect='bilbomatica')
        writer.writerow(dict((fn, fn) for fn in fieldnames))
        for id, country in aq_inner(self.context).objectItems():
            if len(id) != 2:
                continue
            managers = [
                item for item in country.values()
                if ICountryManager.providedBy(item)]
            sectors = [
                item for item in country.values()
                if ISector.providedBy(item)]
            for manager in managers:
                data = dict(
                    fullname=safe_unicode(manager.title).encode('utf-8'),
                    email=safe_unicode(manager.contact_email).encode('utf-8'),
                )
                writer.writerow(data)
            for sector in sectors:
                data = dict(
                    fullname=safe_unicode(sector.contact_name).encode('utf-8'),
                    email=safe_unicode(sector.contact_email).encode('utf-8'),
                )
                writer.writerow(data)
        csv_data = buffer.getvalue()
        buffer.close()
        response = self.request.RESPONSE
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=oira_admin_users.csv",
        )
        response.setHeader(
            "Content-Type", 'text/csv;charset=utf-8')
        return csv_data
