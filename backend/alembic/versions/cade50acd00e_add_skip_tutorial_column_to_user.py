"""Add skip_tutorial column to user

Revision ID: cade50acd00e
Revises: 75a3481c4d0c
Create Date: 2018-04-30 19:45:05.100029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cade50acd00e'
down_revision = '75a3481c4d0c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Users', sa.Column('skip_tutorial', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('Users', 'skip_tutorial')
