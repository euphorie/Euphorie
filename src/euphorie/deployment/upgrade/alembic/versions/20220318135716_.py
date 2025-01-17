"""Add the training table.

Revision ID: 20220318135716
Revises: 20211019165915
Create Date: 2022-03-18 14:06:17.384922
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20220318135716"
down_revision = "20211019165915"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("training"):
        op.create_table(
            "training",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("time", sa.DateTime(), nullable=True),
            sa.Column("account_id", sa.Integer(), nullable=False),
            sa.Column("session_id", sa.Integer(), nullable=False),
            sa.Column("answers", sa.Unicode(), nullable=True),
            sa.Column("status", sa.Unicode(), nullable=True),
            sa.ForeignKeyConstraint(
                ["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["session_id"], ["session.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade():
    op.drop_table("training")
