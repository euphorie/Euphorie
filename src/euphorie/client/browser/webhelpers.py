# coding=utf-8
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from datetime import datetime
from euphorie import MessageFactory as _
from euphorie.client import config
from euphorie.client.client import IClient
from euphorie.client.cookie import setCookie
from euphorie.client.country import IClientCountry
from euphorie.client.interfaces import IItaly
from euphorie.client.model import get_current_account
from euphorie.client.sector import IClientSector
from euphorie.client.session import SESSION_COOKIE
from euphorie.client.session import SessionManager
from euphorie.client.utils import getSecret
from euphorie.content.survey import ISurvey
from euphorie.content.utils import StripMarkup
from euphorie.decorators import reify
from euphorie.ghost import PathGhost
from logging import getLogger
from os import path
from plone import api
from plone.i18n.normalizer import idnormalizer
from plone.memoize.instance import memoize
from plone.memoize.view import memoize_contextless
from plonetheme.nuplone.utils import isAnonymous
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from z3c.appconfig.utils import asBool
from ZODB.POSException import POSKeyError
from zope.browser.interfaces import IBrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18n import translate

import Globals


logger = getLogger(__name__)


# XXX should to to config (registry?)
NAME_TO_PHASE = {
    'start': 'preparation',
    'profile': 'preparation',
    'identification': 'identification',
    'customization': 'identification',
    'actionplan': 'actionplan',
    'report': 'report',
    'status': 'status',
    'help': 'help',
    'new-email': 'useraction',
    'account-settings': 'useraction',
    'account-delete': 'useraction',
    'update': 'preparation',
    'disclaimer': 'help',
    'terms-and-conditions': 'help',
    'training': 'training',
}


class WebHelpers(BrowserView):
    """Browser view with utility methods that can be used in templates.

    Several methods in this view assume that the current survey can be
    found as an attribute on the request. This is normally setup by the
    :py:class:`euphorie.client.survey.SurveyPublishTraverser` traverser.

    View name: @@webhelpers
    """
    sector = None
    SESSION_COOKIE = SESSION_COOKIE

    resources_name = "++resource++euphorie.resources"
    bundle_name = "bundle.js"
    bundle_name_min = "bundle.min.js"

    def __init__(self, context, request):
        super(WebHelpers, self).__init__(context, request)
        if self.anonymous:
            setattr(self.request, 'survey', self._tool)

    @property
    @memoize
    def _my_context(self):
        context = self.context
        if IBrowserView.providedBy(context):
            context = context.context
        return context

    @property
    @memoize
    def sector(self):
        for obj in aq_chain(aq_inner(self._my_context)):
            if IClientSector.providedBy(obj):
                return obj

    @property
    @memoize
    def debug_mode(self):
        return Globals.DevelopmentMode

    @property
    @memoize
    def _settings(self):
        appconfig = getUtility(IAppConfig)
        return appconfig.get('euphorie')

    @property
    @memoize
    def allow_social_sharing(self):
        return asBool(self._settings.get('allow_social_sharing', False))

    @property
    @memoize
    def allow_guest_accounts(self):
        return asBool(self._settings.get('allow_guest_accounts', False))

    @property
    @memoize
    def use_training_module(self):
        return asBool(self._settings.get('use_training_module', False))

    @property
    @memoize
    def use_publication_feature(self):
        return asBool(self._settings.get('use_publication_feature', False))

    @property
    @memoize
    def default_country(self):
        return self._settings.get('default_country', '')

    @property
    @memoize
    def _user(self):
        return getSecurityManager().getUser()

    @property
    @memoize
    def anonymous(self):
        return isAnonymous(self._user)

    @property
    @memoize
    def is_guest_account(self):
        account = getattr(self._user, 'account_type', None)
        return account == config.GUEST_ACCOUNT

    @property
    @memoize
    def session(self):
        return getattr(SessionManager, 'session', None)

    @property
    @memoize
    def guest_session_id(self):
        return self.is_guest_account and self.session_id or None

    @property
    @memoize
    def session_id(self):
        return getattr(self.session, 'id', '')

    @memoize
    def session_by_id(self, sessionid):
        return SessionManager.get_session_by_id(sessionid)

    @property
    @memoize
    def came_from(self):
        came_from = self.request.form.get("came_from")
        if not came_from:
            return aq_parent(self._my_context).absolute_url()
        if not isinstance(came_from, list):
            return came_from
        # If came_from is both in the querystring and the form data
        return came_from[0]

    @property
    @memoize
    def country_name(self):
        for obj in aq_chain(aq_inner(self._my_context)):
            if IClientCountry.providedBy(obj):
                return obj.Title()

    @property
    @memoize
    def sector_name(self):
        for obj in aq_chain(aq_inner(self._my_context)):
            if IClientSector.providedBy(obj):
                return obj.Title()

    @property
    @memoize
    def _tool(self):
        for obj in aq_chain(aq_inner(self._my_context)):
            if ISurvey.providedBy(obj):
                return obj

    @property
    @memoize
    def tool_name(self):
        obj = self._tool
        if not obj:
            return ''
        return obj.Title()

    @property
    @memoize
    def tool_description(self):
        obj = self._tool
        if not obj:
            return ''
        ploneview = self._my_context.restrictedTraverse('@@plone')
        return ploneview.cropText(StripMarkup(obj.introduction), 800)

    @property
    @memoize
    def language_code(self):
        lt = getToolByName(self._my_context, 'portal_languages')
        lang = lt.getPreferredLanguage()
        return lang

    def get_username(self):
        member = api.user.get_current()
        return member.getProperty('fullname') or member.getUserName()

    def get_webstats_js(self):
        return api.portal.get_registry_record('plone.webstats_js')

    def language_dict(self):
        site = getSite()
        ltool = getToolByName(site, 'portal_languages')
        return ltool.getAvailableLanguages()

    @property
    def macros(self):
        return self.index.macros

    def country(self):
        for obj in aq_chain(aq_inner(self._my_context)):
            if IClientCountry.providedBy(obj):
                return obj.id
        return None

    def logoMode(self):
        return 'alien' if 'alien' in self.extra_css else 'native'

    @reify
    def styles_override(self):
        css = ""
        if IItaly.providedBy(self.request):
            css = """
#steps .topics .legend li.answered.risk::before {
    background: purple;
}
#steps .topics .questions li.answered.risk a::before {
    background: purple;
}
"""
        return css

    @reify
    def extra_css(self):
        sector = self.sector
        if sector is None:
            return u''

        sector = aq_base(sector)
        parts = []

        main_background = getattr(sector, 'main_background_colour', None)
        main_foreground = getattr(sector, 'main_foreground_colour', None)
        support_background = getattr(sector, 'support_background_colour', None)
        support_foreground = getattr(sector, 'support_foreground_colour', None)
        if main_background and main_foreground and \
                support_background and support_foreground:
            parts.append('deCornae')
            parts.append(
                    'brightMainColour'
                    if sector.main_background_bright
                    else 'darkMainColour')
            parts.append(
                    'brightSupportColour'
                    if sector.support_background_bright
                    else 'darkSupportColour')

        if getattr(sector, 'logo', None) is not None:
            parts.append('alien')

        lt = getToolByName(self._my_context, 'portal_languages')
        lang = lt.getPreferredLanguage()
        parts.append('language-%s' % lang)

        return ' ' + ' '.join(parts)

    @reify
    def sector_title(self):
        """Return the title to use for the current sector. If the current
        context is not in a sector return the agency name instead.
        """
        sector = self.sector
        if sector is not None and \
                getattr(aq_base(sector), 'logo', None) is not None:
            return sector.Title()
        else:
            return _(
                'title_tool',
                default=u'OiRA - Online interactive Risk Assessment',
            )

    @reify
    def client_url(self):
        """Return the absolute URL for the client."""
        return self.request.client.absolute_url()

    @reify
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
        if base_url is not None and \
                aq_inner(self._my_context).absolute_url().startswith(base_url):
            return base_url
        base_url = self.country_url
        if base_url is not None:
            return base_url
        return self.client_url

        if self.anonymous:
            base_url = self.country_url
            if base_url is not None:
                return base_url
            return self.client_url
        return self._base_url()

    @reify
    def base_url(self):
        if self.anonymous:
            base_url = self.country_url
            if base_url is not None:
                return base_url
            return self.client_url
        return self._base_url()

    @reify
    def resources_url(self):
        return "{}/{}".format(
            self.client_url, self.resources_name)

    @reify
    def is_outside_of_survey(self):
        if self._base_url() != self.survey_url():
            return True
        if (
            self.request.get('ACTUAL_URL').split('/')[-1] ==
            self.survey_url().split('/')[-1]
        ):
            return True
        return False

    @reify
    def get_survey_title(self):
        survey = self._survey
        if not survey:
            return None
        if (
            getattr(self, 'session', None) and
            "/".join(survey.getPhysicalPath()).endswith(self.session.zodb_path)
        ):
            return self.session.title
        return survey.title

    def get_phase(self):
        head, tail = path.split(self.request.PATH_INFO)
        while tail:
            tail = tail.replace('@', '')
            if tail in NAME_TO_PHASE:
                return NAME_TO_PHASE[tail]
            head, tail = path.split(head)
        return ""

    @property
    def came_from_param(self):
        param = ''
        if self.came_from:
            survey_url = self.survey_url()
            if survey_url:
                param = 'came_from={0}'.format(survey_url)
            else:
                param = 'came_from={0}'.format(self.came_from)

        return param

    @reify
    def help_url(self):
        """Return the URL to the current online help page. If we are in a
        survey the help page will be located there. Otherwise the country
        will be used as parent."""
        return '%s/help' % self._base_url()

    @reify
    def about_url(self):
        """Return the URL to the current online about page. If we are in a
        survey the help page will be located there. Otherwise the country
        will be used as parent."""
        return '%s/about' % self._base_url()

    @reify
    def authenticated(self):
        """Check if the current user is authenticated."""
        user = getSecurityManager().getUser()
        return user is not None and user.getUserName() != 'Anonymous User'

    @reify
    def country_url(self):
        """Return the absolute URL for country page."""
        sector = self.sector
        if sector is not None:
            return aq_parent(sector).absolute_url()

        for parent in aq_chain(aq_inner(self._my_context)):
            if IClientCountry.providedBy(parent):
                return parent.absolute_url()

        return None

    @reify
    def session_overview_url(self):
        """Return the absolute URL for the session overview."""
        return self.country_url

    @reify
    def sector_url(self):
        """Return the URL for the current survey."""
        sector = self.sector
        if sector is None:
            return None
        return sector.absolute_url()

    @reify
    def _survey(self):
        survey = getattr(self.request, 'survey', None)
        if survey is not None:
            return survey

        if self.session is None:
            return None

        try:
            return self.request.client.restrictedTraverse(
                self.session.zodb_path.split('/'))
        except KeyError as e:
            # This can happen when a survey has been unpublished while the
            # current user still has it in his session.
            logger.error(e)
            return None

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
            url += '/%s' % phase
        return url

    @memoize
    def survey_zodb_path(self):
        """
            Construct zodb_path from current survey.
            Helper method, since I don't always trust self.session.zodb_path
        """
        elems = []
        obj = self._survey
        while not IClient.providedBy(obj):
            elems.append(obj.id)
            obj = aq_parent(obj)
        elems.reverse()
        return "/".join(elems)

    @reify
    def in_session(self):
        """Check if there is an active survey session."""
        return self._survey is not None

    @reify
    def appendix_documents(self):
        """Return a list of items to be shown in the appendix."""
        documents = api.portal.get().documents

        lt = getToolByName(self._my_context, 'portal_languages')
        lang = lt.getPreferredLanguage()
        if '-' in lang:
            languages = [lang, lang.split('-')[0]]
        else:
            languages = [lang]

        for lang in languages:
            docs = documents.get(lang, None)
            if docs is None:
                continue
            appendix = docs.get('appendix', None)
            if appendix is not None:
                break
        else:
            return []

        base_url = self._base_url()
        return [{'url': '%s/appendix/%s' % (base_url, page.id),
                 'title': page.Title()}
                for page in appendix.values()]

    @reify
    def is_iphone(self):
        """Check if the current request is from an iPhone or similar device
        (such as an iPod touch).
        """
        agent = self.request.get_header('User-Agent', '')
        return 'iPhone' in agent

    def months(self, length='wide'):
        calendar = self.request.locale.dates.calendars['gregorian']
        months = calendar.monthContexts['format'].months[length]
        return sorted(months.items())

    @reify
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
        lt = getToolByName(self._my_context, "portal_languages")
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
                title=StripMarkup(motd.description), text=motd.body,
                id='motd{0}{1}'.format(
                    motd.modification_date.strftime('%Y%m%d%H%M%S'),
                    now.strftime('%Y%m%d'))
            )
        return message

    def tool_notification(self):
        message = None
        obj = self._my_context
        if isinstance(obj, PathGhost):
            obj = self.context.aq_parent
        if ISurvey.providedBy(obj) and obj.hasNotification():
            now = datetime.now()
            message = dict(
                title=obj.tool_notification_title,
                text=obj.tool_notification_message,
                id='tool{}{}{}'.format(
                    obj.modification_date.strftime('%Y%m%d%H%M%S'),
                    now.strftime('%Y%m%d'),
                    ''.join(obj.getPhysicalPath()[2:])))
        return message

    @memoize
    def translang(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            elems = lang.split("-")
            lang = "{0}_{1}".format(elems[0], elems[1].upper())
        return lang

    def closetext(self):
        return translate(
            _(u"button_close", default=u"Close"),
            target_language=self.translang())

    def email_sharing_text(self):
        return translate(
            _(u"I wish to share the following with you"),
            target_language=self.translang())

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
        return getattr(self.session, 'group_id', '')

    @memoize_contextless
    def is_owner(self, session=None):
        ''' Check if the current user is the owner of the session
        '''
        if session is None:
            session = self.session
        if not session:
            return False
        return self.get_current_account() == session.account

    @memoize
    def can_view_session(self, session=None):
        account = self.get_current_account()
        if not account:
            return False
        if session is None:
            session = self.session
        if session is None and self.request.get('sessionid'):
            session = self.session_by_id(self.request.get('sessionid'))
        return (
            session in account.sessions or
            session in account.acquired_sessions
        )

    @memoize
    def can_edit_session(self, session=None):
        return self.can_view_session(session=session)

    @memoize
    def can_publish_session(self, session=None):
        return self.can_edit_session(session=session)

    @memoize
    def can_delete_session(self, session=None, sessionid=''):
        return self.can_edit_session(session=session)

    def resume(self, session):
        ''' Resume a session for the current user if he is allowed to
        '''
        if not self.can_view_session(session):
            raise ValueError('Can only resume session for current user.')

        self.request.other["euphorie.session"] = session
        setCookie(
            self.request.response,
            self.getSecret(),
            SESSION_COOKIE,
            session.id,
        )

    def as_md(self, text):
        """ Return a text with Carriage Returns formatted as a Markdown.
        """
        return u"\r\n".join([x for x in text.split('\r')])

    def show_logo(self):
        """ In plain Euphorie, the logo is always shown
        """
        return True

    def __call__(self):
        return self


class Appendix(WebHelpers):
    """ Browser View for showing the appendix with various links to
    copyright, license, etc.
    Since this is very client-specific, it gets its own template for easy
    customisation.

    """

    def __call__(self):
        return self


class Logo(WebHelpers):
    """ Browser View for showing the markup for the logo
    Since this is very client-specific, it gets its own template for easy
    customisation.

    """

    def __call__(self):
        return self


class UserMenu(WebHelpers):
    """
    View class for the User Menu

    """

    def __call__(self):
        return self.index()


class HelpMenu(WebHelpers):
    """
    View class for the User Menu

    """

    def __call__(self):
        return self.index()
