from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class AddFirstAndLastNameToUser(UpgradeStep):
    """Add first and last name to user."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
