from ftw.upgrade import UpgradeStep


class Make_KeepMeLoggedIn_checkboxOptional(UpgradeStep):
    """Make 'Keep me logged in' checkbox optional."""

    def __call__(self):
        self.install_upgrade_profile()
