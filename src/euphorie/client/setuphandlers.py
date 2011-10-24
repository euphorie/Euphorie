from euphorie.client.authentication import EuphorieAccountPlugin
from euphorie.client.authentication import addEuphorieAccountPlugin
import logging

log = logging.getLogger(__name__)

def setupVarious(context):
    if context.readDataFile('euphorie.client.txt') is None:
        return   

    site=context.getSite()
    pas=site.acl_users
    if not pas.objectIds([EuphorieAccountPlugin.meta_type]):
        addEuphorieAccountPlugin(pas, "euphorie", "Euphorie account manager")
        plugin = pas.euphorie

        infos=[info for info in pas.plugins.listPluginTypeInfo()
               if plugin.testImplements(info["interface"])]
        plugin.manage_activateInterfaces([info["id"] for info in infos])
        for info in infos:
            for i in range(len(pas.plugins.listPluginIds(info["interface"]))):
                pas.plugins.movePluginsUp(info["interface"], ["euphorie"])




