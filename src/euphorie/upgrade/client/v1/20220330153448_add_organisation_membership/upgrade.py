from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class AddOrganisationMembership(UpgradeStep):
    """Add organisation membership."""

    def __call__(self):
        self.install_upgrade_profile()
        alembic_upgrade_to(self.target_version)
