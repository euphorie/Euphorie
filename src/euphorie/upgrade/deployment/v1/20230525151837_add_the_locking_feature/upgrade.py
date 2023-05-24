from ftw.upgrade import UpgradeStep
from plone import api


class AddTheLockingFeature(UpgradeStep):
    """Add the locking feature."""

    def __call__(self):
        self.install_upgrade_profile()
        old_value = api.portal.get_registry_record(
            "euphorie.use_publication_feature", default=False
        )
        api.portal.set_registry_record("euphorie.use_locking_feature", old_value)
