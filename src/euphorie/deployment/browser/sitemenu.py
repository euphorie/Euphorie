from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Acquisition import aq_inner
from euphorie.content import MessageFactory as _
from euphorie.content.sector import ISector
from euphorie.content.survey import ISurvey
from plone import api
from plonetheme.nuplone import MessageFactory as nu_
from plonetheme.nuplone.skin import sitemenu
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.utils import getPortal
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces.user import IMembraneUser


class Sitemenu(sitemenu.Sitemenu):
    @property
    def actions(self):
        """See plonetheme.nuplone.skin.sitemenu.py."""
        menu = super().actions or {}
        children = menu.get("children")
        if not children:
            return None

        submenu = self.menu_country_tools()
        if submenu:
            self.add_submenu(children, submenu)
        if children:
            return menu
        else:
            return None

    def menu_country_tools(self):
        context = aq_inner(self.context)

        # We try to traverse to the view. It would fail for the wrong context
        # (not an ICountry) or if permissions are not met.
        try:
            self.context.restrictedTraverse("@@country-tools")
        except (AttributeError, Unauthorized):
            return None

        menu = {"title": _("menu_admin", default="Admin")}
        menu["children"] = [
            {
                "title": _("menu_country_tools", default="Tools for this country"),
                "url": "%s/@@country-tools" % context.absolute_url(),
            }
        ]
        return menu

    @property
    def settings_url(self):
        user = getSecurityManager().getUser()
        if IMembraneUser.providedBy(user):
            mt = getToolByName(self.context, "membrane_tool")
            home = mt.getUserObject(user_id=user.getUserId())
            return "%s/@@edit" % home.absolute_url()
        else:
            home = getPortal(self.context)
            return "%s/@@settings" % home.absolute_url()

    def organise(self):
        menu = super().organise()
        if menu is not None:
            children = menu["children"]
        else:
            menu = {"title": nu_("menu_organise", default="Organise")}
            children = menu["children"] = []

        context_url = aq_inner(self.context).absolute_url()
        if ISurvey.providedBy(self.context) and checkPermission(self.context, "View"):
            children.append(
                {
                    "title": _("menu_export", default="XML export"),
                    "url": "%s/@@export" % context_url,
                }
            )
        if ISector.providedBy(self.context) and checkPermission(
            self.context, "Euphorie: Add new RIE Content"
        ):
            children.append(
                {
                    "title": _("menu_import", default="Import OiRA Tool"),
                    "url": "%s/@@upload" % context_url,
                }
            )

        if api.user.has_permission("Manage portal"):
            children.append(
                {
                    "title": _("Maintenance view"),
                    "url": f"{api.portal.get().absolute_url()}/@@admin-maintenance",
                }
            )

        if children:
            return menu
        else:
            return None
