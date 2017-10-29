"""Add labels

Revision ID: 97bce257b460
Revises: 8ddc17b0b877
Create Date: 2017-10-29 02:59:49.802384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97bce257b460'
down_revision = '8ddc17b0b877'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Labels',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('position_x', sa.Float(), nullable=False),
    sa.Column('position_y', sa.Float(), nullable=False),
    sa.Column('position_z', sa.Float(), nullable=False),
    sa.Column('shape_width', sa.Float(), nullable=False),
    sa.Column('shape_height', sa.Float(), nullable=False),
    sa.Column('shape_depth', sa.Float(), nullable=False),
    sa.Column('scan_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['scan_id'], ['Scans.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Labels')
