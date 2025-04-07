from .. import MessageFactory as _
from Acquisition import aq_inner
from Acquisition import aq_parent
from collections import OrderedDict
from io import StringIO
from plone import api
from plone.base.utils import safe_text
from plone.namedfile.interfaces import INamedBlobImage
from plonetheme.nuplone import MessageFactory as NuPloneMessageFactory
from plonetheme.nuplone.utils import checkPermission
from Products.Five import BrowserView
from zope.component import queryUtility
from zope.i18nmessageid.message import Message
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import csv
import re


csv.register_dialect(
    "bilbomatica",
    delimiter=",",
    doublequote=False,
    quoting=csv.QUOTE_ALL,
)

IMAGE_MIN_SIZE = (1000, 430)

TAG = re.compile("<.*?>")
UNWANTED = re.compile("(\r|&#13;|\xad)")
WHITE = re.compile(" +")

REGION_NAMES = {"eu": _("European Union"), "EU": _("European Union")}

CUSTOM_COUNTRY_NAMES = {
    # This are areas whose country codes have not stabilized enough
    # to have arrived in the Unicode consortiums translations,
    # or where we use and old/incorrect country code.
    "CS": _("Kosovo"),
    "ME": _("Montenegro"),
    "RS": _("Republic of Serbia"),
    # Political issue, Macedonia can't be called Macedonia...
    "MK": _("F.Y.R. Macedonia"),
}

# New concept: "Type" or "Flavour" of an OiRA tool. Apart from the "Classic"
# one, we add the type "With measures that are already in place".
link_add_measures = _(
    "no_translate_link_add_measures",
    default="<a class='add-clone' id='add-in-place-measure-button'>${text_add_measures}</a>",  # noqa: E501
    mapping={
        "text_add_measures": _(
            "text_add_measures",
            default="add all measures that have already been implemented",
        )
    },
)

TOOL_TYPES = OrderedDict(
    [
        (
            "classic",
            {
                "use_omega_risks": True,
                "title": _("Classic OiRA Tool with positive and negative statements."),
                "description": "",
                "intro_extra": "",
                "intro_extra_always_present": "",
                "button_add_extra": "",
                "button_add_extra_always_present": "",
                "button_remove_extra": "",
                "button_remove_extra_always_present": "",
                "placeholder_add_extra": "",
                "custom_placeholder_add_extra": "",
                "placeholder_add_extra_always_present": "",
                "intro_questions": "",
                "answer_yes": _("label_yes", default="Yes"),
                "answer_no": _("label_no", default="No"),
                "answer_yes_integrated_ap": _("label_yes_integrated_ap", default="Yes"),
                "answer_no_integrated_ap": _("label_no_integrated_ap", default="No"),
                "answer_na": _("label_not_applicable", default="Not applicable"),
                "custom_intro_extra": "",
                "custom_intro_questions": _(
                    "is_risk_acceptable",
                    default="Is this risk acceptable or under control?",
                ),
                "custom_button_add_extra": "",
            },
        ),
        (
            "existing_measures",
            {
                "use_omega_risks": True,
                "title": _(
                    'OiRA Tool where "Measures that are already in place" can be '
                    "defined."
                ),
                "description": "",
                "intro_extra": _(
                    "select_add_existing_measure",
                    default="Select or add any measures that are <strong>already "
                    "implemented</strong>.",
                ),
                "intro_extra_always_present": _(
                    "select_add_existing_measure",
                    default="Select or add any measures that are <strong>already "
                    "implemented</strong>.",
                ),
                "button_add_extra": _(
                    "button_add_existing_measure",
                    default="Add another measure implemented already",
                ),
                "button_add_extra_always_present": _(
                    "button_add_existing_measure",
                    default="Add another measure implemented already",
                ),
                "button_remove_extra": _(
                    "button_remove_existing_measure",
                    default="Remove this existing measure",
                ),
                "button_remove_extra_always_present": _(
                    "button_remove_existing_measure",
                    default="Remove this existing measure",
                ),
                "placeholder_add_extra": _(
                    "placeholder_new_existing",
                    default="Describe a measure that is already in place but not yet "
                    "listed here.",
                ),
                "custom_placeholder_add_extra": _(
                    "custom_placeholder_new_existing",
                    default="Describe a measure that is already in place.",
                ),
                "placeholder_add_extra_always_present": _(
                    "placeholder_new_existing",
                    default="Describe a measure that is already in place but not yet "
                    "listed here.",
                ),
                "intro_questions": _(
                    "implemented_measures_sufficient",
                    default="Are the measures that are already implemented sufficient?",  # noqa: E501
                ),
                "answer_yes": _(
                    "label_yes_sufficient",
                    default="Yes, the remaining risk is acceptable",
                ),
                "answer_no": _(
                    "label_not_sufficient", default="No, more measures are required"
                ),
                "answer_yes_integrated_ap": _(
                    "label_yes_sufficient",
                    default="Yes, the remaining risk is acceptable",
                ),
                "answer_no_integrated_ap": _(
                    "label_not_sufficient_integrated_ap",
                    default="No, more measures are required (to be added below)",  # noqa: E501
                ),
                "answer_na": _("label_not_applicable", default="Not applicable"),
                "custom_intro_extra": _(
                    "add_existing_measure",
                    default="Add any measures that are <strong>already implemented"
                    "</strong>.",
                ),
                "custom_intro_questions": _(
                    "implemented_measures_sufficient",
                    default="Are the measures that are already implemented sufficient?",  # noqa: E501
                ),
                "custom_button_add_extra": _(
                    "custom_button_add_existing_measure",
                    default="Add an already implemented measure",
                ),
            },
        ),
    ]
)


class IToolTypesInfo(Interface):
    def __call__():
        """Returns info (data-structure) about available tool types."""

    def types_existing_measures():
        """Returns all tool type names that use the "Measures already in place"
        feature."""

    def default_tool_type():
        """Returns the default type of tool, valid for this installation."""


@implementer(IToolTypesInfo)
class ToolTypesInfo:
    def __call__(self):
        return TOOL_TYPES

    @property
    def types_existing_measures(self):
        return ["existing_measures"]

    @property
    def default_tool_type(self):
        # The one defined as first option wins
        for key in TOOL_TYPES:
            return key


def get_tool_type_default():
    tti = queryUtility(IToolTypesInfo)
    if tti is not None:
        return tti.default_tool_type
    return "classic"


@implementer(IVocabularyFactory)
class ToolTypesVocabulary:
    def __call__(self, context):
        tti = queryUtility(IToolTypesInfo)
        terms = []
        if tti is not None:
            for key, val in tti().items():
                terms.append(SimpleTerm(key, title=val["title"]))
        return SimpleVocabulary(terms)


ToolTypesVocabularyFactory = ToolTypesVocabulary()


@implementer(IVocabularyFactory)
class MeasuresTextHandlingVocabulary:
    def __call__(self, context):
        terms = [
            SimpleTerm("full", title=_("Full (show Description and General Approach)")),
            SimpleTerm("simple", title=_("Simple (show only General Approach)")),
        ]
        return SimpleVocabulary(terms)


MeasuresTextHandlingVocabularyFactory = MeasuresTextHandlingVocabulary()


def ensure_image_size(value):
    if INamedBlobImage.providedBy(value):
        img_size = value.getImageSize()
        if img_size < IMAGE_MIN_SIZE:
            msg = f"Image “{value.filename}” is too small. "
            msg += "The minimum size is {} (width) x {} (height) pixels. ".format(
                *IMAGE_MIN_SIZE
            )
            msg += "Your image has a size of {} x {}.".format(*img_size)
            raise Invalid(msg)
    return True


def getSurvey(context):
    from euphorie.content.survey import ISurvey
    from euphorie.content.surveygroup import ISurveyGroup

    obj = context
    while obj and not ISurveyGroup.providedBy(obj):
        if ISurvey.providedBy(obj):
            return obj
        obj = aq_parent(obj)


def StripMarkup(markup):
    """Strip all markup from a HTML fragment."""
    if not markup:
        return ""

    txt = TAG.sub(" ", markup)
    return WHITE.sub(" ", txt).strip()


def StripUnwanted(text):
    """Strip unwanted elements from a text fragment."""
    if not text:
        return ""

    return UNWANTED.sub("", text)


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
                title = api.portal.translate(title)
            return title
    return default if default is not None else id


def summarizeCountries(container, request, current_country=None, permission=None):
    from euphorie.content.country import ICountry

    result = {}
    for country in container.values():
        if not ICountry.providedBy(country):
            continue

        if permission and not checkPermission(country, permission):
            continue

        country_type = getattr(country, "country_type", "country")
        if country_type != "region":
            country_type = "country"
        countries = result.setdefault(country_type, [])
        countries.append(
            {
                "id": country.id,
                "title": getRegionTitle(request, country.id, country.title),
                "url": country.absolute_url(),
                "current": (current_country == country.id),
            }
        )
    for ct in result.values():
        ct.sort(key=lambda c: c["title"])

    return result


class DragDropHelper:
    def sortable_explanation(self):
        return api.portal.translate(
            NuPloneMessageFactory(
                "Change order of items by dragging the handle",
                default="Change order of items by dragging the handle",
            ),
        )


class UserExport(BrowserView):
    def __call__(self):
        ret = "<html><body><h1>User Export</h1>"
        from euphorie.content.countrymanager import ICountryManager
        from euphorie.content.sector import ISector

        for id, country in aq_inner(self.context).objectItems():
            if len(id) != 2:
                continue
            managers = [
                item for item in country.values() if ICountryManager.providedBy(item)
            ]
            sectors = [item for item in country.values() if ISector.providedBy(item)]
            if len(managers) + len(sectors) == 0:
                continue
            ret += f"<h2>{country.title}</h2>"
            ret += "<h3>Country managers</h3><ul>"
            for manager in managers:
                ret += f"<li>{manager.title}, {manager.contact_email}</li>"
            ret += "</ul>"
            ret += "<h3>Sector managers</h3><dl>"
            for sector in sectors:
                ret += "<dt><strong>Sector: {}</strong></dt><dd>{}, {}</dd>".format(
                    sector.title, sector.contact_name, sector.contact_email
                )
            ret += "</dl>"

        ret += "</body></html>"
        return ret


class UserExportCSV(BrowserView):
    def __call__(self):
        from euphorie.content.countrymanager import ICountryManager
        from euphorie.content.sector import ISector

        fieldnames = ["fullname", "email"]
        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames, dialect="bilbomatica")
        writer.writerow({fn: fn for fn in fieldnames})
        for id, country in aq_inner(self.context).objectItems():
            if len(id) != 2:
                continue
            managers = [
                item for item in country.values() if ICountryManager.providedBy(item)
            ]
            sectors = [item for item in country.values() if ISector.providedBy(item)]
            for manager in managers:
                data = dict(
                    fullname=safe_text(manager.title).encode("utf-8"),
                    email=safe_text(manager.contact_email).encode("utf-8"),
                )
                writer.writerow(data)
            for sector in sectors:
                data = dict(
                    fullname=safe_text(sector.contact_name).encode("utf-8"),
                    email=safe_text(sector.contact_email).encode("utf-8"),
                )
                writer.writerow(data)
        csv_data = buffer.getvalue()
        buffer.close()
        response = self.request.RESPONSE
        response.setHeader(
            "Content-Disposition", "attachment; filename=oira_admin_users.csv"
        )
        response.setHeader("Content-Type", "text/csv;charset=utf-8")
        return csv_data


def parse_scaled_answers(contents):
    """Get values and answers from a scaled_answers risk field.

    You pass the contents of the field: a multi-line string.

    In most cases we will get something like this:

        very unsafe
        a bit unsafe
        safe enough
        quite safe
        very safe

    The first answer gets value 1, the second 2, etc.
    But we also support something like this, with the values encoded:

        very safe|5
        quite safe|4
        safe enough|3
        a bit unsafe|2
        very unsafe|1

    """
    if not contents:
        return []

    result = []
    lines = filter(None, (line.strip() for line in contents.splitlines()))

    for idx, line in enumerate(lines, start=1):
        if "|" not in line:
            text, value = line, str(idx)
        else:
            text, value = map(str.strip, line.rpartition("|")[::2])

        result.append(
            {
                "text": text,
                "value": value or str(idx),
            },
        )

    return result
