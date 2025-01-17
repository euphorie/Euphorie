"""Empty message.

Revision ID: 26
Revises: 25
Create Date: 2020-02-03 15:42:46.758366
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26"
down_revision = "25"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("session", "completion_percentage"):
        op.add_column(
            "session", sa.Column("completion_percentage", sa.Integer(), nullable=True)
        )


def downgrade():
    op.drop_column("session", "completion_percentage")
