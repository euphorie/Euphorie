"""Add content type: choice

Revision ID: 20250402124248
Revises: 20240419142030
Create Date: 2025-04-02 16:39:06.474435

"""

# revision identifiers, used by Alembic.
revision = "20250402124248"
down_revision = "20240419142030"
branch_labels = None
depends_on = None


def upgrade():
    """This is a noop upgrade, the content type "choice" is not relevant for regular
    Euphorie but only for the installations that have dsetool.policy"""
    pass


def downgrade():
    """This is a noop upgrade, the content type "choice" is not relevant for regular
    Euphorie but only for the installations that have dsetool.policy"""
    pass
