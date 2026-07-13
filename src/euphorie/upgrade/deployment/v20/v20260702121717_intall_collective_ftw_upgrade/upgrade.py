from collective.ftw.upgrade import UpgradeStep


class IntallCollectiveFtwUpgrade(UpgradeStep):
    """Intall collective.ftw.upgrade."""

    def __call__(self):
        self.ensure_profile_installed("collective.ftw.upgrade:default")
