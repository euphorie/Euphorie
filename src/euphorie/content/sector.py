"""
Sector
======

A sector is a national organisation for a specific type of industry. The
sector content type is a minimal Dexterity item type, using a custom view
template.

Each sector is also a user. This is implemented via the `membrane`
framework.

.. _membrane: http://pypi.python.org/pypi/Products.membrane
"""

from .. import MessageFactory as _
from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from borg.localrole.interfaces import ILocalRoleProvider
from euphorie.content.behaviour.dirtytree import isDirty
from euphorie.content.survey import ISurvey
from euphorie.content.surveygroup import ISurveyGroup
from euphorie.content.user import IUser
from euphorie.content.user import UserProvider
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.directives import dexterity
from plone.directives import form
from plone.indexer import indexer
from plone.namedfile import field as filefield
from plone.uuid.interfaces import IAttributeUUID
from plonetheme.nuplone.skin import actions
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.utils import getPortal
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.Permissions import AccessPreviousVersions
from Products.statusmessages.interfaces import IStatusMessage
from z3c.appconfig.interfaces import IAppConfig
from zope import schema
from zope.component import getUtility
from zope.interface import implements

import datetime
import logging
import zExceptions


log = logging.getLogger(__name__)
grok.templatedir("templates")


class ISector(form.Schema, IUser, IBasic):
    """Sector object.

    A sector is a national organisation for a specific type of
    industry.
    """

    form.order_before(title="*")
    dexterity.write_permission(title="euphorie.content.ManageCountry")

    form.order_after(login="title")
    dexterity.write_permission(login="euphorie.content.ManageCountry")

    form.order_before(password="description")

    form.order_after(locked="password")
    dexterity.write_permission(locked="euphorie.content.ManageCountry")

    contact_name = schema.TextLine(
            title=_("label_contact_name", default=u"Contact name"),
            required=True)

    form.order_after(contact_email="contact_name")

    logo = filefield.NamedBlobImage(
            title=_("label_logo", default=u"Logo"),
            description=_("help_image_upload",
                default=u"Upload an image. Make sure your image is of format "
                        u"png, jpg or gif and does not contain any special "
                        u"characters."),
            required=False)


class Sector(dexterity.Container):
    """A sector of industry.

    A sector also acts as a user account in the system, using the membrane
    framework.
    """
    portal_type = "euphorie.clientsector"
    implements(ISector, INavigationRoot, IAttributeUUID)

    locked = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return op


@indexer(ISector)
def SearchableTextIndexer(obj):
    return " ".join([obj.title,
                     obj.description,
                     obj.contact_name or u"",
                     obj.contact_email or u""])


class SectorLocalRoleProvider(grok.Adapter):
    """`borg.localrole` provider for :obj:`ISector` instances.

    This local role provider gives the sector user itself the
    `Sector` local role.
    """
    grok.context(ISector)
    grok.implements(ILocalRoleProvider)
    grok.name("euphorie.sector")

    def getRoles(self, principal_id):
        mt = getToolByName(self.context, "membrane_tool")
        user = mt.getUserObject(user_id=principal_id, brain=True)
        if user is None:
            return ()

        user = user._unrestrictedGetObject()
        if ISector.providedBy(user) and aq_base(user) is aq_base(self.context):
            return ("Sector",)
        return ()

    def getAllRoles(self):
        info = UserProvider(self.context)
        return [(info.getUserId(), ("Sector",))]


def getSurveys(context):
    """Return a list of all surveys for the current sector.

    The return value is a sorted list of dictionaries describing the
    surveygroups for the sector. Each dictionary has the following
    keys:

    * ``id``: surveygroup id
    * ``title`` surveygroup title
    * ``url``: URL for the surveygroup
    * ``published``: boolean indicating if this surveygroup is published
    * ``surveys``: list of surveys for the surveygroup. Each entry is a
      dictionary with the following keys:

      * ``id``: survey id
      * ``title``: survey title
      * ``url``: URL for the survey
      * ``published``: boolean indicating if this survey is the currently
        published version of the surveygroup
      * ``current``: boolean indicating if the *context* is inside this survey
      * ``versions``: list of published versions

    """
    current_version = None
    for sector in aq_chain(aq_inner(context)):
        if ISurvey.providedBy(sector):
            current_version = aq_base(sector)
        if ISector.providedBy(sector):
            break
    else:
        return []

    result = []
    groups = [group for group in sector.values()
                if ISurveyGroup.providedBy(group)]
    repository = getToolByName(context, "portal_repository")
    allow_history = checkPermission(context, AccessPreviousVersions)

    def morph(group, survey):
        info = {'id': survey.id,
                'title': survey.title,
                'url': survey.absolute_url(),
                'published': survey.id == group.published,
                'current': aq_base(survey) is current_version,
                'modified': isDirty(survey),
                'versions': []}
        if not allow_history:
            return info

        history = repository.getHistoryMetadata(survey)
        if history:
            for id in range(history.getLength(countPurged=False) - 1, -1, -1):
                meta = history.retrieve(id,
                        countPurged=False)["metadata"]["sys_metadata"]
                info["versions"].append({
                    'timestamp': datetime.datetime.fromtimestamp(
                        meta["timestamp"]),
                    'history_id': meta["parent"]["history_id"],
                    'version_id': meta["parent"]["version_id"],
                    'location_id': meta["parent"]["location_id"]})
            info["versions"].sort(key=lambda x: x["timestamp"], reverse=True)
        return info

    for group in groups:
        info = {'id': group.id,
                'title': group.title,
                'url': group.absolute_url(),
                'published': bool(group.published)}
        info["surveys"] = [morph(group, survey)
                           for survey in group.values()
                           if ISurvey.providedBy(survey)]
        info["surveys"].sort(key=lambda s: s["title"].lower())
        result.append(info)
    result.sort(key=lambda g: g["title"].lower())
    return result


class View(grok.View):
    grok.context(ISector)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("sector_view")
    grok.name("nuplone-view")

    def update(self):
        self.add_survey_url = "%s/++add++euphorie.surveygroup" % \
                aq_inner(self.context).absolute_url()
        self.surveys = getSurveys(self.context)
        super(View, self).update()


class Delete(actions.Delete):
    """ Only delete the sector if it doesn't have any published surveys.
    """
    grok.context(ISector)

    def verify(self, container, context):
        if not checkPermission(container, "Delete objects"):
            raise zExceptions.Unauthorized

        flash = IStatusMessage(self.request).addStatusMessage
        sector = context
        country = container
        client = getPortal(container).client

        if country.id not in client:
            return True

        cl_country = client[country.id]
        if sector.id not in cl_country:
            return True

        # Look for any published surveys in the client sector, and prevent
        # deletion if any are found
        cl_sector = cl_country[sector.id]
        surveys = [s for s in cl_sector.values() if s.id != 'preview']
        if surveys:
            flash(
                _("message_not_delete_published_sector",
                default=u"You can not delete a sector that contains published "
                        u"OiRA Tools."), "error")
            self.request.response.redirect(context.absolute_url())
            return False
        return True


class ColourPreview(grok.View):
    grok.context(ISector)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("colour-preview")
    grok.template("colour-preview")

    def default_title(self):
        from .. import MessageFactory as _
        return _('title_tool', default=u'OiRA - Online interactive Risk Assessment')


class Settings(form.SchemaEditForm):
    grok.context(ISector)
    grok.require("cmf.ModifyPortalContent")
    grok.layer(NuPloneSkin)
    grok.name("edit")
    grok.template("settings")

    schema = ISector
    default_fieldset_label = None
    formErrorsMessage = u"Please correct the indicated errors."

    def update(self):
        super(Settings, self).update()
        config = getUtility(IAppConfig).get("euphorie", {})
        self.main_colour = config.get("main_colour", '#031c48')
        self.support_colour = config.get("support_colour", '#e69d17')
        self.main_bg_colour = config.get("main_bg_colour", '#031c48')
        self.support_bg_colour = config.get("support_bg_colour", '#e69d17')

    def extractData(self):
        self.fields = self.fields.omit("title", "login")
        if "title" in self.widgets:
            del self.widgets["title"]
        if "login" in self.widgets:
            del self.widgets["login"]
        return super(Settings, self).extractData()


class VersionCommand(grok.View):
    grok.context(ISector)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.name("version-command")

    def render(self):
        action = self.request.get("action")
        if action == "new":
            sector = aq_inner(self.context)
            self.request.response.redirect(
                    "%s/++add++euphorie.surveygroup" % sector.absolute_url())
        else:
            log.error("Invalid version command action: %r", action)
