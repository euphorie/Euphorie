from Acquisition import aq_parent
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager


def _create(container, *args, **kwargs):
    newid=container.invokeFactory(*args, **kwargs)
    return getattr(container, newid)


def createSector(portal, sector, password=None, country="nl"):
    sm=getSecurityManager()

    try:
        admin=aq_parent(portal).acl_users.getUserById("portal_owner")
        newSecurityManager(None, admin)

        if hasattr(portal, "sectors"):
            container=portal.sectors
        else:
            container=_create(portal, "euphorie.sectorcontainer", "sectors")
        if "nl" in container:
            country=container["nl"]
        else:
            country=_create(container, "euphorie.country", "nl")
        sector=_create(country, "euphorie.sector", sector)
        if password is None:
            password=sector.id
        sector.password=password
        return sector
    finally:
        setSecurityManager(sm)


