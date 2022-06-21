"""empty message

Revision ID: 20220620103222
Revises: 20220318135716
Create Date: 2022-06-20 10:33:43.713596

"""
from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20220620103222"
down_revision = "20220318135716"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("account", sa.Column("first_name", sa.Unicode(), nullable=True))
    op.add_column("account", sa.Column("last_name", sa.Unicode(), nullable=True))


def downgrade():
    op.drop_column("account", "last_name")
    op.drop_column("account", "first_name")
