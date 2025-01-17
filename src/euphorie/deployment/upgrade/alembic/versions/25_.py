"""Empty message.

Revision ID: 25
Revises: 24
Create Date: 2019-12-04 11:58:00.148524
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "25"
down_revision = "24"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("account", "created"):
        op.add_column("account", sa.Column("created", sa.DateTime(), nullable=True))
        op.execute("UPDATE account set account_type='full' WHERE account_type is Null")


def downgrade():
    op.drop_column("account", "created")
