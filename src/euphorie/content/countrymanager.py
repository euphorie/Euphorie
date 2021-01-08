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
from five import grok
from plone.dexterity.content import Item
from plone.directives import form
from plone.indexer import indexer
from plone.uuid.interfaces import IAttributeUUID
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from Products.CMFCore.utils import getToolByName
from zope.interface import implements


grok.templatedir("templates")


class ICountryManager(form.Schema, IUser):
    """A country manager is responsible for managing sectors in their country."""


class CountryManager(Item):
    """A country manager."""

    portal_type = "euphorie.countrymanager"
    implements(ICountryManager, IAttributeUUID)

    locked = False

    def _canCopy(self, op=0):
        """Tell Zope2 that this object can not be copied."""
        return False


@indexer(ICountryManager)
def SearchableTextIndexer(obj):
    """Index the title, contact_name and contact_email"""
    return " ".join([obj.title, obj.contact_name, obj.contact_email])


class CountryManagerLocalRoleProvider(grok.Adapter):
    """`borg.localrole` provider for :py:class:`ICountryManager` instances.

    This local role provider gives country managers the Administrator
    role within their country.
    """

    grok.context(ICountry)
    grok.implements(ILocalRoleProvider)
    grok.name("euphorie.countrymanager")

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


class View(grok.View):
    """View name: @@nuplone-view"""

    grok.context(ICountryManager)
    grok.require("zope2.View")
    grok.layer(NuPloneSkin)
    grok.template("countrymanager_view")
    grok.name("nuplone-view")
