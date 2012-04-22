from euphorie.client.authentication import EuphorieAccountPlugin
from euphorie.client.authentication import addEuphorieAccountPlugin
from euphorie.client.api.authentication import EuphorieAPIPlugin
from euphorie.client.api.authentication import addEuphorieAPIPlugin
import logging

log = logging.getLogger(__name__)


def enable_plugin_and_move_to_top(pas, plugin):
    infos = [info for info in pas.plugins.listPluginTypeInfo()
             if plugin.testImplements(info['interface'])]
    plugin.manage_activateInterfaces([info['id'] for info in infos])
    for info in infos:
        for i in range(len(pas.plugins.listPluginIds(info['interface']))):
            pas.plugins.movePluginsUp(info['interface'], [plugin.getId()])

def add_account_plugin(pas):
    addEuphorieAccountPlugin(pas, 'euphorie', 'Euphorie account manager')
    enable_plugin_and_move_to_top(pas, pas.euphorie)


def add_api_authentication_plugin(pas):
    addEuphorieAPIPlugin(pas, 'euphorie_api', 'Euphorie API authentication')
    enable_plugin_and_move_to_top(pas, pas.euphorie_api)


def setupVarious(context):
    if context.readDataFile('euphorie.client.txt') is None:
        return   

    site = context.getSite()
    pas = site.acl_users
    if not pas.objectIds([EuphorieAccountPlugin.meta_type]):
        add_account_plugin(pas)

    if not pas.objectIds([EuphorieAPIPlugin.meta_type]):
        add_api_authentication_plugin(pas)
