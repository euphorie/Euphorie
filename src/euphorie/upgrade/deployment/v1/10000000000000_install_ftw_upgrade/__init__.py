from ftw.upgrade import UpgradeStep


class InstallFtwUpgrade(UpgradeStep):
    """Install ftw.upgrade."""

    def __call__(self):
        self.ensure_profile_installed("ftw.upgrade:default")
