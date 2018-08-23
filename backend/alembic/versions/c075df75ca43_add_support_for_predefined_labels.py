"""Add support for Predefined Labels

Revision ID: c075df75ca43
Revises: 0707294d0a96
Create Date: 2018-08-22 23:07:17.644379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c075df75ca43'
down_revision = '0707294d0a96'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Labels', sa.Column('predefined', sa.Boolean(), nullable=False, server_default='f'))


def downgrade():
    op.drop_column('Labels', 'predefined')
