from euphorie.deployment.upgrade.utils import alembic_upgrade_to

import logging


log = logging.getLogger(__name__)


def alembic_upgrade(context):
    alembic_upgrade_to("28")
