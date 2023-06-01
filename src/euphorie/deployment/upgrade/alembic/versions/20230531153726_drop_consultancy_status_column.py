"""Drop consultancy status column

Revision ID: 20230531153726
Revises: 20230515143459
Create Date: 2023-05-31 15:41:06.990714

"""
from alembic import op
from euphorie.deployment.upgrade.utils import has_column

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20230531153726"
down_revision = "20230515143459"
branch_labels = None
depends_on = None


def upgrade():
    if has_column("consultancy", "status"):
        op.drop_column("consultancy", "status")


def downgrade():
    if not has_column("consultancy", "status"):
        op.add_column(
            "consultancy",
            sa.Column(
                "status", sa.VARCHAR(length=255), autoincrement=False, nullable=True
            ),
        )
