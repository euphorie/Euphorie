from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces.user import IMembraneUser
from plonetheme.nuplone.utils import getPortal
from plonetheme.nuplone.skin.sitemenu import Sitemenu

class EuphorieSitemenu(Sitemenu):
    @property
    def settings_url(self):
        user=getSecurityManager().getUser()

        if IMembraneUser.providedBy(user):
            mt=getToolByName(self.context, "membrane_tool")
            home=mt.getUserObject(user_id=user.getUserId())
            return "%s/@@edit" % home.absolute_url()
        else:
            home=getPortal(self.context)
            return "%s/@@settings" % home.absolute_url()

