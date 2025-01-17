"""Add session redirect

Revision ID: 20230406070728
Revises: 20220720110538
Create Date: 2023-04-06 07:15:08.783635

"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20230406070728"
down_revision = "20220720110538"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("session_redirect"):
        op.create_table(
            "session_redirect",
            sa.Column("old_session_id", sa.Integer(), nullable=False),
            sa.Column("new_session_id", sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint("old_session_id"),
        )


def downgrade():
    if has_table("session_redirect"):
        op.drop_table("session_redirect")
