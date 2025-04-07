"""Add content type: choice

Revision ID: 20250402124248
Revises: 20240419142030
Create Date: 2025-04-02 16:39:06.474435

"""
from alembic import op
from euphorie.deployment.upgrade.utils import has_table

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20250402124248"
down_revision = "20240419142030"
branch_labels = None
depends_on = None


def upgrade():
    if not has_table("choice"):
        op.create_table(
            "choice",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("condition", sa.String(length=512), nullable=True),
            sa.ForeignKeyConstraint(
                ["id"], ["tree.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    if not has_table("option"):
        op.create_table(
            "option",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("choice_id", sa.Integer(), nullable=False),
            sa.Column("zodb_path", sa.String(length=512), nullable=False),
            sa.ForeignKeyConstraint(
                ["choice_id"], ["choice.id"], onupdate="CASCADE", ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade():
    if has_table("choice"):
        op.drop_table("choice")
    if has_table("option"):
        op.drop_table("option")
