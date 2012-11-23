from zope.component import adapter
from Products.PluggableAuthService.interfaces.events import IUserLoggedInEvent
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUser


@adapter(IMembraneUser, IUserLoggedInEvent)
def SectorLoginHandler(account, event):
    """Event handler for logins on the Plone site. This is used to redirect
    sectors on login to their own section of the site.
    """
    request = getattr(account, "REQUEST", None)
    if request is None:
        return

    mt = getToolByName(account, "membrane_tool", None)
    if mt is None:
        return

    obj = mt.getUserObject(user_id=account.getId(), brain=False)
    if obj is not None:
        # Set came_from in the request to make sure login_next will not
        # redirect the user to another place.
        request.other["came_from"] = obj.absolute_url()
        request.response.redirect(obj.absolute_url(), lock=True)
