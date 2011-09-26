import datetime
import logging
from htmllaundry import StripMarkup
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from euphorie.client.sector import IClientSector
from euphorie.content.risk import EnsureInterface
from euphorie.content.survey import ISurvey

log = logging.getLogger(__name__)


def set_evaluation_method_interfaces(context):
    ct = getToolByName(context, "portal_catalog")
    risks = ct(portal_type="euphorie.risk")
    count = 0
    for brain in risks:
        log.debug("Updating interfaces for %s", brain.getPath())
        risk = brain.getObject()
        EnsureInterface(risk)
        count += 1
    log.info("Updated interfaces for %d risks", count)


def convert_solution_description_to_text(context):
    ct = getToolByName(context, "portal_catalog")
    risks = ct(portal_type="euphorie.solution")
    count = 0
    for brain in risks:
        log.debug("Updating description for %s", brain.getPath())
        try:
            solution = brain.getObject()
        except KeyError:
            log.error('Could not get object for %s', brain.getPath())
        description = StripMarkup(solution.description)
        if description != solution.description:
            solution.description = description
        count += 1
    log.info("Updated description for %d solutions", count)


def add_wp_column_to_company(context):
    from z3c.saconfig import Session
    from euphorie.deployment.upgrade.utils import TableExists
    from euphorie.client import model
    from zope.sqlalchemy import datamanager
    import transaction

    session=Session()
    if TableExists(session, "company"):
        session.execute("ALTER TABLE company ADD workers_participated bool NULL")
        model.metadata.create_all(session.bind, checkfirst=True)
        datamanager.mark_changed(session)
        transaction.get().commit()

    log.info("Added new column 'workers_participated' to table 'company'")


def renew_survey_published_date(context):
    """ Update the published attr of surveys to set the date to now.
        This will force all surveys to redirect to the @@update page from where
        users' session trees can be updated.
    """
    site = getSite()
    client = getattr(site, 'client')
    # Loop through all client surveys
    for country in client.objectValues():
        for sector in country.objectValues():
            if not IClientSector.providedBy(sector):
                continue

            for survey in sector.objectValues():
                if not ISurvey.providedBy(survey):
                    continue

                published = getattr(survey, "published", None)
                if isinstance(published, tuple):
                    survey.published = (
                        published[0], published[1], datetime.datetime.now())
                else:
                    # BBB: Euphorie 1.x did not use a tuple to store extra 
                    # information.
                    published = datetime.datetime.now()

