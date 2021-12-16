from ftw.upgrade import UpgradeStep


class ToggleForSelfRegistration(UpgradeStep):
    """Toggle for self registration."""

    def __call__(self):
        self.install_upgrade_profile()
