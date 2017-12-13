"""Add Scan and Slices

Revision ID: 8ddc17b0b877
Revises: 029e431a31ea
Create Date: 2017-10-29 02:16:59.766660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ddc17b0b877'
down_revision = '029e431a31ea'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Scans',
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Slices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('location', sa.Float(), nullable=False),
        sa.Column('position_x', sa.Float(), nullable=False),
        sa.Column('position_y', sa.Float(), nullable=False),
        sa.Column('position_z', sa.Float(), nullable=False),
        sa.Column('scan_id', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['scan_id'], ['Scans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Slices')
    op.drop_table('Scans')
