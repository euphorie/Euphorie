from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class AddLastLoginColumn(UpgradeStep):
    """Add the last_login column to the account table."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
