from zope.i18nmessageid import MessageFactory as mf
MessageFactory = mf("euphorie")
del mf

from Products.CMFCore.permissions import setDefaultRoles

setDefaultRoles("Euphorie: Manage country", ("Manager",))
setDefaultRoles("Euphorie: Add new RIE Content", ("Manager",))
setDefaultRoles("Euphorie: Delete published content", ("Manager",))
