"""Add consultancy table

Revision ID: 20230421141443
Revises: 20230406070728
Create Date: 2023-04-21 14:17:25.526866

"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20230421141443"
down_revision = "20230406070728"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("consultancy"):
        op.create_table(
            "consultancy",
            sa.Column("session_id", sa.Integer(), nullable=False),
            sa.Column("account_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["session_id"], ["session.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
        )


def downgrade():
    if has_table("consultancy"):
        op.drop_table("consultancy")
