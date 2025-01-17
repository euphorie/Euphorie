"""Remove the completion_percentage column.

Revision ID: 20220705145832
Revises: 20220620103222
Create Date: 2022-07-05 14:55:08.235238
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20220705145832"
down_revision = "20220620103222"
branch_labels = None
depends_on = None


def upgrade():
    if has_column("session", "completion_percentage"):
        op.drop_column("session", "completion_percentage")


def downgrade():
    op.add_column(
        "session",
        sa.Column(
            "completion_percentage", sa.INTEGER(), autoincrement=False, nullable=True
        ),
    )
