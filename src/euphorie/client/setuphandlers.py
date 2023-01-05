from euphorie.client.authentication import addEuphorieAccountPlugin
from euphorie.client.authentication import EuphorieAccountPlugin
from plone import api

import logging


log = logging.getLogger(__name__)


def enable_plugin_and_move_to_top(pas, plugin):
    infos = [
        info
        for info in pas.plugins.listPluginTypeInfo()
        if plugin.testImplements(info["interface"])
    ]
    plugin.manage_activateInterfaces([info["id"] for info in infos])
    for info in infos:
        for i in range(len(pas.plugins.listPluginIds(info["interface"]))):
            pas.plugins.movePluginsUp(info["interface"], [plugin.getId()])


def add_account_plugin(pas):
    addEuphorieAccountPlugin(pas, "euphorie", "Euphorie account manager")
    enable_plugin_and_move_to_top(pas, pas.euphorie)


def setupVarious(context):
    site = api.portal.get()
    pas = site.acl_users
    if not pas.objectIds([EuphorieAccountPlugin.meta_type]):
        add_account_plugin(pas)
    ppr = api.portal.get_tool("portal_password_reset")
    ppr.setExpirationTimeout(0.5)
