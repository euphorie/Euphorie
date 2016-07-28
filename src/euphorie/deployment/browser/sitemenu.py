from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces.user import IMembraneUser
from plonetheme.nuplone.utils import getPortal
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.skin.sitemenu import Sitemenu
from plonetheme.nuplone import MessageFactory as nu_
from euphorie.content import MessageFactory as _
from euphorie.content.sector import ISector
from euphorie.content.survey import ISurvey


class EuphorieSitemenu(Sitemenu):
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
        menu = super(EuphorieSitemenu, self).organise()
        if menu is not None:
            children = menu["children"]
        else:
            menu = {"title": nu_("menu_organise", default=u"Organise")}
            children = menu["children"] = []

        context_url = aq_inner(self.context).absolute_url()
        if ISurvey.providedBy(self.context) and \
                checkPermission(self.context, "View"):
            children.append({"title": _("menu_export", default=u"XML export"),
                             "url": "%s/@@export" % context_url})
        if ISector.providedBy(self.context) and \
                checkPermission(self.context, "Euphorie: Add new RIE Content"):
            children.append(
                    {"title": _("menu_import", default=u"Import OiRA Tool"),
                     "url": "%s/@@upload" % context_url})
        if children:
            return menu
        else:
            return None
