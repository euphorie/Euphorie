from ftw.upgrade import UpgradeStep


class RemoveTheEuphorieSmartprintngUrlRecord(UpgradeStep):
    """Remove the euphorie.smartprintng_url record."""

    def __call__(self):
        self.install_upgrade_profile()
