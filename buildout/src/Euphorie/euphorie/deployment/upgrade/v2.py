import logging
from Products.CMFCore.utils import getToolByName

log = logging.getLogger(__name__)

def resetSurveyWorkflow(context):
    wt=getToolByName(context, 'portal_workflow')
    workflow=wt.survey
    published=workflow.states.published
    if "Copy or Move" in published.permission_roles:
        log.info("Copy or Move permission already set")
        return

    log.info("Fixing Copy or Move permission in survey workflow")
    published.permission_roles["Copy or Move"]=("Authenticated", "Sector", "CountryManager", "Manager")
    count=wt._recursiveUpdateRoleMappings(context, {"survey": workflow})
    log.info("Updated permissions for %d objects", count)


