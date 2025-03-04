from ftw.upgrade import UpgradeStep


class AddANewRegistryRecordToServeHelpPagesFromARemoteServer(UpgradeStep):
    """Add a new registry record to serve help pages from a remote server."""

    def __call__(self):
        self.install_upgrade_profile()
