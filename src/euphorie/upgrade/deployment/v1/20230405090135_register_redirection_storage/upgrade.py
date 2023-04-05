from ftw.upgrade import UpgradeStep


class RegisterRedirectionStorage(UpgradeStep):
    """Register redirection storage."""

    def __call__(self):
        self.install_upgrade_profile()
