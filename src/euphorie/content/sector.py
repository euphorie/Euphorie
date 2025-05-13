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
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.indexer import indexer
from plone.namedfile import field as filefield
from plone.supermodel import model
from plone.uuid.interfaces import IAttributeUUID
from plonetheme.nuplone.utils import checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.Permissions import AccessPreviousVersions
from zope import schema
from zope.component import adapter
from zope.interface import implementer

import datetime
import logging


log = logging.getLogger(__name__)


class ISector(model.Schema, IUser, IBasic):
    """Sector object.

    A sector is a national organisation for a specific type of industry.
    """

    directives.order_before(title="*")
    directives.write_permission(title="euphorie.content.ManageCountry")

    directives.order_after(login="title")
    directives.write_permission(login="euphorie.content.ManageCountry")

    directives.order_before(password="description")

    directives.order_after(locked="password")
    directives.write_permission(locked="euphorie.content.ManageCountry")

    contact_name = schema.TextLine(
        title=_("label_contact_name", default="Contact name"), required=True
    )

    directives.order_after(contact_email="contact_name")

    logo = filefield.NamedBlobImage(
        title=_("label_logo", default="Logo"),
        description=_(
            "help_image_upload",
            default=(
                "The logo will appear on the sector overview page of your country. "
                "Make sure your image is of format png, jpg or gif and "
                "does not contain any special characters. "
                "The new logo will only become visible after "
                "you have saved your changes and "
                "published the OiRA tool."
            ),
        ),
        required=False,
    )


@implementer(ISector, INavigationRoot, IAttributeUUID)
class Sector(Container):
    """A sector of industry.

    A sector also acts as a user account in the system, using the
    membrane framework.
    """

    portal_type = "euphorie.clientsector"

    locked = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return op


@indexer(ISector)
def SearchableTextIndexer(obj):
    return " ".join(
        [obj.title, obj.description, obj.contact_name or "", obj.contact_email or ""]
    )


@adapter(ISector)
@implementer(ILocalRoleProvider)
class SectorLocalRoleProvider:
    """`borg.localrole` provider for :obj:`ISector` instances.

    This local role provider gives the sector user itself the `Sector`
    local role.
    """

    def __init__(self, context):
        self.context = context

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
    * ``obsolete``: boolean indicating if this surveygroup is obsolete
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
    groups = [group for group in sector.values() if ISurveyGroup.providedBy(group)]
    repository = getToolByName(context, "portal_repository")
    allow_history = checkPermission(context, AccessPreviousVersions)

    def morph(group, survey):
        published = survey.id == group.published
        info = {
            "id": survey.id,
            "title": survey.title,
            "url": survey.absolute_url(),
            "published": published,
            "publication_date": published and survey.published or None,
            "current": aq_base(survey) is current_version,
            "modified": isDirty(survey),
            "versions": [],
        }
        if not allow_history:
            return info

        history = repository.getHistoryMetadata(survey)
        if history:
            for id in range(history.getLength(countPurged=False) - 1, -1, -1):
                meta = history.retrieve(id, countPurged=False)["metadata"][
                    "sys_metadata"
                ]
                info["versions"].append(
                    {
                        "timestamp": datetime.datetime.fromtimestamp(meta["timestamp"]),
                        "history_id": meta["parent"]["history_id"],
                        "version_id": meta["parent"]["version_id"],
                        "location_id": meta["parent"]["location_id"],
                    }
                )
            info["versions"].sort(key=lambda x: x["timestamp"], reverse=True)
        return info

    for group in groups:
        info = {
            "id": group.id,
            "title": group.title,
            "url": group.absolute_url(),
            "published": bool(group.published),
            "obsolete": bool(group.obsolete),
        }
        info["surveys"] = [
            morph(group, survey)
            for survey in group.values()
            if ISurvey.providedBy(survey)
        ]
        info["surveys"].sort(key=lambda s: s["title"].lower())
        result.append(info)
    result.sort(key=lambda g: g["title"].lower())
    return result
