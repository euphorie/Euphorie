from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from datetime import datetime
from dateutil import tz
from decimal import Decimal
from euphorie import MessageFactory as _
from euphorie.client import config
from euphorie.client.adapters.session_traversal import ITraversedSurveySession
from euphorie.client.client import IClient
from euphorie.client.country import IClientCountry
from euphorie.client.model import get_current_account
from euphorie.client.model import Group
from euphorie.client.model import OrganisationMembership
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.client.sector import IClientSector
from euphorie.client.update import wasSurveyUpdated
from euphorie.client.utils import getSecret
from euphorie.content.survey import ISurvey
from euphorie.content.utils import getRegionTitle
from euphorie.content.utils import StripMarkup
from functools import cached_property
from json import dumps
from logging import getLogger
from os import path
from pkg_resources import resource_listdir
from plone import api
from plone.i18n.interfaces import ILanguageUtility
from plone.i18n.normalizer import idnormalizer
from plone.memoize import forever
from plone.memoize.instance import memoize
from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from plonetheme.nuplone.utils import isAnonymous
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISecuritySchema
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from sqlalchemy import and_
from urllib.parse import urlencode
from user_agents import parse
from ZODB.POSException import POSKeyError
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.deprecation import deprecate
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory


pl_message = MessageFactory("plonelocales")
pae_message = MessageFactory("plone.app.event")
logger = getLogger(__name__)


# XXX should to to config (registry?)
NAME_TO_PHASE = {
    "start": "preparation",
    "involve": "involve",
    "profile": "preparation",
    "identification": "identification",
    "customization": "identification",
    "actionplan": "actionplan",
    "report": "report",
    "consultancy": "consultancy",
    "consultants": "consultancy",
    "status": "status",
    "help": "help",
    "new-email": "useraction",
    "account-settings": "useraction",
    "account-delete": "useraction",
    "update": "preparation",
    "disclaimer": "help",
    "terms-and-conditions": "help",
    "training": "training",
    "email-reminder": "reminder",
}


class WebHelpers(BrowserView):
    """Browser view with utility methods that can be used in templates.

    Several methods in this view assume that the current survey can be
    found as an attribute on the request. This is normally setup by the
    :py:class:`euphorie.client.survey.SurveyPublishTraverser` traverser.

    View name: @@webhelpers
    """

    certificates_path = "++resource++euphorie.resources/assets/oira/certificates"
    media_path = "++resource++euphorie.resources/media"
    style_path = "++resource++euphorie.resources/assets/oira/style"
    script_path = "++resource++patternslib"

    brand = "oira"

    css_path = "++resource++euphorie.resources/assets/{brand}/style/all.css"
    css_path_min = "++resource++euphorie.resources/assets/{brand}/style/all.css"

    js_name = "bundle.min.js"

    favicon_path = (
        "++resource++euphorie.resources/assets/{brand}/favicon/apple-touch-icon.png"
    )

    group_model = Group
    hide_organisation_tab = False
    survey_session_model = SurveySession
    dashboard_tabs = ["surveys", "assessments", "certificates", "organisation"]

    navigation_tree_legend = [
        {"class": "unvisited", "title": _("Unvisited")},
        {"class": "postponed", "title": _("Postponed")},
        {"class": "answered", "title": _("Risk not present")},
        {"class": "answered risk", "title": _("Risk present")},
    ]

    # Inspection is meant for showing an edit-form in read-only/display mode.
    allow_inspecting_archived_sessions = False
    allow_inspecting_locked_sessions = False

    def to_decimal(self, value):
        """Transform value in to a decimal."""
        return Decimal(value)

    @property
    @memoize
    def resources_timestamp(self):
        return api.portal.get_registry_record(
            "euphorie.deployment.resources_timestamp", default=""
        )

    @property
    @memoize
    def server_timezone(self):
        return datetime.now(tz.tzlocal()).tzname()

    @property
    @memoize
    def sector(self):
        for obj in aq_chain(aq_inner(self.context)):
            if IClientSector.providedBy(obj):
                return obj

    @property
    @memoize
    def debug_mode(self):
        return api.env.debug_mode()

    @property
    @memoize
    def allow_social_sharing(self):
        return api.portal.get_registry_record(
            "euphorie.allow_social_sharing", default=False
        )

    @property
    @memoize
    def allow_guest_accounts(self):
        return api.portal.get_registry_record(
            "euphorie.allow_guest_accounts", default=False
        )

    @property
    @memoize
    def allow_self_registration(self):
        registry = getUtility(IRegistry)
        security_settings = registry.forInterface(ISecuritySchema, prefix="plone")
        return security_settings.enable_self_reg

    @property
    @memoize
    def use_involve_phase(self):
        return api.portal.get_registry_record(
            "euphorie.use_involve_phase", default=False
        )

    @property
    @memoize
    def use_consultancy_phase(self):
        return self.content_country_obj.enable_consultancy

    @property
    @memoize
    def use_training_module(self):
        globally_enabled = api.portal.get_registry_record(
            "euphorie.use_training_module", default=False
        )
        if not globally_enabled:
            return False
        country_enabled = self.content_country_obj.enable_web_training
        if not country_enabled:
            return False
        if self._survey is None:
            return True
        return self._survey.enable_web_training

    @property
    def display_training_module(self):
        if not self.use_training_module:
            return False
        traversed_session = self.traversed_session
        if traversed_session is None:
            return False

        training_slide = api.content.get_view(
            name="training_slide", context=self.context, request=self.request
        )
        if (
            training_slide.existing_measures_training
            or training_slide.planned_measures_training
        ):
            return True
        return False

    @property
    @memoize
    @deprecate(
        "Publication has been changed to locking. Deprecated in version 15.0.0.dev0"
    )
    def use_publication_feature(self):
        return api.portal.get_registry_record(
            "euphorie.use_locking_feature", default=False
        )

    @memoize
    @deprecate(
        "Publication has been changed to locking. Deprecated in version 15.0.0.dev0"
    )
    def use_publication_feature_for_session(self, session):
        # to be overwritten as needed
        return self.use_locking_feature

    @property
    @memoize
    def use_locking_feature(self):
        return api.portal.get_registry_record(
            "euphorie.use_locking_feature", default=False
        )

    @memoize
    def use_locking_feature_for_session(self, session):
        # to be overwritten as needed
        return self.use_locking_feature

    @property
    @memoize
    def use_archive_feature(self):
        return api.portal.get_registry_record(
            "euphorie.use_archive_feature", default=False
        )

    @property
    @memoize
    def use_help_section(self):
        return api.portal.get_registry_record("euphorie.use_help_section", default=True)

    # Feature switch, can be overwritten in subclass
    show_completion_percentage = False

    @property
    @memoize
    def show_certificates_tab(self):
        return self.use_training_module

    @property
    @memoize
    def default_country(self):
        return api.portal.get_registry_record("euphorie.default_country", default="")

    @property
    @memoize
    @deprecate("Use current_account instead. Deprecated in version 15.0.0.dev0")
    def _user(self):
        return self.current_account

    @property
    @memoize
    def current_account(self):
        return self.get_current_account()

    @property
    @memoize
    def anonymous(self):
        return isAnonymous(self.current_account)

    @property
    @memoize
    def is_guest_account(self):
        account = getattr(self.current_account, "account_type", None)
        return account == config.GUEST_ACCOUNT

    @property
    @memoize
    def session(self):
        raise Exception("Use the traversed session")

    @property
    @memoize
    def traversed_session(self):
        for obj in self.context.aq_chain:
            if ITraversedSurveySession.providedBy(obj):
                return obj

    def redirectOnSurveyUpdate(self):
        """Utility method for views to check if a survey has been updated, and
        if so redirect the user to the update confirmation page is generated.

        The return value is `True` if an update is required and `False`
        otherwise.
        """
        if not self.can_edit_session:
            return False
        traversed_session = self.traversed_session
        session = traversed_session.session
        survey = traversed_session.aq_parent
        if not wasSurveyUpdated(session, survey):
            return False
        self.request.response.redirect(
            "{session_url}/@@update?initial_view=1".format(
                session_url=traversed_session.absolute_url()
            )
        )
        return True

    @property
    @memoize
    def session_id(self):
        traversed_session = self.traversed_session
        return traversed_session.session.id if traversed_session else ""

    @memoize
    @deprecate(
        "Replace with session.completion_percentage "
        "or self.traversed_session.session.completion_percentage. "
        "Deprecated in version 14.1.4.dev0"
    )
    def update_completion_percentage(self, session=None):
        if not session:
            session = self.traversed_session.session
        return session.completion_percentage

    def get_progress_indicator_title(self, completion_percentage=None):
        if completion_percentage is None and self.traversed_session is not None:
            completion_percentage = self.traversed_session.session.completion_percentage
        title = _(
            "progress_indicator_title",
            default="${completion_percentage}% Complete",
            mapping={"completion_percentage": completion_percentage or 0},
        )
        return api.portal.translate(title)

    @memoize
    def get_came_from(self, default=None):
        came_from = self.request.form.get("came_from")
        if not came_from:
            return default
        if isinstance(came_from, list):
            # If came_from is both in the querystring and the form data
            came_from = came_from[0]
        put = getToolByName(self.context, "portal_url")
        if came_from and not put.isURLInPortal(came_from):
            return default
        return came_from

    @property
    @memoize
    def came_from(self):
        default = aq_parent(self.context).absolute_url()
        came_from = self.get_came_from(default=default)
        return came_from

    @property
    @memoize
    def country_obj(self):
        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                return obj

    @property
    @memoize
    def county_obj_via_parents(self):
        for obj in self.request.PARENTS:
            if IClientCountry.providedBy(obj):
                return obj

    @property
    @memoize
    def country_name(self):
        obj = self.country_obj
        if not obj:
            return ""
        return obj.Title()

    @property
    @memoize
    def content_country_obj(self):
        """Return the country object from the content area."""
        country_id = self.country_obj.id
        root = getUtility(ISiteRoot)
        country = getattr(root.sectors, country_id)
        return country

    @property
    @memoize
    def selected_country(self):
        """Return the country id that is present in the path.

        Fall back to the default_country
        """
        country = self.county_obj_via_parents
        if country:
            return country.getId()
        return self.default_country

    @property
    @memoize
    def sector_name(self):
        for obj in aq_chain(aq_inner(self.context)):
            if IClientSector.providedBy(obj):
                return obj.Title()
        return ""

    @property
    @memoize
    def tool_name(self):
        obj = self._survey
        if not obj:
            return ""
        return obj.Title()

    @property
    @memoize
    def tool_description(self):
        obj = self._survey
        if not obj:
            return ""
        ploneview = self.context.restrictedTraverse("@@plone")
        return ploneview.cropText(StripMarkup(obj.introduction), 800)

    @property
    @memoize
    def language_code(self):
        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        return lang

    @memoize_contextless
    def getNameForLanguageCode(self, langCode, native=True):
        lang_util = getUtility(ILanguageUtility)
        info = lang_util.getAvailableLanguageInformation().get(langCode, None)
        if info is not None:
            if native:
                return info.get("native", info.get("name", None))
            lang_names = self.request.locale.displayNames.languages
            name = lang_names.get(langCode, langCode)
            # Better show the (English) full name than only the language code
            if name == langCode:
                name = info.get("name")
            return name.capitalize()
        return None

    @memoize
    def getTranslatedCountryName(self, country_id):
        return getRegionTitle(self.request, country_id)

    @property
    @forever.memoize
    def available_help_languages(self):
        exclude = {"illustrations"}
        return (
            set(resource_listdir("plonestatic.euphorie", "resources/assets/oira/help"))
            - exclude
        )

    @property
    @memoize
    def help_language(self):
        lang = self.language_code
        # No country-specific Help texts are curently supported
        if lang.find("-"):
            lang = lang.split("-")[0]
        return lang if lang in self.available_help_languages else "en"

    def get_username(self):
        member = api.user.get_current()
        return member.getProperty("fullname") or member.getUserName()

    def get_webstats_js(self):
        return api.portal.get_registry_record("plone.webstats_js")

    def language_dict(self):
        site = getSite()
        ltool = getToolByName(site, "portal_languages")
        return ltool.getAvailableLanguages()

    @property
    def macros(self):
        return self.index.macros

    @property
    @memoize
    def country(self):
        """XXX it would be better to write this country id, consider
        deprecating this."""
        obj = self.country_obj
        if not obj:
            return ""
        return obj.id

    def logoMode(self):
        return "alien" if "alien" in self.extra_css else "native"

    def check_markup(self, text):
        if StripMarkup(text).strip():
            return text

    @property
    @memoize
    def extra_css(self):
        sector = self.sector
        if sector is None:
            return ""

        sector = aq_base(sector)
        parts = []

        if getattr(sector, "logo", None) is not None:
            parts.append("alien")

        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        parts.append("language-%s" % lang)

        return " " + " ".join(parts)

    @property
    @memoize
    def sector_title(self):
        """Return the title to use for the current sector.

        If the current context is not in a sector return the agency name
        instead.
        """
        sector = self.sector
        if sector is not None and getattr(aq_base(sector), "logo", None) is not None:
            return sector.Title()
        else:
            return _(
                "title_tool",
                default="OiRA - Online interactive Risk Assessment",
            )

    @property
    @memoize
    def client(self):
        if not self.context:
            return
        for obj in self.context.aq_chain:
            if IClient.providedBy(obj):
                return obj

    @property
    @memoize
    def client_url(self):
        """Return the absolute URL for the client."""
        return self.client.absolute_url() if self.client else "."

    @property
    @memoize
    def portal_url(self):
        return api.portal.get().absolute_url()

    @property
    @memoize
    def country_or_client_url(self):
        """Return the country URL, but fall back to the client URL in case the
        country URL is None.

        Relevant in tests only, as far as I can see
        """
        return self.country_url or self.client_url

    def _base_url(self):
        """Return a base URL to be used for non-survey specific pages.

        If we are in a survey the help page will be located there.
        Otherwise the country will be used as parent.
        """
        base_url = self.survey_url()
        if base_url is not None and aq_inner(self.context).absolute_url().startswith(
            base_url
        ):
            return base_url
        base_url = self.country_url
        if base_url is not None:
            return base_url
        return self.client_url

    @property
    @memoize
    def base_url(self):
        if self.anonymous:
            base_url = self.country_url
            if base_url is not None:
                return base_url
            return self.client_url
        return self._base_url()

    @property
    @memoize
    def certificates_url(self):
        return f"{self.client_url}/{self.certificates_path}"

    @property
    @memoize
    def media_url(self):
        return f"{self.client_url}/{self.media_path}"

    @property
    @memoize
    def style_url(self):
        return f"{self.client_url}/{self.style_path}"

    @property
    @memoize
    def css_url(self):
        return "{}/{}?t={}".format(
            self.client_url,
            (
                self.css_path.format(brand=self.brand)
                if not self.debug_mode
                else self.css_path_min.format(brand=self.brand)
            ),
            self.resources_timestamp,
        )

    @property
    @memoize
    def js_url(self):
        return "{}/{}/{}?t={}".format(
            self.client_url,
            self.script_path,
            self.js_name,
            self.resources_timestamp,
        )

    @property
    @memoize
    def favicon_url(self):
        return "{}/{}?t={}".format(
            self.client_url,
            self.favicon_path.format(brand=self.brand),
            self.resources_timestamp,
        )

    @property
    @memoize
    @deprecate(
        "Replace with  a check for `webhelpers.survey_url`, "
        "deprecated in version 11.1.2"
    )
    def is_outside_of_survey(self):
        if self._base_url() != self.survey_url():
            return True
        if (
            self.request.get("ACTUAL_URL").split("/")[-1]
            == self.survey_url().split("/")[-1]
        ):
            return True
        return False

    @property
    @memoize
    def get_survey_title(self):
        survey = self._survey
        if not survey:
            return None
        if getattr(self, "session", None) and "/".join(
            survey.getPhysicalPath()
        ).endswith(self.session.zodb_path):
            return self.session.title
        return survey.title

    def get_phase(self):
        head, tail = path.split(self.request.PATH_INFO)
        while tail:
            tail = tail.replace("@", "").split("_")[0]
            if tail in NAME_TO_PHASE:
                return NAME_TO_PHASE[tail]
            head, tail = path.split(head)
        return ""

    @cached_property
    def phase(self):
        return self.get_phase()

    def get_dashboard_tab(self):
        tail = path.split(self.request.PATH_INFO.rstrip("/"))[-1].lstrip("@@")
        if tail in self.dashboard_tabs:
            return tail
        return "dashboard"

    @property
    def came_from_param(self):
        if self.came_from:
            # If the tool has a notification message, we cannot allow to deeplink
            # into it, since the user might then miss the notificaton.
            if not self.tool_notification():
                return urlencode({"came_from": self.came_from})
            survey_url = self.survey_url()
            if survey_url:
                return urlencode({"came_from": survey_url})
        return ""

    @property
    @memoize
    def help_url(self):
        """Return the URL to the current online help page.

        If we are in a survey the help page will be located there.
        Otherwise the country will be used as parent.
        """
        return "%s/help" % self._base_url()

    @property
    @memoize
    def about_url(self):
        """Return the URL to the current online about page.

        If we are in a survey the help page will be located there.
        Otherwise the country will be used as parent.
        """
        return "%s/about" % self._base_url()

    @property
    @memoize
    def authenticated(self):
        """Check if the current user is authenticated."""
        user = getSecurityManager().getUser()
        return user is not None and user.getUserName() != "Anonymous User"

    @property
    @memoize
    def country_url(self):
        """Return the absolute URL for country page."""
        sector = self.sector
        if sector is not None:
            return aq_parent(sector).absolute_url()

        for parent in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(parent):
                return parent.absolute_url()

        return None

    @property
    @memoize
    def session_overview_url(self):
        """Return the absolute URL for the session overview."""
        return self.country_url

    @property
    @memoize
    def sector_url(self):
        """Return the URL for the current survey."""
        sector = self.sector
        if sector is None:
            return None
        return sector.absolute_url()

    @property
    @memoize
    def _survey(self):
        for parent in aq_chain(aq_inner(self.context)):
            if ISurvey.providedBy(parent):
                return parent

    @property
    @memoize
    def is_survey(self):
        """Return `True` if the webhelper's context is within a survey, `False`
        otherwise.
        """
        return bool(self._survey)

    @memoize
    def survey_url(self, phase=None):
        """Return the URL for the curreny survey.

        If a phase is specified the URL for the first page of that phase
        is returned.
        """
        survey = self._survey
        if not survey:
            return None

        url = survey.absolute_url()
        if phase is not None:
            url += "/@@%s" % phase
        return url

    @memoize
    def survey_zodb_path(self):
        """Construct zodb_path from current survey.

        Helper method, since I don't always trust self.session.zodb_path
        """
        elems = []
        obj = self._survey
        if not obj:
            return ""
        while not IClient.providedBy(obj):
            elems.append(obj.id)
            obj = aq_parent(obj)
        elems.reverse()
        return "/".join(elems)

    @property
    @memoize
    def integrated_action_plan(self):
        if not api.portal.get_registry_record(
            "euphorie.use_integrated_action_plan", default=False
        ):
            return False
        return getattr(self._survey, "integrated_action_plan", False)

    @property
    @memoize
    def use_action_plan_phase(self):
        return not self.integrated_action_plan

    @property
    @memoize
    def report_completion_threshold(self):
        survey = self._survey
        if not survey:
            return None
        return survey.report_completion_threshold or 0

    @property
    @memoize
    def use_email_reminder(self):
        survey = self._survey
        if not survey:
            return None
        return survey.enable_email_reminder

    @property
    @memoize
    def in_session(self):
        """Check if there is an active survey session."""
        return self._survey is not None

    def is_initialised_session(self, session):
        """A session without children has not passed the Identification phase
        yet."""
        return session.children().count()

    @property
    @memoize
    def appendix_documents(self):
        """Return a list of items to be shown in the appendix."""
        documents = api.portal.get().documents

        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        if "-" in lang:
            languages = [lang, lang.split("-")[0]]
        else:
            languages = [lang]

        for lang in languages:
            docs = documents.get(lang, None)
            if docs is None:
                continue
            appendix = docs.get("appendix", None)
            if appendix is not None:
                break
        else:
            return []

        base_url = self._base_url()
        return [
            {"url": f"{base_url}/appendix/{page.id}", "title": page.Title()}
            for page in appendix.values()
        ]

    @property
    @memoize
    def is_iphone(self):
        """Check if the current request is from an iPhone or similar device
        (such as an iPod touch)."""
        agent = self.request.get_header("User-Agent", "")
        return "iPhone" in agent

    def months(self, length="wide"):
        calendar = self.request.locale.dates.calendars["gregorian"]
        months = calendar.monthContexts["format"].months[length]
        return sorted(months.items())

    def timezoned_date(self, mydate=None):
        if mydate is None:
            return None
        # If the date already has a timezone, don't touch it
        if mydate.tzinfo is not None:
            return mydate
        local_tz = tz.gettz(self.server_timezone)
        return mydate.replace(tzinfo=local_tz)

    @property
    @memoize
    def get_sector_logo(self):
        sector = self.sector
        if sector is None:
            return None
        real_sector = sector._sector()
        images = getMultiAdapter((real_sector, self.request), name="images")
        try:
            return images.scale("logo", height=400, direction="up") or None
        except POSKeyError:
            return None

    @memoize
    def get_tool_image_url(self, survey=None):
        if not survey:
            survey = self._survey
        if getattr(survey, "image", None):
            return f"{survey.absolute_url()}/@@images/image/large"

    def messages(self):
        status = IStatusMessage(self.request)
        messages = status.show()
        for m in messages:
            m.id = idnormalizer.normalize(m.message)
        return messages

    def _getLanguages(self):
        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        if "-" in lang:
            return [lang, lang.split("-")[0], "en"]
        else:
            return [lang, "en"]

    def _findMOTD(self):
        documents = api.portal.get().documents

        motd = None
        for lang in self._getLanguages():
            docs = documents.get(lang, None)
            if docs is None:
                continue
            motd = docs.get("motd", None)
            if motd is not None:
                return motd

    def splash_message(self):
        message = None
        motd = self._findMOTD()
        if motd:
            now = datetime.now()
            message = dict(
                title=StripMarkup(motd.description),
                text=motd.body,
                id="motd{}{}".format(
                    motd.modification_date.strftime("%Y%m%d%H%M%S"),
                    now.strftime("%Y%m%d"),
                ),
            )
        return message

    def tool_notification(self):
        message = None
        obj = self._survey
        if ISurvey.providedBy(obj) and obj.hasNotification():
            now = datetime.now()
            message = dict(
                title=obj.tool_notification_title,
                text=obj.tool_notification_message,
                id="tool{}{}{}".format(
                    obj.modification_date.strftime("%Y%m%d%H%M%S"),
                    now.strftime("%Y%m%d"),
                    "".join(obj.getPhysicalPath()[2:]),
                ),
            )
        return message

    def closetext(self):
        return api.portal.translate(_("button_close", default="Close"))

    def email_sharing_text(self):
        return api.portal.translate(_("I wish to share the following with you"))

    def getSecret(self):
        return getSecret()

    @memoize_contextless
    def get_current_account(self):
        return get_current_account()

    @memoize_contextless
    def get_my_group_id(self):
        account = self.get_current_account()
        return account and account.group_id or ""

    @memoize
    def get_session_group_id(self):
        return getattr(self.session, "group_id", "")

    @property
    @memoize
    def can_view_session(self):
        account = self.get_current_account()
        if not account:
            return False
        session = self.traversed_session.session

        # Check if it is my session
        if session.account_id == account.id:
            return True

        # Check if it is a session of my organisation
        if (
            Session()
            .query(OrganisationMembership)
            .filter(
                and_(
                    OrganisationMembership.owner_id == session.account_id,
                    OrganisationMembership.member_id == account.id,
                )
            )
            .count()
        ):
            return True
        return session in account.acquired_sessions

    @property
    @memoize
    def can_edit_session(self):
        if not self.can_view_session:
            return False
        session = self.traversed_session.session
        if session.is_archived:
            return False
        if session.is_locked:
            return False
        return True

    @cached_property
    def can_inspect_session(self):
        """Can the user inspect the session?

        If a session is archived or locked, you cannot edit it.
        This used to mean that you cannot see the answers to risks, or indeed
        the entire 'identification' phase.  We may want to allow inspecting
        those parts without being able to edit them.  In the UI we could show
        the chosen answers for risks, without showing an editable form.
        """
        if not self.can_view_session:
            return False
        session = self.traversed_session.session
        if session.is_archived and not self.allow_inspecting_archived_sessions:
            return False
        if session.is_locked and not self.allow_inspecting_locked_sessions:
            return False
        return True

    @property
    @deprecate(
        "Publication has been changed to locking. Deprecated in version 15.0.0.dev0"
    )
    def can_publish_session(self):
        return self.can_lock_session

    @property
    @memoize
    def can_archive_session(self):
        if not self.use_archive_feature:
            return False
        if self.traversed_session.session.is_archived:
            return False
        return self.can_edit_session

    @property
    @memoize
    def can_delete_session(self):
        return self.can_edit_session

    @property
    @memoize
    def is_owner(self):
        """Check if the current user is the owner of the session."""
        session = self.traversed_session.session
        return self.get_current_account() == session.account

    @property
    @memoize
    def is_manager(self):
        """Check if the current user is a manager of the session."""
        account = self.get_current_account()
        if not account:
            return False
        session = self.traversed_session.session
        if (
            Session()
            .query(OrganisationMembership)
            .filter(
                and_(
                    OrganisationMembership.owner_id == session.account_id,
                    OrganisationMembership.member_id == account.id,
                    OrganisationMembership.member_role == "manager",
                )
            )
            .count()
        ):
            return True

    @property
    @memoize
    def can_lock_session(self):
        if not self.use_locking_feature:
            return False
        if self.is_owner:
            return True
        if self.is_manager:
            return True
        return False

    @property
    @memoize
    def can_unlock_session(self):
        return self.can_lock_session

    def resume(self, session):
        """Resume a session for the current user if he is allowed to."""
        raise Exception("Obsolete, we traverse to sessions now")

    def as_md(self, text):
        """Return a text with Carriage Returns formatted as a Markdown."""
        return "\r\n".join([x for x in text.split("\r")])

    def show_logo(self):
        """In plain Euphorie, the logo is always shown."""
        return True

    @property
    @memoize
    def portal_transforms(self):
        return api.portal.get_tool("portal_transforms")

    def get_safe_html(self, text):
        if not text:
            return ""
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()

    @property
    @memoize
    def custom_js(self):
        """Return custom JavaScript where necessary."""
        return ""

    @memoize_contextless
    def date_picker_i18n_json(self):
        """Taken from: https://github.com/ploneintranet/ploneintranet/blob/mast
        er/src/ploneintranet/layout/browser/date_picker.py  # noqa: E501.

        Use this like: <input class="pat-date-picker"        ... data-
        pat-date-picker="...; i18n: ${portal_url}/@@date-
        picker-i18n.json; ..."        />
        """
        json = dumps(
            {
                "previousMonth": api.portal.translate(pae_message("prev_month_link")),
                "nextMonth": api.portal.translate(pae_message("next_month_link")),
                "months": [
                    api.portal.translate(pl_message(month))
                    for month in [
                        "month_jan",
                        "month_feb",
                        "month_mar",
                        "month_apr",
                        "month_may",
                        "month_jun",
                        "month_jul",
                        "month_aug",
                        "month_sep",
                        "month_oct",
                        "month_nov",
                        "month_dec",
                    ]
                ],
                "weekdays": [
                    api.portal.translate(pl_message(weekday))
                    for weekday in [
                        "weekday_sun",
                        "weekday_mon",
                        "weekday_tue",
                        "weekday_wed",
                        "weekday_thu",
                        "weekday_fri",
                        "weekday_sat",
                    ]
                ],
                "weekdaysShort": [
                    api.portal.translate(pl_message(weekday_abbr))
                    for weekday_abbr in [
                        "weekday_sun_abbr",
                        "weekday_mon_abbr",
                        "weekday_tue_abbr",
                        "weekday_wed_abbr",
                        "weekday_thu_abbr",
                        "weekday_fri_abbr",
                        "weekday_sat_abbr",
                    ]
                ],
            }
        )
        return json

    def get_sessions_query(
        self,
        context=None,
        searchable_text=None,
        order_by=False,
        include_archived=False,
        filter_by_account=True,
        filter_by_group=False,
        table=None,
    ):
        """Method to return a query that looks for sessions.

        :param context: limits the sessions under this context
        :param searchable_text: filters on survey title
        :param order_by: is by default on survey title but you can pass
            None to disable ordering or a SQLAlchemy expression
        :param include_archived: unless explicitely set to a truish value,
            archived sessions are excluded
        :param filter_by_account: True means current account.
            A falsish value means do not filter.
            Otherwise try to interpret the user input:
            a string or an int means the account_id should be that value,
            an object account will be used to extract the account id,
            from an iterable we will try to extract the account ids
        :param filter_by_group: True means current account group,
            A falsish value means do not filter.
            Otherwise try to interpret the user input:
            a string or an int means the group_id should be that value,
            an object group will be used to extract the group id,
            and from an iterable we will try to extract the group ids
        :param table: if None use the default table in `cls.survey_session_model`
            otherwise use the one passed by the user
        """
        if table is None:
            table = self.survey_session_model
        query = Session.query(table)

        query = query.filter(table.get_context_filter(context or self.context))

        if filter_by_account:
            query = query.filter(table.get_account_filter(account=filter_by_account))
        if filter_by_group:
            query = query.filter(table.get_group_filter(group=filter_by_group))
        if not include_archived:
            query = query.filter(table.get_archived_filter())
        if searchable_text:
            query = query.filter(table.title.ilike(searchable_text))
        if order_by is None:
            pass  # Do not append any order_by
        elif order_by:
            query = query.order_by(order_by)
        else:
            query = query.order_by(table.modified.desc(), table.title)
        return query

    @memoize
    def is_outdated_browser(self):
        ua_string = self.request.get("HTTP_USER_AGENT", "")
        ua = parse(ua_string)
        return ua.browser.family == "IE"

    @property
    def pat_validation_messages(self):
        lang = getattr(self.request, "LANGUAGE", "en")
        if "-" in lang:
            elems = lang.split("-")
            lang = f"{elems[0]}_{elems[1].upper()}"
        messages = {
            "message-date": translate(
                _("error_validation_date", default="This value must be a valid date"),
                target_language=lang,
            ),
            "message-datetime": translate(
                _(
                    "error_validation_datetime",
                    default="This value must be a valid date and time",
                ),
                target_language=lang,
            ),
            "message-email": translate(
                _(
                    "error_validation_email",
                    default="This value must be a valid email address",
                ),
                target_language=lang,
            ),
            "message-number": translate(
                _("error_validation_number", default="This value must be a number"),
                target_language=lang,
            ),
            "message-required": translate(
                _("message_field_required", default="Please fill out this field."),
                target_language=lang,
            ),
        }
        return "; ".join([f"{key}: {value}" for key, value in messages.items()])

    @property
    @memoize
    def is_new_session(self):
        if self.request.get("new_session"):
            return True
        session = self.traversed_session.session
        return session.children().count() == 0

    def is_section_disabled(self, section):
        """Is the section disabled in this phase?

        See get_active_and_disabled_for_section for an explanation.

        This returns a boolean.
        """
        if section == "preparation":
            return self.phase == ""
        if section == "involve":
            return self.phase == "" or (
                self.phase == "preparation" and self.is_new_session
            )
        if section in ("identification", "actionplan"):
            return (
                self.phase in ("", "preparation") and self.is_new_session
            ) or not self.can_inspect_session
        if section in ("consultancy", "report", "training", "status", "reminder"):
            # These menu items should be active even if user cannot edit or inspect.
            return self.phase in ("", "preparation") and self.is_new_session

        # Default to not disable unknown sections.
        return False

    def get_active_and_disabled_for_section(self, section):
        """Is the section active or disabled in this phase?

        The navigation tree has sections: preparation, identification, etc.
        The phase (self.phase) is the current section you are viewing.
        The section argument that is passed in, is a section in the navigation
        tree.  This method answers two questions:

        * Is the section the currently active phase?
        * Should the section be disabled?

        What 'disabled' means is up to the frontend, but the expectation is
        that a disabled section is shown greyed out, and not clickable.

        This returns a tuple with two booleans: active and disabled.
        """
        active = section == self.phase
        disabled = self.is_section_disabled(section)
        return active, disabled

    @property
    @memoize
    def survey_tree_data(self):
        if self.anonymous:
            return []

        url = self.traversed_session.absolute_url()
        integrated_action_plan = self.integrated_action_plan

        data = []

        active, disabled = self.get_active_and_disabled_for_section("preparation")
        data.append(
            {
                "active": active,
                "disabled": disabled,
                "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                "id": "step-1",
                "name": "preparation",
                "href": f"{url}/@@start#content",
                "title": api.portal.translate(
                    _("label_preparation", default="Preparation")
                ),
                "has_tree": False,
            }
        )

        if self.use_involve_phase:
            active, disabled = self.get_active_and_disabled_for_section("involve")
            data.append(
                {
                    "active": active,
                    "disabled": disabled,
                    "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                    "id": "step-involve",
                    "name": "involve",
                    "href": f"{url}/@@involve#content",
                    "title": api.portal.translate(
                        _("label_involve", default="Involve")
                    ),
                    "has_tree": False,
                }
            )

        active, disabled = self.get_active_and_disabled_for_section("identification")
        title = ""
        if integrated_action_plan:
            title = api.portal.translate(_("label_assessment", "Assessment"))
        else:
            t1 = api.portal.translate(_("label_identification", "Identification"))
            t2 = api.portal.translate(_("label_evaluation", "Evaluation"))
            title = f"{t1} + {t2}"
        data.append(
            {
                "active": active,
                "disabled": disabled,
                "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                "id": "step-2",
                "name": "identification",
                "href": f"{url}/@@identification#content",
                "title": title,
                "has_tree": active,
            }
        )

        if self.use_action_plan_phase:
            # The tree for the action section uses the same structure as the
            # identification tree, with the only differences that only risks
            # and their parent modules are shown and that the entire tree is
            # expanded.
            active, disabled = self.get_active_and_disabled_for_section("actionplan")
            data.append(
                {
                    "active": active,
                    "disabled": disabled,
                    "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                    "id": "step-4",
                    "name": "action-plan",
                    "href": f"{url}/@@actionplan#content",
                    "title": api.portal.translate(
                        _("label_action_plan", default="Action Plan")
                    ),
                    "has_tree": active,
                }
            )

        if self.use_consultancy_phase:
            active, disabled = self.get_active_and_disabled_for_section("consultancy")
            data.append(
                {
                    "active": active,
                    "disabled": disabled,
                    "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                    "id": "step-consultancy",
                    "name": "consultancy",
                    "href": f"{url}/@@consultancy#content",
                    "title": api.portal.translate(
                        _("label_consultancy", default="Consultancy")
                    ),
                    "has_tree": False,
                }
            )

        # TODO: check if guest.
        active, disabled = self.get_active_and_disabled_for_section("report")
        data.append(
            {
                "active": active,
                "disabled": disabled,
                "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                "id": "step-5",
                "name": "report",
                "href": f"{url}/@@report#content",
                "title": api.portal.translate(_("label_report", default="Report")),
                "has_tree": False,
            }
        )

        if self.use_training_module:
            active, disabled = self.get_active_and_disabled_for_section("training")
            data.append(
                {
                    "active": active,
                    "disabled": disabled,
                    "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                    "id": "step-6",
                    "name": "training",
                    "href": f"{url}/@@training#content",
                    "title": api.portal.translate(
                        _("menu_training", default="Training")
                    ),
                    "has_tree": False,
                }
            )

        active, disabled = self.get_active_and_disabled_for_section("status")
        data.append(
            {
                "active": active,
                "disabled": disabled,
                "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                "id": "status",
                "name": "status",
                "href": f"{url}/@@status#content",
                "title": api.portal.translate(_("navigation_status", default="Status")),
                "has_tree": False,
            }
        )

        if self.use_email_reminder:
            active, disabled = self.get_active_and_disabled_for_section("reminder")
            data.append(
                {
                    "active": active,
                    "disabled": disabled,
                    "class": f'{"active" if active else ""} {"disabled" if disabled else ""}',  # noqa: E501
                    "id": "reminder",
                    "name": "involve",
                    "href": f"{url}/@@email-reminder#content",
                    "title": api.portal.translate(
                        _("navigation_email_reminder", default="Email reminder")
                    ),
                    "has_tree": False,
                }
            )

        return data

    def get_user_email(self, account=None):
        return account.email

    def get_user_fullname(self, account=None):
        return account.title

    def __call__(self):
        return self
