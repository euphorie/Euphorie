"""Add a timestamp to the company table.

Revision ID: 20210409113814
Revises: 29
Create Date: 2021-04-09 11:58:37.115736
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20210409113814"
down_revision = "29"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("company", "timestamp"):
        op.add_column("company", sa.Column("timestamp", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column("company", "timestamp")
