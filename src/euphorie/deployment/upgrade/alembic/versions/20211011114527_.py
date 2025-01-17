"""The boolean active column becomes the deactivated date time column.

Revision ID: 20211011114527
Revises: 20210409113814
Create Date: 2021-10-11 09:45:27.876273
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20211011114527"
down_revision = "20210409113814"
branch_labels = None
depends_on = None


def upgrade():
    """The boolean active column becomes the deactivated date time column."""
    if not has_column("group", "deactivated"):
        op.add_column("group", sa.Column("deactivated", sa.DateTime(), nullable=True))
        op.execute(
            """UPDATE "group" SET deactivated = '1970-01-01' WHERE active = FALSE"""
        )
    if has_column("group", "active"):
        op.drop_column("group", "active")


def downgrade():
    op.add_column(
        "group", sa.Column("active", sa.BOOLEAN(), autoincrement=False, nullable=True)
    )
    op.execute("""UPDATE "group" SET active = TRUE WHERE deactivated IS NULL""")
    op.execute("""UPDATE "group" SET active = FALSE WHERE deactivated IS NOT NULL""")
    op.drop_column("group", "deactivated")
