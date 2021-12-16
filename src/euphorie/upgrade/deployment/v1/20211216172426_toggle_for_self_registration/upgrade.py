from ftw.upgrade import UpgradeStep


class ToggleForSelfRegistration(UpgradeStep):
    """Allow self registration by default."""

    def __call__(self):
        self.install_upgrade_profile()
