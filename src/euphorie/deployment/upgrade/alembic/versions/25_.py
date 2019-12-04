"""empty message

Revision ID: 25
Revises: 24
Create Date: 2019-12-04 11:58:00.148524

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '25'
down_revision = '24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('created', sa.DateTime(), nullable=True))
    op.execute("UPDATE account set account_type='full' WHERE account_type is Null")
    op.add_column('group', sa.Column('brand', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'brand')
    op.drop_column('account', 'created')
    # ### end Alembic commands ###
