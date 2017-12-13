"""Change Label structure

Revision ID: fcf5d0ba4bca
Revises: 97bce257b460
Create Date: 2017-10-29 17:26:31.227393

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fcf5d0ba4bca'
down_revision = '97bce257b460'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('LabelSelections',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('position_x', sa.Float(), nullable=False),
        sa.Column('position_y', sa.Float(), nullable=False),
        sa.Column('position_z', sa.Float(), nullable=False),
        sa.Column('shape_width', sa.Float(), nullable=False),
        sa.Column('shape_height', sa.Float(), nullable=False),
        sa.Column('label_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['label_id'], ['Labels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('Labels', 'position_x')
    op.drop_column('Labels', 'position_z')
    op.drop_column('Labels', 'position_y')
    op.drop_column('Labels', 'shape_height')
    op.drop_column('Labels', 'shape_depth')
    op.drop_column('Labels', 'shape_width')


def downgrade():
    op.add_column('Labels', sa.Column('shape_width', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('Labels', sa.Column('shape_depth', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('Labels', sa.Column('shape_height', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('Labels', sa.Column('position_y', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('Labels', sa.Column('position_z', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('Labels', sa.Column('position_x', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_table('LabelSelections')
