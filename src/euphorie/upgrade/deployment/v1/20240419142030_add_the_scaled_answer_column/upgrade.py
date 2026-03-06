from collective.ftw.upgrade import UpgradeStep
from euphorie.deployment.upgrade.utils import alembic_upgrade_to


class AddTheScaledAnswerColumn(UpgradeStep):
    """Add the scaled_answer column."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
