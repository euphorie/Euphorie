from collective.ftw.upgrade import UpgradeStep
from euphorie.deployment.upgrade.utils import alembic_upgrade


class UpgradeToAlembicHead(UpgradeStep):
    """Create the OrganisationMembership table."""

    def __call__(self):
        alembic_upgrade()
