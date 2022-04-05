"""empty message

Revision ID: 20220330153448
Revises: 20211019165915
Create Date: 2022-03-30 15:54:39.081724

"""
from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20220330153448"
down_revision = "20211019165915"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "membership",
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("member_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["member_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["account.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("owner_id"),
    )
    op.create_index(
        op.f("ix_membership_member_id"), "membership", ["member_id"], unique=False
    )
    op.create_index(
        op.f("ix_membership_owner_id"), "membership", ["owner_id"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_membership_owner_id"), table_name="membership")
    op.drop_index(op.f("ix_membership_member_id"), table_name="membership")
    op.drop_table("membership")
