from ftw.upgrade import UpgradeStep


class UpdateLanguageSettings(UpgradeStep):
    """Update language settings: use_request_negotiation=True."""

    def __call__(self):
        self.install_upgrade_profile()
