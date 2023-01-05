from euphorie.deployment.upgrade.utils import alembic_upgrade
from ftw.upgrade import UpgradeStep


class UpgradeToAlembicHead(UpgradeStep):
    """Create the OrganisationMembership table."""

    def __call__(self):
        alembic_upgrade()
