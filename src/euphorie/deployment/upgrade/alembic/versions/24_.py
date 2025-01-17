"""Try to add an image binary column and an image_filename column to the risk
table Also add column "refreshed" to the session table and copy data from
modified.

Revision ID: 24
Revises:
Create Date: 2019-09-09 10:24:51.539339
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("risk", "image_data"):
        op.add_column("risk", sa.Column("image_data", sa.LargeBinary(), nullable=True))
    if not has_column("risk", "image_data_scaled"):
        op.add_column(
            "risk", sa.Column("image_data_scaled", sa.LargeBinary(), nullable=True)
        )
    if not has_column("risk", "image_filename"):
        op.add_column(
            "risk", sa.Column("image_filename", sa.UnicodeText(), nullable=True)
        )
    if not has_column("session", "refreshed"):
        op.add_column("session", sa.Column("refreshed", sa.DateTime(), nullable=True))
        op.execute("UPDATE session SET refreshed = modified")


def downgrade():
    op.drop_column("risk", "image_data")
    op.drop_column("risk", "image_data_scaled")
    op.drop_column("risk", "image_filename")
    op.drop_column("session", "refreshed")
