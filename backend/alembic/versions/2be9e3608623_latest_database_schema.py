"""Latest database schema

Revision ID: 2be9e3608623
Revises: e3cf6b7115ec
Create Date: 2018-01-11 23:39:28.622616

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '2be9e3608623'
down_revision = 'e3cf6b7115ec'
branch_labels = None
depends_on = None

slices_orientation_enum = ENUM('X', 'Y', 'Z', name='slices_orientation_enum', create_type=False)


def upgrade():
    slices_orientation_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('LabelSelections', sa.Column('has_binary_mask', sa.Boolean(), nullable=False))
    op.add_column('Scans', sa.Column('converted', sa.Boolean(), nullable=True))
    op.add_column('Scans', sa.Column('number_of_slices', sa.Integer(), nullable=False))
    op.add_column('Slices', sa.Column('orientation', slices_orientation_enum, nullable=False))


def downgrade():
    op.drop_column('Slices', 'orientation')
    op.drop_column('Scans', 'number_of_slices')
    op.drop_column('Scans', 'converted')
    op.drop_column('LabelSelections', 'has_binary_mask')
    slices_orientation_enum.drop(op.get_bind(), checkfirst=True)
