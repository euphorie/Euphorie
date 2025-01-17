"""Empty message.

Revision ID: 20231019121221
Revises: 20230515143459
Create Date: 2023-10-19 17:58:47.014626
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20231019121221"
down_revision = "20230515143459"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("notification_subscription"):
        op.create_table(
            "notification_subscription",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("account_id", sa.Integer(), nullable=False),
            sa.Column("category", sa.String(length=512), nullable=False),
            sa.Column("enabled", sa.Boolean(), nullable=False, default=False),
            sa.ForeignKeyConstraint(
                ["account_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade():
    op.drop_table("notification_subscription")
