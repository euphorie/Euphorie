from ftw.upgrade import UpgradeStep


class FixNavigationInCMS(UpgradeStep):
    """Fix navigation in CMS."""

    def __call__(self):
        self.install_upgrade_profile()
