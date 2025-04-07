from ftw.upgrade import UpgradeStep


class InstallTheMaintenanceActions(UpgradeStep):
    """Install the maintenance actions."""

    def __call__(self):
        self.install_upgrade_profile()
