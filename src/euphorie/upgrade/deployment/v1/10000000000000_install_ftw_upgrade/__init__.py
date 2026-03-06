from collective.ftw.upgrade import UpgradeStep


class InstallFtwUpgrade(UpgradeStep):
    """Install collective.ftw.upgrade."""

    def __call__(self):
        self.ensure_profile_installed("collective.ftw.upgrade:default")
