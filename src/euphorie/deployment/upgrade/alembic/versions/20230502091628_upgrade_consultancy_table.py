"""Upgrade consultancy table

Revision ID: 20230502091628
Revises: 20230421141443
Create Date: 2023-05-02 09:24:29.093386

"""

from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20230502091628"
down_revision = "20230421141443"
branch_labels = None
depends_on = None


def upgrade():
    if not has_column("consultancy", "status"):
        op.add_column(
            "consultancy", sa.Column("status", sa.Unicode(length=255), nullable=True)
        )


def downgrade():
    if has_column("consultancy", "status"):
        op.drop_column("consultancy", "status")
