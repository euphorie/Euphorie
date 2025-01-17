"""Add SessionEvent table

Revision ID: 20230504061955
Revises: 20230502091628
Create Date: 2023-05-04 06:20:23.137551

"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20230504061955"
down_revision = "20230502091628"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("session_event"):
        op.create_table(
            "session_event",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("time", sa.DateTime(), nullable=False),
            sa.Column("account_id", sa.Integer(), nullable=True),
            sa.Column("session_id", sa.Integer(), nullable=False),
            sa.Column("action", sa.Unicode(length=32), nullable=True),
            sa.Column("note", sa.Unicode(), nullable=True),
            sa.ForeignKeyConstraint(["account_id"], ["account.id"], onupdate="CASCADE"),
            sa.ForeignKeyConstraint(
                ["session_id"], ["session.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade():
    if has_table("session_event"):
        op.drop_table("session_event")
