"""Add support for Predefined Labels

Revision ID: c075df75ca43
Revises: 9f2eafdf821e
Create Date: 2018-08-22 23:07:17.644379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c075df75ca43'
down_revision = '9f2eafdf821e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Labels', sa.Column('is_predefined', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('Labels', 'is_predefined')
