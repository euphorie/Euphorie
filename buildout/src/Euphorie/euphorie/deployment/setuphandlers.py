import logging
from zope.interface import alsoProvides
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import _createObjectByType
from plone.app.layout.navigation.interfaces import INavigationRoot

log = logging.getLogger(__name__)

def setupVarious(context):
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('euphorie.deployment.txt') is None:
        return

    site=context.getSite()
    disableRedirectTracking(site)
    setupInitialContent(site)
    setupVersioning(site)

COUNTRIES = dict(at=u"Austria",
                 be=u"Belgium",
                 bg=u"Bulgaria",
                 se=u"Sweden",
                 cy=u"Cyprus",
                 cz=u"The Czech Republic",
                 de=u"Germany",
                 dk=u"Denmark",
                 ee=u"Estonia",
                 es=u"Spain",
                 fi=u"Finland",
                 fr=u"France",
                 gb=u"The United Kingdom",
                 gr=u"Greece",
                 hu=u"Hungary",
                 ie=u"Ireland",
                 it=u"Italy",
                 lt=u"Lithuania",
                 lu=u"Luxembourg",
                 lv=u"Latvia",
                 mt=u"Malta",
                 nl=u"The Netherlands",
                 pl=u"Poland",
                 pt=u"Portugal",
                 ro=u"Romania",
                 sk=u"Slovakia",
                 si=u"Slovenia",
                 )


def setupInitialContent(site):
    from Products.CMFCore.utils import getToolByName

    present=site.objectIds()
    wt=site.portal_workflow

    for obj in [ "Members", "events", "news"]:
        if obj in present:
            site.manage_delObjects([obj])
            log.info("Removed default Plone %s folder", obj)

    if "sectors" not in present:
        site.invokeFactory("euphorie.sectorcontainer", "sectors", title="Surveys")
        mt=getToolByName(site, "portal_membership")
        mt.setMembersFolderById("sectors")
        log.info("Added sectors folder")

    sectors=site.sectors
    for (country_id, title) in COUNTRIES.items():
        if country_id not in sectors:
            sectors.invokeFactory("euphorie.country", country_id, title=title)
            log.info("Added country %s (%s)", country_id, title)
        country=sectors[country_id]
        if "help" not in country:
            createContentInContainer(country, "euphorie.page", id="help", title=u"Help", checkConstraints=False)
            log.info("Added help section for country %s (%s)", country_id, title)
        help=country["help"]
        if not INavigationRoot.providedBy(help):
            alsoProvides(help, INavigationRoot)
            log.info("Made help for country %s (%s) a navigation root.", country_id, title)

    if "client" not in present:
        site.invokeFactory("euphorie.client", "client", title="Client")
        wt.doActionFor(site.client, "publish")
        log.info("Added Euphorie client instance")

    if "documents" not in present:
        site.invokeFactory("euphorie.folder", "documents", title=u"Documents")
        log.info("Added documents folder")
    documents=site.documents

    if not INavigationRoot.providedBy(documents):
        alsoProvides(documents, INavigationRoot)
        log.info("Made documentation folder a navigation root.")

    lt=getToolByName(site, "portal_languages")
    present_languages=documents.objectIds()
    for (code,name) in lt.listSupportedLanguages():
        if code not in present_languages:
            documents.invokeFactory("euphorie.documentation", code, title=name)
            log.info("Added documentation folder for %s (%s)", name, code)
        docs=documents[code]
        if "help" not in docs:
            createContentInContainer(docs, "euphorie.help", id="help", checkConstraints=False)
            log.info("Added online help text for language %s (%s)", name, code)
        if "appendix" not in docs:
            _createObjectByType("euphorie.page", docs, "appendix", title=u"Appendix")
            log.info("Added appendix folder for language %s (%s)", name, code)




def disableRedirectTracking(site):
    # Add additional setup code here
    from zope.component import getSiteManager
    from zope.component.interfaces import IComponentRegistry
    from plone.app.redirector.interfaces import IRedirectionStorage
    sm=getSiteManager(site)
    if sm is None or not IComponentRegistry.providedBy(sm):
        log.warn("Failed to find a site manager, can not remove IRedirectionStorage utility")
        return

    sm.unregisterUtility(provided=IRedirectionStorage)


def setupVersioning(site):
    repository=site.portal_repository
    if "euphorie.survey" not in repository.getVersionableContentTypes():
        repository.setVersionableContentTypes(["euphorie.survey"])
        log.info("Enabled versioning for survey versions.")

