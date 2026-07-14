from collective.ftw.upgrade import UpgradeStep


class InstallTheNewRegistryRecordToCustomizeTheDisplayOfTheClient(UpgradeStep):
    """Install the new registry record to customize the display of the client."""

    def __call__(self):
        self.install_upgrade_profile()
