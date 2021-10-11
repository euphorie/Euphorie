from euphorie.deployment.upgrade.utils import alembic_upgrade_to
from ftw.upgrade import UpgradeStep


class ReworkTheWayInWhichWeAreMarkingGroupsAsActive(UpgradeStep):
    """Rework the way in which we are marking groups as active."""

    def __call__(self):
        alembic_upgrade_to(self.target_version)
