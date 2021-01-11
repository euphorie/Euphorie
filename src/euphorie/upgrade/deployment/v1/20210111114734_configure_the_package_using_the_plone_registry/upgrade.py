from ftw.upgrade import UpgradeStep


class ConfigureThePackageUsingThePloneRegistry(UpgradeStep):
    """Configure the package using the plone registry."""

    def __call__(self):
        self.install_upgrade_profile()
