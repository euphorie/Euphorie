from ftw.upgrade import UpgradeStep


class NotificationsRegistryEntries(UpgradeStep):
    """Notifications registry entries."""

    def __call__(self):
        self.install_upgrade_profile()
