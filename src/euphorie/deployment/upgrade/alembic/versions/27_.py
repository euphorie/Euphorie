"""Empty message.

Revision ID: 27
Revises: 26
Create Date: 2020-03-04 10:51:17.559416
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "27"
down_revision = "26"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("action_plan", "action"):
        op.add_column(
            "action_plan", sa.Column("action", sa.UnicodeText(), nullable=True)
        )
    if not has_column("action_plan", "solution_id"):
        op.add_column(
            "action_plan", sa.Column("solution_id", sa.String(length=20), nullable=True)
        )
    if not has_column("action_plan", "plan_type"):
        op.add_column(
            "action_plan", sa.Column("plan_type", sa.String(length=20), nullable=True)
        )
        op.create_index(
            op.f("ix_action_plan_plan_type"), "action_plan", ["plan_type"], unique=False
        )
        op.execute("UPDATE action_plan SET plan_type = 'measure_custom'")
        op.execute(
            """
UPDATE action_plan ap
    SET "action" = CASE
    WHEN ap.prevention_plan is not NULL
    THEN ap.action_plan || E'\n' || ap.prevention_plan
    ELSE ap.action_plan END"""
        )
        op.alter_column("action_plan", "plan_type", nullable=False)

    if not has_column("session", "migrated"):
        op.add_column("session", sa.Column("migrated", sa.DateTime(), nullable=True))


def downgrade():
    op.drop_index(op.f("ix_action_plan_plan_type"), table_name="action_plan")
    op.drop_column("action_plan", "solution_id")
    op.drop_column("action_plan", "plan_type")
    op.drop_column("action_plan", "action")
    op.drop_column("session", "migrated")
