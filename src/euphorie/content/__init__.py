from AccessControl.Permission import addPermission
from zope.i18nmessageid import MessageFactory as mf


MessageFactory = mf("euphorie")
del mf


addPermission("Euphorie: Manage country", ("Manager",))
addPermission("Euphorie: Add new RIE Content", ("Manager",))
addPermission("Euphorie: Delete published content", ("Manager",))
