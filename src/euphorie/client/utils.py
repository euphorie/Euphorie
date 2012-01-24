import colorsys
import random
from PIL.ImageColor import getrgb
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Header import Header
import email.Utils as emailutils
import logging
import threading
import simplejson
from decorator import decorator
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from Acquisition import aq_parent
import Globals
from five import grok
from AccessControl import getSecurityManager
from zope.component import getUtility
from zope.interface import Interface
from plone.memoize.instance import memoize
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from euphorie.decorators import reify
from euphorie.content.utils import StripMarkup
from euphorie.client import MessageFactory as _
from euphorie.client.interfaces import IClientSkinLayer
from euphorie.client.sector import IClientSector

locals = threading.local()
log = logging.getLogger(__name__)

grok.templatedir('templates')


def setRequest(request):
    locals.request = request


def getRequest():
    return locals.request


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


class WebHelpers(grok.View):
    """Browser view with utility methods that can be used in templates.

    Several methods in this view assume that the current survey can be
    found as an attribute on the request. This is normally setup by the
    :py:class:`euphorie.client.survey.SurveyPublishTraverser` traverser.
    """
    grok.context(Interface)
    grok.layer(IClientSkinLayer)
    grok.name('webhelpers')
    grok.require('zope2.View')
    grok.template('webhelpers')

    sector = None

    def __init__(self, context, request):
        super(WebHelpers, self).__init__(context, request)
        for obj in aq_chain(aq_inner(context)):
            if IClientSector.providedBy(obj):
                self.sector = obj
                break
        self.debug_mode = Globals.DevelopmentMode

    @property
    def macros(self):
        return self.index.macros

    def country(self):
        from euphorie.client.country import IClientCountry
        for obj in aq_chain(aq_inner(self.context)):
            if IClientCountry.providedBy(obj):
                return obj.id
        else:
            return None

    def logoMode(self):
        return 'alien' if 'alien' in self.extra_css else 'native'

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
            return _('title_tool', default=u'OiRA')

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
        if base_url is not None:
            return base_url
        base_url = self.country_url
        if base_url is not None:
            return base_url
        return self.client_url

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
        survey = getattr(self.request, 'survey', None)
        if survey is not None:
            return survey

        session = SessionManager.session
        if session is None:
            return None

        try:
            return self.request.client.restrictedTraverse(
                    session.zodb_path.split('/'))
        except KeyError, e:
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
        if survey is None:
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
