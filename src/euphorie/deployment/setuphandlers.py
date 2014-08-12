import logging
from Products.CMFPlone.utils import _createObjectByType
from Products.PlonePAS.plugins.passwordpolicy import PasswordPolicyPlugin
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from euphorie.client.api.entry import API
from euphorie.content.passwordpolicy import EuphoriePasswordPolicy
from euphorie.content.utils import REGION_NAMES
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.utils import createContentInContainer
from zope.interface import alsoProvides

log = logging.getLogger(__name__)


def setupVarious(context):
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('euphorie.deployment.txt') is None:
        return

    site = context.getSite()
    disableRedirectTracking(site)
    setupInitialContent(site)
    setupVersioning(site)
    registerPasswordPolicy(site)


COUNTRIES = {
        "at": (u"Austria", "eu-member"),
        "be": (u"Belgium", "eu-member"),
        "bg": (u"Bulgaria", "eu-member"),
        "se": (u"Sweden", "eu-member"),
        "cy": (u"Cyprus", "eu-member"),
        "cz": (u"The Czech Republic", "eu-member"),
        "de": (u"Germany", "eu-member"),
        "dk": (u"Denmark", "eu-member"),
        "ee": (u"Estonia", "eu-member"),
        "es": (u"Spain", "eu-member"),
        "fi": (u"Finland", "eu-member"),
        "fr": (u"France", "eu-member"),
        "gb": (u"The United Kingdom", "eu-member"),
        "gr": (u"Greece", "eu-member"),
        "hu": (u"Hungary", "eu-member"),
        "ie": (u"Ireland", "eu-member"),
        "it": (u"Italy", "eu-member"),
        "lt": (u"Lithuania", "eu-member"),
        "lu": (u"Luxembourg", "eu-member"),
        "lv": (u"Latvia", "eu-member"),
        "mt": (u"Malta", "eu-member"),
        "nl": (u"The Netherlands", "eu-member"),
        "pl": (u"Poland", "eu-member"),
        "pt": (u"Portugal", "eu-member"),
        "ro": (u"Romania", "eu-member"),
        "sk": (u"Slovakia", "eu-member"),
        "si": (u"Slovenia", "eu-member"),

        "li": (u"Liechtenstein", "efta"),
        "no": (u"Norway", "efta"),
        "ch": (u"Switzerland", "efta"),

        "hr": (u"Republic of Croatia", "candidate-eu"),
        "is": (u"Republic of Iceland", "candidate-eu"),
        "mk": (u"F.Y.R. Macedonia", "candidate-eu"),
        "me": (u"Montenegro", "candidate-eu"),
        "tr": (u"Republic of Turkey", "candidate-eu"),

        "al": (u"Republic of Albania", "potential-candidate-eu"),
        "ba": (u"Bosnia and Herzegovina", "potential-candidate-eu"),
        "cs": (u"Kosovo", "potential-candidate-eu"),
        "rs": (u"Republic of Serbia", "potential-candidate-eu"),
        }


for i in REGION_NAMES.items():
    COUNTRIES[i[0]] = (i[1], "region")


def setupInitialContent(site):
    from Products.CMFCore.utils import getToolByName

    present = site.objectIds()
    wt = site.portal_workflow

    for obj in ["Members", "events", "news"]:
        if obj in present:
            site.manage_delObjects([obj])
            log.info("Removed default Plone %s folder", obj)

    if "sectors" not in present:
        site.invokeFactory("euphorie.sectorcontainer",
                "sectors", title="Surveys")
        mt = getToolByName(site, "portal_membership")
        mt.setMembersFolderById("sectors")
        log.info("Added sectors folder")

    sectors = site.sectors
    for (country_id, info) in COUNTRIES.items():
        (title, country_type) = info
        if country_id not in sectors:
            sectors.invokeFactory("euphorie.country", country_id,
                    title=title, country_type=country_type)
            log.info("Added country %s (%s)", country_id, title)
        country = sectors[country_id]
        if "help" not in country:
            createContentInContainer(country, "euphorie.page", id="help",
                    title=u"Help", checkConstraints=False)
            log.info("Added help section for country %s (%s)",
                    country_id, title)
        help = country["help"]
        if not INavigationRoot.providedBy(help):
            alsoProvides(help, INavigationRoot)
            log.info("Made help for country %s (%s) a navigation root.",
                    country_id, title)

    if "client" not in present:
        site.invokeFactory("euphorie.client", "client", title="Client")
        wt.doActionFor(site.client, "publish")
        log.info("Added Euphorie client instance")

    client = site.client
    if 'api' not in client:
        client['api'] = API('api')

    if "documents" not in present:
        site.invokeFactory("euphorie.folder", "documents", title=u"Documents")
        log.info("Added documents folder")
    documents = site.documents

    if not INavigationRoot.providedBy(documents):
        alsoProvides(documents, INavigationRoot)
        log.info("Made documentation folder a navigation root.")

    lt = getToolByName(site, "portal_languages")
    present_languages = documents.objectIds()
    for (code, name) in lt.listSupportedLanguages():
        if code not in present_languages:
            documents.invokeFactory("euphorie.documentation", code, title=name)
            log.info("Added documentation folder for %s (%s)", name, code)
        docs = documents[code]
        if "help" not in docs:
            createContentInContainer(docs, "euphorie.help",
                    id="help", checkConstraints=False)
            log.info("Added online help text for language %s (%s)", name, code)
        if "appendix" not in docs:
            _createObjectByType("euphorie.page", docs,
                    "appendix", title=u"Appendix")
            log.info("Added appendix folder for language %s (%s)", name, code)


def disableRedirectTracking(site):
    # Add additional setup code here
    from zope.component import getSiteManager
    from zope.component.interfaces import IComponentRegistry
    from plone.app.redirector.interfaces import IRedirectionStorage
    sm = getSiteManager(site)
    if sm is None or not IComponentRegistry.providedBy(sm):
        log.warn("Failed to find a site manager, can not remove "
                 "IRedirectionStorage utility")
        return

    sm.unregisterUtility(provided=IRedirectionStorage)


def setupVersioning(site):
    repository = site.portal_repository
    if "euphorie.survey" not in repository.getVersionableContentTypes():
        repository.setVersionableContentTypes(["euphorie.survey"])
        log.info("Enabled versioning for survey versions.")


def registerPasswordPolicy(site):
    pas = api.portal.get_tool('acl_users')

    # Deactivate the default policy
    for oid in pas.objectIds([PasswordPolicyPlugin.meta_type]):
        if oid in pas.plugins._getPlugins(IValidationPlugin):
            pas.plugins.deactivatePlugin(IValidationPlugin, oid)

    # Activate the Euphorie policy
    if not pas.objectIds([EuphoriePasswordPolicy.meta_type]):
        plugin = EuphoriePasswordPolicy(
            EuphoriePasswordPolicy.id,
            EuphoriePasswordPolicy.meta_type
        )
        pas._setObject(plugin.getId(), plugin)
        plugin = getattr(pas, plugin.getId())

        infos = [info for info in pas.plugins.listPluginTypeInfo()
            if plugin.testImplements(info["interface"])
        ]
        plugin.manage_activateInterfaces([info["id"] for info in infos])
        for info in infos:
            for i in range(len(pas.plugins.listPluginIds(info["interface"]))):
                pas.plugins.movePluginsUp(info["interface"], [plugin.getId()])
