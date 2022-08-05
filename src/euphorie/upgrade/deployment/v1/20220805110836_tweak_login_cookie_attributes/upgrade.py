from euphorie.client.setuphandlers import set_up_session_plugin
from ftw.upgrade import UpgradeStep
from plone import api


class TweakLoginCookieAttributes(UpgradeStep):
    """Tweak login cookie attributes."""

    def __call__(self):
        self.install_upgrade_profile()
        site = api.portal.get()
        pas = site.acl_users
        set_up_session_plugin(pas)
