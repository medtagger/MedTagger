"""Add disabled flags

Revision ID: 0707294d0a96
Revises: 3f2c98c1710b
Create Date: 2018-08-03 20:51:00.650220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0707294d0a96'
down_revision = '3f2c98c1710b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ScanCategories', sa.Column('disabled', sa.Boolean(), nullable=False, server_default='f'))


def downgrade():
    op.drop_column('ScanCategories', 'disabled')
