from collective.ftw.upgrade import UpgradeStep
from euphorie.deployment.upgrade.utils import alembic_upgrade_to


class AddNotificationTables(UpgradeStep):
    """Add notification tables."""

    def __call__(self):
        self.install_upgrade_profile()
        alembic_upgrade_to(self.target_version)
