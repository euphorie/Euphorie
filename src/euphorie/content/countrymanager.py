"""
Country Manager
---------------

A `membrane` user account inside a country that has the permission to add
sectors (which are also membrane users) to that country.

.. _membrane: http://pypi.python.org/pypi/Products.membrane
"""

from Acquisition import aq_inner
from borg.localrole.interfaces import ILocalRoleProvider
from euphorie.content.country import ICountry
from euphorie.content.user import IUser
from euphorie.content.user import UserProvider
from plone.dexterity.content import Item
from plone.indexer import indexer
from plone.supermodel import model
from plone.uuid.interfaces import IAttributeUUID
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import implementer


class ICountryManager(model.Schema, IUser):
    """A country manager is responsible for managing sectors in their
    country."""


@implementer(ICountryManager, IAttributeUUID)
class CountryManager(Item):
    """A country manager."""

    portal_type = "euphorie.countrymanager"

    locked = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False


@indexer(ICountryManager)
def SearchableTextIndexer(obj):
    """Index the title, contact_name and contact_email."""
    return " ".join([obj.title, obj.contact_name, obj.contact_email])


@adapter(ICountry)
@implementer(ILocalRoleProvider)
class CountryManagerLocalRoleProvider:
    """`borg.localrole` provider for :py:class:`ICountryManager` instances.

    This local role provider gives country managers the Administrator
    role within their country.
    """

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal_id):
        mt = getToolByName(self.context, "membrane_tool")
        user = mt.getUserObject(user_id=principal_id, brain=True)
        if user is None:
            return ()

        user = user._unrestrictedGetObject()
        if not ICountryManager.providedBy(user):
            return ()

        if user.getPhysicalPath()[:-1] == aq_inner(self.context).getPhysicalPath():
            return ("CountryManager", "Editor", "Contributor", "Reader", "Reviewer")
        else:
            return ()

    def getAllRoles(self):
        managers = [
            UserProvider(manager)
            for manager in self.context.values()
            if ICountryManager.providedBy(manager)
        ]
        return [
            (
                manager.getUserId(),
                ("CountryyManager", "Editor", "Contributor", "Reader", "Reviewer"),
            )
            for manager in managers
        ]
