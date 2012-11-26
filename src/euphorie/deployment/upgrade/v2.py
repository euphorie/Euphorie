import logging
from Acquisition import aq_parent

log = logging.getLogger(__name__)


def resetSurveyWorkflow(context):
    from Products.CMFCore.utils import getToolByName
    siteroot = aq_parent(context)
    wt = getToolByName(siteroot, 'portal_workflow')
    workflow = wt.survey
    published = workflow.states.published
    if "Copy or Move" in published.permission_roles:
        log.info("Copy or Move permission already set")
        return

    log.info("Fixing Copy or Move permission in survey workflow")
    published.permission_roles["Copy or Move"] = ("Authenticated", "Sector",
                                                  "CountryManager", "Manager")
    count = wt._recursiveUpdateRoleMappings(siteroot, {"survey": workflow})
    log.info("Updated permissions for %d objects", count)


def resetPublishPermission(context):
    from AccessControl.Permission import Permission
    siteroot = aq_parent(context)
    permission = Permission("Euphorie: Publish a Survey", (), siteroot)
    if "CountryManager" not in permission.getRoles(default=[]):
        permission.setRole("CountryManager", True)
        log.info("Adding publish permission for country managers")


def migrateCompanyTable(context):
    from z3c.saconfig import Session
    from euphorie.deployment.upgrade.utils import ColumnExists
    from euphorie.deployment.upgrade.utils import TableExists
    from euphorie.client import model
    from zope.sqlalchemy import datamanager
    import transaction

    session = Session()
    if ColumnExists(session, "company", "referer"):
        return

    if TableExists(session, "company"):
        log.info("Moving company table to dutch_company")
        session.execute("ALTER TABLE company RENAME TO dutch_company")
        session.execute(
                "ALTER SEQUENCE company_id_seq RENAME TO dutch_company_id_seq")
        session.execute(
                "ALTER INDEX ix_company_session_id RENAME TO "
                        "ix_dutch_company_session_id")
        model.metadata.create_all(session.bind, checkfirst=True)
        datamanager.mark_changed(session)
        transaction.get().commit()

    log.info("Creating new company table")


def addTermsAndConditionsColumn(context):
    from z3c.saconfig import Session
    from euphorie.deployment.upgrade.utils import ColumnExists
    from zope.sqlalchemy import datamanager
    import transaction
    session = Session()
    if ColumnExists(session, "user", "tc_approved"):
        return

    log.info("Adding tc_approved column to account table")
    session.execute("ALTER TABLE account ADD COLUMN tc_approved INT")
    datamanager.mark_changed(session)
    transaction.get().commit()


def updateSurveyWorkflow(context):
    from Products.CMFCore.utils import getToolByName
    siteroot = aq_parent(context)
    log.info("Reloading content workflows.")
    context.runImportStepFromProfile("profile-euphorie.content:default",
            "workflow", False)
    log.info("Updating permissions for existing content.")
    wt = getToolByName(siteroot, "portal_workflow")
    count = wt.updateRoleMappings()
    log.info("Updated permissions for %d objects.", count)


def updateInitialContent(context):
    from euphorie.deployment.setuphandlers import setupInitialContent
    siteroot = aq_parent(context)
    setupInitialContent(siteroot)


def addAccountChangeTable(context):
    from z3c.saconfig import Session
    from euphorie.client import model
    from zope.sqlalchemy import datamanager
    import transaction
    transaction.get().commit()  # Clean current connection to prevent hangs
    session = Session()
    model.AccountChangeRequest.__table__.create(
            bind=session.bind, checkfirst=True)
    datamanager.mark_changed(session)
    transaction.get().commit()


def addCountryGrouping(context):
    from euphorie.deployment.setuphandlers import COUNTRIES
    sectors = aq_parent(context).sectors
    client = aq_parent(context).client
    for (country_id, info) in COUNTRIES.items():
        for parent in sectors, client:
            country = parent.get(country_id)
            if country is None:
                continue
            if getattr(country, "country_type", None):
                continue
            country.country_type = info[1]
            log.info("Set country type for %s to %s in %s", country_id,
                    info[1], parent.Title())
