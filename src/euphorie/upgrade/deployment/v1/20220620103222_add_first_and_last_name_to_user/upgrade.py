from collective.ftw.upgrade import UpgradeStep
from euphorie.deployment.upgrade.utils import alembic_upgrade_to


class AddFirstAndLastNameToUser(UpgradeStep):
    """Add first and last name to user."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
