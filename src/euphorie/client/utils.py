"""
Utils
-----

Helper functions.
"""

from .. import MessageFactory as _
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from euphorie.client import model
from euphorie.content.utils import StripMarkup
from plone import api
from sqlalchemy import sql
from z3c.saconfig import Session
from zope.i18nmessageid import MessageFactory

import email.utils as emailutils
import logging
import random
import threading

locals = threading.local()
log = logging.getLogger(__name__)

pl_message = MessageFactory("plonelocales")
CONTENT_LANGUAGE_COOKIE = "CONTENT_LANGUAGE"


def setRequest(request):
    locals.request = request


def getRequest():
    return getattr(locals, "request", None)


def getSecret():
    try:
        site = api.portal.get()
    except api.exc.CannotGetPortalError:
        site = None
    return getattr(site, "euphorie_secret", "secret")


def randomString(length=16):
    """Return 32 bytes of random data.

    Only characters which do not require special escaping in HTML or
    URLs are generated.
    """
    safe_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-"
    return "".join(random.choice(safe_characters) for idx in range(length))


def get_translated_custom_risks_title(request):
    return api.portal.translate(_("label_custom_risks", default="Custom risks"))


def HasText(html):
    """Determine if a HTML fragment contains text."""
    if not html:
        return False
    text = StripMarkup(html).replace(" ", "").replace("&nbsp;", "")
    return bool(text)


def CreateEmailTo(sender_name, sender_email, recipient, subject, body):
    mail = MIMEMultipart("alternative")
    mail["From"] = emailutils.formataddr((sender_name, sender_email))
    mail["To"] = recipient
    mail["Subject"] = Header(subject.encode("utf-8"), "utf-8")
    mail["Date"] = emailutils.formatdate(localtime=True)
    mail.set_param("charset", "utf-8")
    if isinstance(body, str):
        mail.attach(MIMEText(body.encode("utf-8"), "plain", "utf-8"))
    else:
        mail.attach(MIMEText(body))

    return mail


def _getContentLanguageCookie(request):
    """Gets the preferred content language from a cookie.

    This mimics `getLanguageCookie` from `plone.i18n`.

    Don't use this directly.  Use `getContentLanguagePref` instead.
    """
    langCookie = request.cookies.get(CONTENT_LANGUAGE_COOKIE)
    if not langCookie:
        return None
    lt = api.portal.get_tool("portal_languages")
    if langCookie in lt.getSupportedLanguages():
        return langCookie
    # Bad cookie, throw it away.
    request.RESPONSE.expireCookie(CONTENT_LANGUAGE_COOKIE, path="/")
    return None


def getContentLanguagePref(request):
    """Gets the preferred content language.

    Get it from a cookie.  Fall back to the default language of the site.
    """
    res = _getContentLanguageCookie(request)
    if res is not None:
        return res
    return api.portal.get_registry_record("plone.default_language")


def _setContentLanguageCookie(lang=None, request=None):
    """Sets a cookie for overriding language content negotiation.

    This mimics `setLanguageCookie` from `plone.i18n`.

    Don't use this directly.  Use `setLanguage` instead.
    If `lang` is None or otherwise empty, expire the cookie.
    """
    if not lang:
        # At first I wanted to expire the cookie, if it was set.
        # But that would always expire the cookie when you view a country.
        return None
    lt = api.portal.get_tool("portal_languages")
    if lang not in lt.getSupportedLanguages():
        return None
    if lang != _getContentLanguageCookie(request):
        request.RESPONSE.setCookie(CONTENT_LANGUAGE_COOKIE, lang, path="/")
    return lang


def setLanguage(request, context=None, lang=None):
    """Switch Plone to prefer another language for content.

    If no language is given via the `lang` parameter the language is
    taken from a `language` request parameter. If a dialect was chosen
    but is not available the main language is used instead. If the main
    language is also unavailable switch back to English.

    Changed in version 19.2.2: this only affects content, NOT the UI.
    We no longer set the I18N_LANGUAGE cookie, but a new CONTENT_LANGUAGE
    cookie.
    Since this version, `context` is no longer required as parameter,
    as we don't use it.  We could warn about it, but let's not for now:
    we may need it in the future.
    """
    if lang is None:
        lang = request.form.get("language")
    if not lang:
        # Fall back to language neutral.
        _setContentLanguageCookie(lang=None, request=request)
        return

    lang = lang.lower()
    res = _setContentLanguageCookie(lang=lang, request=request)
    if res is None and "-" in lang:
        lang = lang.split("-")[0]
        res = _setContentLanguageCookie(lang=lang, request=request)
        if res is None:
            log.warning("Failed to switch language to %r", lang)


def remove_empty_modules(nodes):
    """Takes a list of modules and risks.

    Removes modules that don't have any risks in them.
    Modules with submodules (with risks) must however be kept.

    How it works:
    -------------
    Use the 'grow' method to create a tree datastructure that
    mirrors the actual layout of modules and risks.

    Then 'prune' it by removing all branches that end in modules.

    Lastly flatten the tree back into a list and use it to filter the
    original list.
    """
    tree = {}
    ids = []

    def grow(tree, nodes):
        for i in range(0, len(nodes)):
            node = nodes[i]
            inserted = False
            for k in tree.keys():
                if node.path.startswith(k[0]):
                    if tree[k]:
                        grow(tree[k], [node])
                    else:
                        tree[k] = {(node.path, node.type, node.id): {}}
                    inserted = True
                    break
            if not inserted:
                tree[(node.path, node.type, node.id)] = {}

    def prune(tree):
        for k in list(tree):
            if tree[k]:
                prune(tree[k])

            if not tree[k] and k[1] == "module":
                del tree[k]

    def flatten(tree):
        for k in tree.keys():
            ids.append(k[2])
            flatten(tree[k])

    grow(tree, nodes)
    prune(tree)
    flatten(tree)
    return [n for n in nodes if n.id in ids]


def get_unactioned_nodes(ls, filter_for_measures=False):
    """Takes a list of modules and risks and removes all risks that have been
    actioned (i.e has at least one valid action plan). Also remove all modules
    that have lost all their risks in the process.

    See https://syslab.com/proj/issues/2885
    """
    unactioned = []
    for n in ls:
        if n.type == "module":
            unactioned.append(n)

        elif n.type == "risk":
            action_plans = n.standard_measures + n.custom_measures
            if not action_plans:
                if filter_for_measures:
                    if not (n.in_place_standard + n.in_place_custom):
                        unactioned.append(n)
                else:
                    unactioned.append(n)
            else:
                # It's possible that there is an action plan object, but
                # that it's not yet fully populated
                if action_plans[0] is None or action_plans[0].action is None:
                    unactioned.append(n)

    return remove_empty_modules(unactioned)


def get_actioned_nodes(ls):
    """Takes a list of modules and risks and removes all risks that are *not*
    actioned (i.e does not have at least one valid action plan) Also remove all
    modules that have lost all their risks in the process.

    See https://syslab.com/proj/issues/2885
    """
    actioned = []
    for n in ls:
        if n.type == "module":
            actioned.append(n)

        if n.type == "risk":
            action_plans = n.standard_measures + n.custom_measures
            if len(action_plans):
                # It's possible that there is an action plan object, but
                # it's not yet fully populated
                plans = [p.action for p in action_plans]
                if plans[0] is not None:
                    actioned.append(n)

    return remove_empty_modules(actioned)


def get_unanswered_nodes(session):
    query = (
        Session()
        .query(model.SurveyTreeItem)
        .filter(
            sql.and_(
                model.SurveyTreeItem.session == session,
                sql.or_(
                    model.MODULE_WITH_UNANSWERED_RISKS_FILTER,
                    model.UNANSWERED_RISKS_FILTER,
                ),
                sql.not_(model.SKIPPED_PARENTS),
            )
        )
        .order_by(model.SurveyTreeItem.path)
    )
    return query.all()


def get_risk_not_present_nodes(session):
    query = (
        Session()
        .query(model.SurveyTreeItem)
        .filter(
            sql.and_(
                model.SurveyTreeItem.session == session,
                sql.or_(
                    model.SKIPPED_PARENTS,
                    model.MODULE_WITH_RISKS_NOT_PRESENT_FILTER,
                    model.RISK_NOT_PRESENT_FILTER,
                    model.SKIPPED_MODULE,
                ),
            )
        )
        .order_by(model.SurveyTreeItem.path)
    )
    return query.all()


def get_italian_risk_not_present_nodes(session):
    query = (
        Session()
        .query(model.SurveyTreeItem)
        .filter(
            sql.and_(
                model.SurveyTreeItem.session == session,
                sql.or_(
                    model.SKIPPED_PARENTS,
                    model.MODULE_WITH_RISKS_NOT_PRESENT_FILTER,
                    model.SKIPPED_MODULE,
                    model.UNANSWERED_RISKS_FILTER,
                ),
            )
        )
        .order_by(model.SurveyTreeItem.path)
    )
    return query.all()
