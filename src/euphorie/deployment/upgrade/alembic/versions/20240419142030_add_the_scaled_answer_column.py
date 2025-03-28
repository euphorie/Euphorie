"""Add the scaled_answer column to the risk table

Revision ID: 20240419142030
Revises: 20231019121221
Create Date: 2024-04-19 14:19:41.050854

"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20240419142030"
down_revision = "20231019121221"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if not has_column("risk", "scaled_answer"):
        op.add_column(
            "risk", sa.Column("scaled_answer", sa.UnicodeText(), nullable=True)
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if has_column("risk", "scaled_answer"):
        op.drop_column("risk", "scaled_answer")
    # ### end Alembic commands ###
