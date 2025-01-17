"""Add the last_login column to the account table.

Revision ID: 20211019165915
Revises: 20211011114527
Create Date: 2021-10-19 16:59:15.046779
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20211019165915"
down_revision = "20211011114527"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("account", "last_login"):
        op.add_column("account", sa.Column("last_login", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("account", "last_login")
