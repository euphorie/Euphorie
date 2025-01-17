"""Create the organisation_membership table.

Revision ID: 20220720110538
Revises: 20220705145832
Create Date: 2022-04-01 14:22:44.091422
"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20220720110538"
down_revision = "20220705145832"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("organisation_membership"):
        op.create_table(
            "organisation_membership",
            sa.Column(
                "organisation_id", sa.Integer(), autoincrement=True, nullable=False
            ),
            sa.Column("owner_id", sa.Integer(), nullable=False),
            sa.Column("member_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ["member_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["owner_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("organisation_id"),
        )

    if not has_column("organisation_membership", "member_role"):
        op.add_column(
            "organisation_membership",
            sa.Column("member_role", sa.UnicodeText(), nullable=True),
        )

    if not has_table("organisation"):
        op.create_table(
            "organisation",
            sa.Column(
                "organisation_id", sa.Integer(), autoincrement=True, nullable=False
            ),
            sa.Column("owner_id", sa.Integer(), nullable=False),
            sa.Column("title", sa.UnicodeText(), nullable=True),
            sa.Column("image_data", sa.LargeBinary(), nullable=True),
            sa.Column("image_data_scaled", sa.LargeBinary(), nullable=True),
            sa.Column("image_filename", sa.UnicodeText(), nullable=True),
            sa.ForeignKeyConstraint(
                ["owner_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("organisation_id"),
        )


def downgrade():
    if has_table("organisation"):
        op.drop_table("organisation")
    if has_table("organisation_membership"):
        op.drop_table("organisation_membership")
