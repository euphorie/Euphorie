from ftw.upgrade import UpgradeStep


class UpdateLanguageSettings(UpgradeStep):
    """Update language settings: use_request_negotiation=True.

    And allow to modify language preferences in the settings panel.
    """

    def __call__(self):
        self.install_upgrade_profile()
