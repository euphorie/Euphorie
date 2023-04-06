from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class AddSessionRedirect(UpgradeStep):
    """Add session redirect."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
