# coding=utf-8
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
from euphorie.client.model import Risk
from euphorie.client.model import Session
from euphorie.client.model import SurveySession
from euphorie.client.model import SurveyTreeItem
from euphorie.client.sector import IClientSector
from euphorie.client.update import wasSurveyUpdated
from euphorie.client.utils import getSecret
from euphorie.content.survey import ISurvey
from euphorie.content.utils import getRegionTitle
from euphorie.content.utils import StripMarkup
from euphorie.ghost import PathGhost
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
from plonetheme.nuplone.utils import isAnonymous
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from six.moves.urllib.parse import urlencode
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
    "status": "status",
    "help": "help",
    "new-email": "useraction",
    "account-settings": "useraction",
    "account-delete": "useraction",
    "update": "preparation",
    "disclaimer": "help",
    "terms-and-conditions": "help",
    "training": "training",
}


class WebHelpers(BrowserView):
    """Browser view with utility methods that can be used in templates.

    Several methods in this view assume that the current survey can be
    found as an attribute on the request. This is normally setup by the
    :py:class:`euphorie.client.survey.SurveyPublishTraverser` traverser.

    View name: @@webhelpers
    """

    certificates_path = "++resource++euphorie.resources/oira/certificates"
    media_path = "++resource++euphorie.resources/media"
    style_path = "++resource++euphorie.resources/oira/style"
    script_path = "++resource++euphorie.resources/oira/script"

    brand = "oira"

    css_path = "++resource++euphorie.resources/{brand}/style/all.css"
    css_path_min = "++resource++euphorie.resources/{brand}/style/all.css"

    js_name = "bundle.js"
    js_name_min = "bundle.min.js"

    favicon_path = "++resource++euphorie.resources/{brand}/favicon/apple-touch-icon.png"

    group_model = Group
    survey_session_model = SurveySession

    def to_decimal(self, value):
        """Transform value in to a decimal"""
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
    def use_involve_phase(self):
        return api.portal.get_registry_record(
            "euphorie.use_involve_phase", default=False
        )

    @property
    @memoize
    def use_training_module(self):
        return api.portal.get_registry_record(
            "euphorie.use_training_module", default=False
        )

    @property
    @memoize
    def use_publication_feature(self):
        return api.portal.get_registry_record(
            "euphorie.use_publication_feature", default=False
        )

    @property
    @memoize
    def use_clone_feature(self):
        return api.portal.get_registry_record(
            "euphorie.use_clone_feature", default=False
        )

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

    @property
    @memoize
    def show_completion_percentage(self):
        """Feature switch, can be overwritten in subclass"""
        return False

    @property
    @memoize
    def default_country(self):
        return api.portal.get_registry_record("euphorie.default_country", default=u"")

    @property
    @memoize
    def _user(self):
        return self.get_current_account()

    @property
    @memoize
    def anonymous(self):
        return isAnonymous(self._user)

    @property
    @memoize
    def is_guest_account(self):
        account = getattr(self._user, "account_type", None)
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
        """Utility method for views to check if a survey has been updated,
        and if so redirect the user to the update confirmation page is
        generated. The return value is `True` if an update is required and
        `False` otherwise."""
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

    def update_completion_percentage(self, session=None):
        if not session:
            session = self.traversed_session.session
        query = (
            Session.query(SurveyTreeItem)
            .filter(SurveyTreeItem.session_id == session.id)
            .filter(SurveyTreeItem.type == "module")
            .filter(SurveyTreeItem.skip_children == False)  # noqa: E712
        ).order_by(SurveyTreeItem.depth)
        total_risks = 0
        answered_risks = 0

        @memoize
        def recursive_skip_children(module):
            return module.skip_children or (
                module.parent and recursive_skip_children(module.parent)
            )

        for module in query:
            if not module.path:
                # XXX When does a module not have a path?
                continue
            if recursive_skip_children(module):
                continue
            total_risks_query = (
                Session.query(Risk)
                .filter(Risk.session_id == session.id)
                .filter(Risk.path.like(module.path + "%"))
                .filter(Risk.depth == module.depth + 1)
            )
            total_risks = total_risks + total_risks_query.count()
            answered_risks_query = total_risks_query.filter(
                Risk.identification != None  # noqa: E711
            )
            answered_risks = answered_risks + answered_risks_query.count()

        completion_percentage = (
            int(round((answered_risks * 1.0 / total_risks * 1.0) * 100.0))
            if total_risks
            else 0
        )
        session.completion_percentage = completion_percentage
        return completion_percentage

    def get_progress_indicator_title(self, completion_percentage=None):
        if completion_percentage is None and self.traversed_session is not None:
            completion_percentage = self.traversed_session.session.completion_percentage
        title = _(
            "progress_indicator_title",
            default=u"${completion_percentage}% Complete",
            mapping={"completion_percentage": completion_percentage or 0},
        )
        return api.portal.translate(title)

    @property
    @memoize
    def came_from(self):
        came_from = self.request.form.get("came_from")
        if not came_from:
            return aq_parent(self.context).absolute_url()
        if not isinstance(came_from, list):
            return came_from
        # If came_from is both in the querystring and the form data
        return came_from[0]

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
        """Return the country id that is present in the path. Fall back to the
        default_country"""
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
    def getNameForLanguageCode(self, langCode):
        lang_util = getUtility(ILanguageUtility)
        info = lang_util.getAvailableLanguageInformation().get(langCode, None)
        if info is not None:
            return info.get("native", info.get("name", None))
        return None

    @memoize
    def getTranslatedCountryName(self, country_id):
        return getRegionTitle(self.request, country_id)

    @property
    @forever.memoize
    def available_help_languages(self):
        exclude = set(["illustrations"])
        return set(resource_listdir("euphorie.client", "resources/oira/help")) - exclude

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
        """XXX it would be better to write this country id, consider deprecating this"""
        obj = self.country_obj
        if not obj:
            return ""
        return obj.id

    def logoMode(self):
        return "alien" if "alien" in self.extra_css else "native"

    @property
    @memoize
    def extra_css(self):
        sector = self.sector
        if sector is None:
            return u""

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
        """Return the title to use for the current sector. If the current
        context is not in a sector return the agency name instead.
        """
        sector = self.sector
        if sector is not None and getattr(aq_base(sector), "logo", None) is not None:
            return sector.Title()
        else:
            return _(
                "title_tool",
                default=u"OiRA - Online interactive Risk Assessment",
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
        """Return the country URL, but fall back to the client URL in case
        the country URL is None.
        Relevant in tests only, as far as I can see"""
        return self.country_url or self.client_url

    def _base_url(self):
        """Return a base URL to be used for non-survey specific pages.
        If we are in a survey the help page will be located there. Otherwise
        the country will be used as parent.
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
        return "{}/{}".format(self.client_url, self.certificates_path)

    @property
    @memoize
    def media_url(self):
        return "{}/{}".format(self.client_url, self.media_path)

    @property
    @memoize
    def style_url(self):
        return "{}/{}".format(self.client_url, self.style_path)

    @property
    @memoize
    def css_url(self):
        return "{}/{}?t={}".format(
            self.client_url,
            self.css_path.format(brand=self.brand)
            if not self.debug_mode
            else self.css_path_min.format(brand=self.brand),
            self.resources_timestamp,
        )

    @property
    @memoize
    def js_url(self):
        return "{}/{}/{}?t={}".format(
            self.client_url,
            self.script_path,
            self.js_name if not self.debug_mode else self.js_name_min,
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

    def get_dashboard_tab(self):
        head, tail = path.split(self.request.PATH_INFO)
        if tail in ["surveys", "assessments"]:
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
        """Return the URL to the current online help page. If we are in a
        survey the help page will be located there. Otherwise the country
        will be used as parent."""
        return "%s/help" % self._base_url()

    @property
    @memoize
    def about_url(self):
        """Return the URL to the current online about page. If we are in a
        survey the help page will be located there. Otherwise the country
        will be used as parent."""
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

    @memoize
    def survey_url(self, phase=None):
        """Return the URL for the curreny survey.

        If a phase is specified the URL for the first page of that
        phase is returned.
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
        """
        Construct zodb_path from current survey.
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
    def in_session(self):
        """Check if there is an active survey session."""
        return self._survey is not None

    def is_initialised_session(self, session):
        """
        A session without children has not passed the Identification phase yet
        """
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
            {"url": "%s/appendix/%s" % (base_url, page.id), "title": page.Title()}
            for page in appendix.values()
        ]

    @property
    @memoize
    def is_iphone(self):
        """Check if the current request is from an iPhone or similar device
        (such as an iPod touch).
        """
        agent = self.request.get_header("User-Agent", "")
        return "iPhone" in agent

    def months(self, length="wide"):
        calendar = self.request.locale.dates.calendars["gregorian"]
        months = calendar.monthContexts["format"].months[length]
        return sorted(months.items())

    def timezoned_date(self, mydate=None):
        if mydate is None:
            return None
        utc = tz.gettz(self.server_timezone)
        return mydate.replace(tzinfo=utc)

    @property
    @memoize
    def get_sector_logo(self):
        sector = self.sector
        if sector is None:
            return None
        images = getMultiAdapter((sector, self.request), name="images")
        try:
            return images.scale("logo", height=100, direction="up") or None
        except POSKeyError:
            return None

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
                id="motd{0}{1}".format(
                    motd.modification_date.strftime("%Y%m%d%H%M%S"),
                    now.strftime("%Y%m%d"),
                ),
            )
        return message

    def tool_notification(self):
        message = None
        obj = self._survey
        if isinstance(obj, PathGhost):
            obj = self.context.aq_parent
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
        return api.portal.translate(_(u"button_close", default=u"Close"))

    def email_sharing_text(self):
        return api.portal.translate(_(u"I wish to share the following with you"))

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
        return session in account.sessions or session in account.acquired_sessions

    @property
    @memoize
    def can_edit_session(self):
        return self.can_view_session and not self.traversed_session.session.is_archived

    @property
    @memoize
    def can_publish_session(self):
        return self.can_edit_session

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
        """Check if the current user is the owner of the session"""
        session = self.traversed_session.session
        return self.get_current_account() == session.account

    @property
    @memoize
    def can_duplicate_session(self):
        return self.use_clone_feature

    def resume(self, session):
        """Resume a session for the current user if he is allowed to"""
        raise Exception("Obsolete, we traverse to sessions now")

    def as_md(self, text):
        """Return a text with Carriage Returns formatted as a Markdown."""
        return u"\r\n".join([x for x in text.split("\r")])

    def show_logo(self):
        """In plain Euphorie, the logo is always shown"""
        return True

    @property
    @memoize
    def portal_transforms(self):
        return api.portal.get_tool("portal_transforms")

    def get_safe_html(self, text):
        data = self.portal_transforms.convertTo(
            "text/x-html-safe", text, mimetype="text/html"
        )
        return data.getData()

    @property
    @memoize
    def custom_js(self):
        """Return custom JavaScript where necessary"""
        return ""

    @memoize_contextless
    def date_picker_i18n_json(self):
        """Taken from:
        https://github.com/ploneintranet/ploneintranet/blob/master/src/ploneintranet/layout/browser/date_picker.py  # noqa: E501

        Use this like:
        <input class="pat-date-picker"
               ...
               data-pat-date-picker="...; i18n: ${portal_url}/@@date-picker-i18n.json; ..."
               />
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
        """Method to return a query that looks for sessions

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
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
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
        return "; ".join(
            [
                "{key}: {value}".format(key=key, value=value)
                for key, value in messages.items()
            ]
        )

    def __call__(self):
        return self
