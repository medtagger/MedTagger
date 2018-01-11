"""Fix

Revision ID: e3cf6b7115ec
Revises: 1fba3df23f8b
Create Date: 2017-12-13 09:18:05.896837

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e3cf6b7115ec'
down_revision = '1fba3df23f8b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Slices', sa.Column('converted', sa.Boolean(), nullable=True))
    op.add_column('Slices', sa.Column('stored', sa.Boolean(), nullable=True))
    op.alter_column('Slices', 'location',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('Slices', 'position_x',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('Slices', 'position_y',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('Slices', 'position_z',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)


def downgrade():
    op.alter_column('Slices', 'position_z',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('Slices', 'position_y',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('Slices', 'position_x',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('Slices', 'location',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.drop_column('Slices', 'stored')
    op.drop_column('Slices', 'converted')
