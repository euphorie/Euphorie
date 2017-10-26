"""
Utils
-----

Helper functions.
"""

from .. import MessageFactory as _
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
from datetime import datetime
from decorator import decorator
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from euphorie.client import config
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.interfaces import IItaly
from euphorie.client.sector import IClientSector
from euphorie.content.survey import ISurvey
from euphorie.content.utils import StripMarkup
from euphorie.decorators import reify
from euphorie.ghost import PathGhost
from five import grok
from json import dumps
from os import path
from PIL.ImageColor import getrgb
from plone import api
from plone.app.controlpanel.site import ISiteSchema
from plone.i18n.normalizer import idnormalizer
from plone.memoize.instance import memoize
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.utils import isAnonymous
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from ZODB.POSException import POSKeyError
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
import colorsys
import email.Utils as emailutils
import Globals
import logging
import random
import simplejson
import threading

locals = threading.local()
log = logging.getLogger(__name__)

grok.templatedir('templates')
pl_message = MessageFactory('plonelocales')


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
}


def setRequest(request):
    locals.request = request


def getRequest():
    return getattr(locals, 'request', None)


def getSecret():
    site = getUtility(ISiteRoot)
    return getattr(site, 'euphorie_secret', 'secret')


def randomString(length=16):
    """Return 32 bytes of random data. Only characters which do not require
    special escaping in HTML or URLs are generated."""

    safe_characters = 'abcdefghijklmnopqrstuvwxyz' \
                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                      '1234567890-'
    output = []
    append = output.append
    for i in xrange(length):
        append(random.choice(safe_characters))
    return ''.join(output)


@decorator
def jsonify(func, *args, **kwargs):
    request = getattr(args[0], "request")
    request.response.setHeader("Content-Type", "application/json")
    data = func(*args, **kwargs)
    return simplejson.dumps(data)


def get_translated_custom_risks_title(request):
    lang = getattr(request, 'LANGUAGE', 'en')
    if "-" in lang:
        elems = lang.split("-")
        lang = "{0}_{1}".format(elems[0], elems[1].upper())
    title = translate(_(
        'title_other_risks', default=u'Added risks (by you)'),
        target_language=lang)
    return title


class WebHelpers(grok.View):
    """Browser view with utility methods that can be used in templates.

    Several methods in this view assume that the current survey can be
    found as an attribute on the request. This is normally setup by the
    :py:class:`euphorie.client.survey.SurveyPublishTraverser` traverser.

    View name: @@webhelpers
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name('webhelpers')
    grok.template('webhelpers')

    sector = None

    def __init__(self, context, request):
        from euphorie.client.session import SessionManager
        from euphorie.client.country import IClientCountry
        super(WebHelpers, self).__init__(context, request)
        for obj in aq_chain(aq_inner(context)):
            if IClientSector.providedBy(obj):
                self.sector = obj
                break
        self.debug_mode = Globals.DevelopmentMode
        appconfig = getUtility(IAppConfig)
        settings = appconfig.get('euphorie')
        self.allow_social_sharing = settings.get('allow_social_sharing', False)
        self.allow_guest_accounts = settings.get('allow_guest_accounts', False)
        user = getSecurityManager().getUser()
        self.anonymous = isAnonymous(user)
        account = getattr(user, 'account_type', None)
        self.is_guest_account = account == config.GUEST_ACCOUNT
        self.guest_session_id = (
            self.is_guest_account and
            getattr(SessionManager, 'session', None) and
            SessionManager.session.id or None)
        self.session_id = (
            getattr(SessionManager, 'session', None) and
            SessionManager.session.id or '')

        came_from = self.request.form.get("came_from")
        if came_from:
            if isinstance(came_from, list):
                # If came_from is both in the querystring and the form data
                self.came_from = came_from[0]
            self.came_from = came_from
        else:
            self.came_from = aq_parent(context).absolute_url()

        self.country_name = ''
        self.sector_name = ''
        self.tool_name = ''
        self.tool_description = ''
        ploneview = self.context.restrictedTraverse('@@plone')
        for obj in aq_chain(aq_inner(self.context)):
            if ISurvey.providedBy(obj):
                self.tool_name = obj.Title()
                self.tool_description = ploneview.cropText(
                    StripMarkup(obj.introduction), 800)
                if self.anonymous:
                    setattr(self.request, 'survey', obj)
            if IClientSector.providedBy(obj):
                self.sector_name = obj.Title()
            if IClientCountry.providedBy(obj):
                self.country_name = obj.Title()
                break

    def get_username(self):
        member = api.user.get_current()
        return member.getProperty('fullname') or member.getUserName()

    def get_webstats_js(self):
        site = getSite()
        return ISiteSchema(site).webstats_js

    def language_dict(self):
        site = getSite()
        ltool = getToolByName(site, 'portal_languages')
        return ltool.getAvailableLanguages()

    @property
    def macros(self):
        return self.index.macros

    def country(self):
        from euphorie.client.country import IClientCountry
        for obj in aq_chain(aq_inner(self.context)):
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

        lt = getToolByName(self.context, 'portal_languages')
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
            return _('title_tool', default=u'OiRA - Online interactive Risk Assessment')

    @reify
    def client_url(self):
        """Return the absolute URL for the client."""
        return self.request.client.absolute_url()

    def _base_url(self):
        """Return a base URL to be used for non-survey specific pages.
        If we are in a survey the help page will be located there. Otherwise
        the country will be used as parent.
        """
        base_url = self.survey_url()
        if base_url is not None and \
                aq_inner(self.context).absolute_url().startswith(base_url):
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
    def is_outside_of_survey(self):
        return self._base_url() != self.survey_url()

    @reify
    def get_survey_title(self):
        survey = self._survey
        if not survey:
            return None
        if getattr(self, 'session', None):
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
        if self.came_from:
            survey_url = self.survey_url()
            if survey_url:
                param = 'came_from={0}'.format(survey_url)
            else:
                param = 'came_from={0}'.format(self.came_from)
        else:
            param = ''
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

        from euphorie.client.country import IClientCountry
        for parent in aq_chain(aq_inner(self.context)):
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
        from euphorie.client.session import SessionManager
        self.session = SessionManager.session
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
            log.error(e)
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

    @reify
    def in_session(self):
        """Check if there is an active survey session."""
        return self._survey is not None

    @reify
    def appendix(self):
        """Return a list of items to be shown in the appendix."""
        documents = getUtility(ISiteRoot).documents

        lt = getToolByName(self.context, 'portal_languages')
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
        lt = getToolByName(self.context, "portal_languages")
        lang = lt.getPreferredLanguage()
        if "-" in lang:
            return [lang, lang.split("-")[0], "en"]
        else:
            return [lang, "en"]

    def _findMOTD(self):
        documents = getUtility(ISiteRoot).documents

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
        obj = self.context
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


def HasText(html):
    """Determine if a HTML fragment contains text.
    """
    if not html:
        return False
    text = StripMarkup(html).replace(' ', '').replace('&nbsp;', '')
    return bool(text)


def CreateEmailTo(sender_name, sender_email, recipient, subject, body):
    mail = MIMEMultipart('alternative')
    mail['From'] = emailutils.formataddr((sender_name, sender_email))
    mail['To'] = recipient
    mail['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
    mail['Message-Id'] = emailutils.make_msgid()
    mail['Date'] = emailutils.formatdate(localtime=True)
    mail.set_param('charset', 'utf-8')
    if isinstance(body, unicode):
        mail.attach(MIMEText(body.encode('utf-8'), 'plain', 'utf-8'))
    else:
        mail.attach(MIMEText(body))

    return mail


def setLanguage(request, context, lang=None):
    """Switch Plone to another language. If no language is given via the
    `lang` parameter the language is taken from a `language`
    request parameter. If a dialect was chosen but is not available the main
    language is used instead. If the main language is also unavailable switch
    back to English.
    """
    if lang is None:
        lang = request.form.get('language')
    if not lang:
        return

    lang = lang.lower()
    lt = getToolByName(context, 'portal_languages')
    res = lt.setLanguageCookie(lang=lang)
    if res is None and '-' in lang:
        lang = lang.split('-')[0]
        res = lt.setLanguageCookie(lang=lang)
        if res is None:
            log.warn('Failed to switch language to %s', lang)
            lt.setLanguageCookie(lang='en')
            lang = 'en'

    # In addition to setting the cookie also update the PTS language.
    # This effectively switches Plone over to the new language without
    # requiring a new HTTP request.
    request['LANGUAGE'] = lang
    binding = request.get('LANGUAGE_TOOL', None)
    if binding is not None:
        binding.LANGUAGE = lang


def RelativePath(start, end):
    """Determine the relative path between two items in the ZODB."""
    if start is end:
        return ''

    start = start.getPhysicalPath()
    end = end.getPhysicalPath()
    while start and end and start[0] == end[0]:
        start = start[1:]
        end = end[1:]

    if start:
        return '%s/%s' % ('/'.join(len(start) * ['..']), '/'.join(end))
    else:
        return '/'.join(end)


def MatchColour(colour, low_l=0.2, high_l=0.65, s_factor=1):
    """Determine a colour that contrasts with a given colour. The resulting
    colour pair can be used as foreground and background, guaranteeing
    readable text.

    The match colour is determined by flipping the luminisoty to 10% or 90%,
    while keeping the hue and saturation stable. The only exception are
    yellowish colours, for those the luminosity is always set to 10%.
    """
    (r, g, b) = getrgb(colour)
    (h, l, s) = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    if 0.16 < h < 0.33:
        l = low_l
    elif l > 0.49:
        l = low_l
    else:
        l = high_l
    s *= s_factor
    (r, g, b) = colorsys.hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % (r * 255, g * 255, b * 255)


def IsBright(colour):
    """Check if a (RGB) colour is a bright colour."""
    (r, g, b) = getrgb(colour)
    (h, l, s) = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return l > 0.50


class I18nJSONView(grok.View):
    """ Provide the translated month and weekday names for pat-datepicker
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name('date-picker-i18n.json')

    def render(self):
        lang = getattr(self.request, 'LANGUAGE', 'en')
        if "-" in lang:
            lang = lang.split("-")[0]
        json = dumps({
            "months": [
                translate(
                    pl_message(month),
                    target_language=lang) for month in [
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
                translate(
                    pl_message(weekday),
                    target_language=lang) for weekday in [
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
                translate(
                    pl_message(weekday_abbr),
                    target_language=lang) for weekday_abbr in [
                        "weekday_sun_abbr",
                        "weekday_mon_abbr",
                        "weekday_tue_abbr",
                        "weekday_wed_abbr",
                        "weekday_thu_abbr",
                        "weekday_fri_abbr",
                        "weekday_sat_abbr",
                ]
            ],
        })

        return json


class DefaultIntroduction(grok.View):
    """
        Browser view that displays the default introduction text for a Suvey.
        It is used when the Survey does not define its own introduction
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name('default_introduction')
    grok.template('default_introduction')


class ContentDefaultIntroduction(grok.View):
    """
        Browser view that displays the default introduction text for a Suvey.
        It is used when the Survey does not define its own introduction
    """
    grok.context(Interface)
    grok.layer(NuPloneSkin)
    grok.name('default_introduction')
    grok.template('default_introduction')
