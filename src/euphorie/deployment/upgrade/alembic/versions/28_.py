"""Empty message.

Revision ID: 28
Revises: 27
Create Date: 2020-05-28 12:52:00.626910
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "28"
down_revision = "27"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("action_plan", "used_in_training"):
        op.add_column(
            "action_plan", sa.Column("used_in_training", sa.Boolean(), nullable=True)
        )
        op.create_index(
            op.f("ix_action_plan_used_in_training"),
            "action_plan",
            ["used_in_training"],
            unique=False,
        )
        op.execute(
            "UPDATE action_plan set used_in_training=True "
            "where plan_type in ('in_place_standard', 'in_place_custom')"
        )


def downgrade():
    op.drop_index(op.f("ix_action_plan_used_in_training"), table_name="action_plan")
    op.drop_column("action_plan", "used_in_training")
