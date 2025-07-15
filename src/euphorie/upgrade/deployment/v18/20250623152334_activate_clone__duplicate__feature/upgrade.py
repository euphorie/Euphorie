from ftw.upgrade import UpgradeStep


class ActivateClone_duplicate_feature(UpgradeStep):
    """Activate clone (duplicate) feature."""

    def __call__(self):
        self.install_upgrade_profile()
