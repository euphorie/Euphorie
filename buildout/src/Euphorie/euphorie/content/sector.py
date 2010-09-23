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

from Acquisition import aq_base
from Acquisition import aq_inner
from zope.interface import implements
from zope.component import adapts
from zope import schema
from zope import event
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.app.dexterity.behaviors.metadata import IBasic
from euphorie.content import MessageFactory as _
from plone.namedfile import field as filefield
from Products.membrane.interfaces import user as membrane
from Products.Archetypes.event import ObjectEditedEvent
from borg.localrole.interfaces import ILocalRoleProvider
from euphorie.content.surveygroup import ISurveyGroup
from euphorie.content import colour
from z3c.form.browser.password import PasswordFieldWidget



class ISector(form.Schema, IBasic):
    """Sector object.

    A sector is a national organisation for a specific type of
    industry.
    """

    title = schema.TextLine(
            title = _(u"Name"),
            description = _(u"The name of the sector will also be used to "
                            u"generate the login name for the sector "
                            u"account."),
            required = True)
    form.order_before(title="*")

    password = schema.Password(
            title = _(u"Password"),
            required = True)
    form.order_after(password="title")
    form.widget(password=PasswordFieldWidget)

    contact_name = schema.TextLine(
            title = _(u"Contact"),
            description = _(u"The name of the person or organisation "
                            u"responsible for maintaining this sector."),
            required=True)

    contact_email = schema.ASCIILine(
            title = _(u"Contact email address"),
            description = _(u"Email address for the person or organisation "
                            u"responsible for maintaining this sector."),
            required = True)


    logo = filefield.NamedImage(
            title = _(u"Sector logo"),
            description = _(u"The sector logo will be shown instead of the "
                            u"agency logo. A logo should not be larger than "
                            u"370x100 pixels."),
            required = False)

    main_colour = colour.Colour(
            title = _(u"Main site background colour"),
            required = False)
    form.widget(main_colour=colour.ColourFieldWidget)

    support_colour = colour.Colour(
            title = _(u"Site background support colour"),
            description = _(u"This colour is only used if the main colour is "
                            u"also set."),
            required = False)
    form.widget(support=colour.ColourFieldWidget)



class Sector(dexterity.Container):
    """A sector of industry.

    A sector also acts as a user account in the system, using the membrane
    framework.
    """
    implements(ISector)



class SectorLocalRolesProvider(object):
    """`borg.localrole` provider for :obj:`ISector` instances.

    This local role provider gives the sector user itself the
    `Sector` local role.
    """
    adapts(ISector)
    implements(ILocalRoleProvider)

    def __init__(self, sector):
        self.sector=sector

    def getRoles(self, principal_id):
        if principal_id==self.sector.getId():
            return ("Sector",)
        return ()

    def getAllRoles(self):
        return [(self.sector.getId(), ("Sector",))]



class SectorUserProvider(object):
    """Base class for membrane adapters for :obj:`ISector` instances.
    
    This base class implements the
    :obj:`Products.membrane.interfaces.IMembraneUserObject` interface which is
    responisble for generating an id for a user object. This implementation
    uses the id of the sector as both userid and login name. This is safe in an
    Euphorie site since all sectors are stored in the same container,
    preventing id conflicts.

    This adapter does not claim to implement the `IMembraneUserObject`
    interface itself, since that would complicate the registration of the other
    adapters a little bit (`zope.component` can no longer determine the
    interface provided by an adapter if it provides multiple interfaces, even
    if they are derived classes).
    """
    adapts(ISector)

    def __init__(self, sector):
        self.sector=sector

    def getUserId(self):
        return self.sector.id

    def getUserName(self):
        return self.sector.id



class SectorUserAuthentication(SectorUserProvider):
    """Sector account authentication routines.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserAuth` interface. This
    interface is responsible for the authentication logic of accounts.
    """
    adapts(ISector)
    implements(membrane.IMembraneUserAuth)

    def __init__(self, sector):
        self.sector=sector

    def authenticateCredentials(self, credentials):
        candidate=credentials.get("password", None)
        real=getattr(aq_base(self.sector), "password", None)
        if candidate is None or real is None:
            return None

        if candidate==real:
            return (self.getUserId(), self.getUserName())

        return None


class SectorUserChanger(SectorUserProvider):
    """Sector account password changing.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserChanger` interface. This
    interface is responsible for changing a users password.
    """
    adapts(ISector)
    implements(membrane.IMembraneUserChanger)

    def doChangeUser(self, login, password, **kwargs):
        """Set the login name and password for a sector.

        Changing the username for a sector is not allowed, and any
        attempt to do so will raise a `ValueError`.

        The *password* parameter is the plaintext password.
        """
        if login!=self.sector.id:
            raise ValueError("Username changes are not allowed for sectors")
        self.sector.password=password



class SectorUserProperties(SectorUserProvider):
    """Sector user properties handling.

    This adapter implements the
    :obj:`Products.membrane.interfaces.user.IMembraneUserProperties` interface. This
    interface is responsible all handling of member properties.

    The interface is based on the basic PAS plugin
    :obj:`Products.PluggableAuthService.interfaces.IMutablePropertiesPlugin`
    interface. As a result all methods take a `user` parameter, which should
    always be the same as the adapted object for membrane adapters.
    """
    adapts(ISector)
    implements(membrane.IMembraneUserProperties)

    # A mapping for ISector properties to Plone user properties
    property_map = [ ( "title",         "fullname" ),
                     ( "contact_email", "email" ) ]

    def getPropertiesForUser(self, user, request=None):
        properties={}
        for (sector_prop, user_prop) in self.property_map:
            value=getattr(self.sector, sector_prop)
            # None values are not allowed, so replace those with an empty string
            properties[user_prop]=(value is not None) and value or u""
        return properties


    def setPropertiesForUser(self, user, propertysheet):
        marker = []
        changes=set()
        for (sector_prop, user_prop) in self.property_map:
            value=propertysheet.getProperty(user_prop, default=marker)
            if value is not marker:
                setattr(self.sector, sector_prop, value)
                changes.add(sector_prop)

        if changes:
            self.sector.reindexObject(idxs=list(changes))
            event.notify(ObjectEditedEvent(self.sector))



class View(grok.View):
    grok.context(ISector)
    grok.require("zope2.View")

    def update(self):
        self.add_survey_url="%s/++add++euphorie.surveygroup" % \
                aq_inner(self.context).absolute_url()
        self.surveys=[dict(id=survey.id,
                           title=survey.title,
                           url=survey.absolute_url())
                      for survey in self.context.values()
                      if ISurveyGroup.providedBy(survey)]
        super(View, self).update()

