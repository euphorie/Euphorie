from alembic import command
from alembic import op
from alembic.config import Config
from euphorie.client.model import Session
from logging import getLogger
from pkg_resources import resource_filename
from sqlalchemy import inspect
from zope.deprecation import deprecate


logger = getLogger(__name__)


def has_table(name):
    """Utility function that can be used in alembic upgrades to check if a
    table exists."""
    return name in inspect(op.get_bind()).get_table_names()


def has_column(table_name, column_name):
    """Utility function that can be used in alembic upgrades to check if a
    column exists."""
    bind = op.get_bind()
    columns = inspect(bind).get_columns(table_name)
    return any(column["name"] == column_name for column in columns)


def alembic_upgrade():
    """Upgrade the database to the alembic head."""
    script_location = resource_filename("euphorie.deployment.upgrade", "alembic")
    url = Session().bind.engine.url.__to_string__(hide_password=False)
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", url)
    command.upgrade(alembic_cfg, "head")


@deprecate(
    "Use alembic_upgrade() to reach the head alembic revision",
)
def alembic_upgrade_to(revision):
    script_location = resource_filename("euphorie.deployment.upgrade", "alembic")
    url = Session().bind.engine.url.__to_string__(hide_password=False)
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", url)
    try:
        command.upgrade(alembic_cfg, revision)
    except Exception:
        logger.exception(
            "Migration failed, you might need to adapt the script to match "
            "your DB state"
        )
