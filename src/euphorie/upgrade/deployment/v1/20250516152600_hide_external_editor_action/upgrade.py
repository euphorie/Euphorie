from ftw.upgrade import UpgradeStep


class HideExternalEditorAction(UpgradeStep):
    """Hide external editor action.

    And fix its condition to not fail when the `externalEditorEnabled`
    skin script is not available.
    """

    def __call__(self):
        self.install_upgrade_profile()
