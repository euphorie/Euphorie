import logging
from Acquisition import aq_parent
from five import grok
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from plonetheme.nuplone.utils import getPortal
from euphorie.content.interfaces import ISurveyUnpublishEvent
from euphorie.content.survey import ISurvey

log = logging.getLogger(__name__)


@grok.subscribe(ISurvey, ISurveyUnpublishEvent)
def handleSurveyUnpublish(survey, event):
    """Event handler (subscriber) to take care of unpublishing a survey
    from the client.
    """
    surveygroup = aq_parent(survey)
    sector = aq_parent(surveygroup)
    country = aq_parent(sector)

    pas = getToolByName(survey, "acl_users")
    clientuser = pas.getUserById("client")
    sm = getSecurityManager()
    try:
        newSecurityManager(None, clientuser)
        client = getPortal(survey).client
        try:
            clientcountry = client[country.id]
            clientsector = clientcountry[sector.id]
            clientsector[surveygroup.id]
        except KeyError:
            log.info("Trying to unpublish unpublished survey %s",
                    "/".join(survey.getPhysicalPath()))
            return

        clientsector.manage_delObjects([surveygroup.id])
        if not clientsector.keys():
            clientcountry.manage_delObjects([clientsector.id])
    finally:
        setSecurityManager(sm)
