from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class AddNotificationTables(UpgradeStep):
    """Add notification tables."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
