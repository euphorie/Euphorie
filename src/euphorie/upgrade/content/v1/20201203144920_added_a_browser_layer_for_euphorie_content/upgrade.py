from ftw.upgrade import UpgradeStep


class AddedABrowserLayerForEuphorieContent(UpgradeStep):
    """Added a browser layer for euphorie.content."""

    def __call__(self):
        self.install_upgrade_profile()
