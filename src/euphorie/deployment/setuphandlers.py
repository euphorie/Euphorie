from euphorie.content.passwordpolicy import EuphoriePasswordPolicy
from euphorie.content.utils import REGION_NAMES
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.PlonePAS.plugins.passwordpolicy import PasswordPolicyPlugin
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from zope.interface import alsoProvides

import logging


log = logging.getLogger(__name__)


def setupVarious(context):
    site = api.portal.get()
    disableRedirectTracking(site)
    setupInitialContent(site)
    setupVersioning(site)
    registerPasswordPolicy(site)
    setupSecureSessionCookie(site)


COUNTRIES = {
    "at": ("Austria", "eu-member"),
    "be": ("Belgium", "eu-member"),
    "bg": ("Bulgaria", "eu-member"),
    "se": ("Sweden", "eu-member"),
    "cy": ("Cyprus", "eu-member"),
    "cz": ("The Czech Republic", "eu-member"),
    "de": ("Germany", "eu-member"),
    "dk": ("Denmark", "eu-member"),
    "ee": ("Estonia", "eu-member"),
    "es": ("Spain", "eu-member"),
    "fi": ("Finland", "eu-member"),
    "fr": ("France", "eu-member"),
    "gb": ("The United Kingdom", "eu-member"),
    "gr": ("Greece", "eu-member"),
    "hu": ("Hungary", "eu-member"),
    "ie": ("Ireland", "eu-member"),
    "it": ("Italy", "eu-member"),
    "lt": ("Lithuania", "eu-member"),
    "lu": ("Luxembourg", "eu-member"),
    "lv": ("Latvia", "eu-member"),
    "mt": ("Malta", "eu-member"),
    "nl": ("The Netherlands", "eu-member"),
    "pl": ("Poland", "eu-member"),
    "pt": ("Portugal", "eu-member"),
    "ro": ("Romania", "eu-member"),
    "sk": ("Slovakia", "eu-member"),
    "si": ("Slovenia", "eu-member"),
    "li": ("Liechtenstein", "efta"),
    "no": ("Norway", "efta"),
    "ch": ("Switzerland", "efta"),
    "hr": ("Republic of Croatia", "candidate-eu"),
    "is": ("Republic of Iceland", "candidate-eu"),
    "mk": ("F.Y.R. Macedonia", "candidate-eu"),
    "me": ("Montenegro", "candidate-eu"),
    "tr": ("Republic of Turkey", "candidate-eu"),
    "al": ("Republic of Albania", "potential-candidate-eu"),
    "ba": ("Bosnia and Herzegovina", "potential-candidate-eu"),
    "cs": ("Kosovo", "potential-candidate-eu"),
    "rs": ("Republic of Serbia", "potential-candidate-eu"),
}

for i in REGION_NAMES.items():
    COUNTRIES[i[0]] = (i[1], "region")


def setupInitialContent(site):
    present = site.objectIds()
    for obj in ["Members", "events", "news"]:
        if obj in present:
            site.manage_delObjects([obj])
            log.info("Removed default Plone %s folder", obj)

    if "sectors" not in present:
        site.invokeFactory(
            "euphorie.sectorcontainer",
            "sectors",
            title="Surveys",
        )
        mt = getToolByName(site, "portal_membership")
        mt.setMembersFolderById("sectors")
        log.info("Added sectors folder")

    sectors = site.sectors
    for country_id, info in COUNTRIES.items():
        (title, country_type) = info
        if country_id not in sectors:
            sectors.invokeFactory(
                "euphorie.country",
                country_id,
                title=title,
                country_type=country_type,
            )
            log.info("Added country %s (%s)", country_id, title)
        country = sectors[country_id]
        if "help" not in country:
            createContentInContainer(
                country,
                "euphorie.page",
                id="help",
                title="Help",
                checkConstraints=False,
            )
            log.info("Added help section for country %s (%s)", country_id, title)
        help = country["help"]
        if not INavigationRoot.providedBy(help):
            alsoProvides(help, INavigationRoot)
            log.info(
                "Made help for country %s (%s) a navigation root.",
                country_id,
                title,
            )

    if "client" not in present:
        site.invokeFactory("euphorie.client", "client", title="Client")
        api.content.transition(site.client, to_state="published")
        log.info("Added Euphorie client instance")

    if "documents" not in present:
        site.invokeFactory("euphorie.folder", "documents", title="Documents")
        log.info("Added documents folder")
    documents = site.documents

    if not INavigationRoot.providedBy(documents):
        alsoProvides(documents, INavigationRoot)
        log.info("Made documentation folder a navigation root.")

    lt = getToolByName(site, "portal_languages")
    present_languages = documents.objectIds()
    for code, name in lt.listSupportedLanguages():
        if code not in present_languages:
            documents.invokeFactory(
                "euphorie.documentation",
                code,
                title=name,
            )
            log.info("Added documentation folder for %s (%s)", name, code)
        docs = documents[code]
        if "help" not in docs:
            createContentInContainer(
                docs,
                "euphorie.help",
                id="help",
                checkConstraints=False,
            )
            log.info("Added online help text for language %s (%s)", name, code)
        if "appendix" not in docs:
            _createObjectByType(
                "euphorie.page",
                docs,
                "appendix",
                title="Appendix",
            )
            log.info("Added appendix folder for language %s (%s)", name, code)


def disableRedirectTracking(site):
    # Add additional setup code here
    from plone.app.redirector.interfaces import IRedirectionStorage
    from zope.component import getSiteManager
    from zope.interface.interfaces import IComponentRegistry

    sm = getSiteManager(site)
    if sm is None or not IComponentRegistry.providedBy(sm):
        log.warning(
            "Failed to find a site manager, can not remove "
            "IRedirectionStorage utility"
        )
        return

    sm.unregisterUtility(provided=IRedirectionStorage)


def setupVersioning(site):
    repository = site.portal_repository
    if "euphorie.survey" not in repository.getVersionableContentTypes():
        repository.setVersionableContentTypes(["euphorie.survey"])
        log.info("Enabled versioning for survey versions.")


def registerPasswordPolicy(site):
    pas = api.portal.get_tool("acl_users")

    # Deactivate the default policy
    for oid in pas.objectIds([PasswordPolicyPlugin.meta_type]):
        if oid in pas.plugins._getPlugins(IValidationPlugin):
            pas.plugins.deactivatePlugin(
                IValidationPlugin,
                oid,
            )

    # Activate the Euphorie policy
    if not pas.objectIds([EuphoriePasswordPolicy.meta_type]):
        plugin = EuphoriePasswordPolicy(
            EuphoriePasswordPolicy.id,
            EuphoriePasswordPolicy.meta_type,
        )
        pas._setObject(plugin.getId(), plugin)
        plugin = getattr(pas, plugin.getId())

        infos = [
            info
            for info in pas.plugins.listPluginTypeInfo()
            if plugin.testImplements(info["interface"])
        ]
        plugin.manage_activateInterfaces([info["id"] for info in infos])
        for info in infos:
            for i in range(len(pas.plugins.listPluginIds(info["interface"]))):
                pas.plugins.movePluginsUp(
                    info["interface"],
                    [plugin.getId()],
                )


def setupSecureSessionCookie(site):
    session = api.portal.get_tool("acl_users").get("session")
    if not session:
        return
    if not session.secure:
        session.secure = True
