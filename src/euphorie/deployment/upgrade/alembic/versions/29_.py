"""empty message

Revision ID: 29
Revises: 28
Create Date: 2020-12-02 09:32:52.283455

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "29"
down_revision = "28"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("group", sa.Column("active", sa.Boolean(), nullable=True))
    op.execute("""UPDATE "group" set active=True""")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("group", "active")
    # ### end Alembic commands ###