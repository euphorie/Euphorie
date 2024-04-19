from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class AddTheScaledAnswerColumn(UpgradeStep):
    """Add the scaled_answer column."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
