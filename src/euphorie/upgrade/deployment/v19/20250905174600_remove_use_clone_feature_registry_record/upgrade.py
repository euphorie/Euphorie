from ftw.upgrade import UpgradeStep


class RemoveCloneFeatureFlag(UpgradeStep):
    """Remove clone feature flag, which is always on now."""

    def __call__(self):
        self.install_upgrade_profile()
