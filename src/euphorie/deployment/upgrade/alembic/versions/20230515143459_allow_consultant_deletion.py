"""Allow consultant deletion.

Revision ID: 20230515143459
Revises: 20230504061955
Create Date: 2023-05-15 14:36:08.134660
"""

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20230515143459"
down_revision = "20230504061955"
branch_labels = None
depends_on = None


def upgrade():
    try:
        op.alter_column(
            "consultancy", "account_id", existing_type=sa.INTEGER(), nullable=True
        )
        op.drop_constraint(
            "consultancy_account_id_fkey", "consultancy", type_="foreignkey"
        )
        op.create_foreign_key(
            None,
            "consultancy",
            "account",
            ["account_id"],
            ["id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        )
    except Exception:
        # SQLite
        pass


def downgrade():
    op.drop_constraint(None, "consultancy", type_="foreignkey")
    op.create_foreign_key(
        "consultancy_account_id_fkey",
        "consultancy",
        "account",
        ["account_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    op.alter_column(
        "consultancy", "account_id", existing_type=sa.INTEGER(), nullable=False
    )
