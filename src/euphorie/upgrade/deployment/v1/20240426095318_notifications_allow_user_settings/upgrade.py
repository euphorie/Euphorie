from ftw.upgrade import UpgradeStep


class NotificationsAllowUserSettings(UpgradeStep):
    """Notifications allow user settings."""

    def __call__(self):
        self.install_upgrade_profile()
