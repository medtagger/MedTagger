"""Add width and height to Slices

Revision ID: 729cd1e8cde1
Revises: 75a3481c4d0c
Create Date: 2018-05-06 14:32:27.355556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column


# revision identifiers, used by Alembic.
revision = '729cd1e8cde1'
down_revision = '75a3481c4d0c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Slices', sa.Column('height', sa.Integer(), nullable=True))
    op.add_column('Slices', sa.Column('width', sa.Integer(), nullable=True))

    # Fill old data with safe 512x512 (it is impossible to check all images in the DB to fill new values - for now...)
    slices = table('Slices', column('height'), column('width'))
    op.execute(slices.update().values({'height': 512, 'width': 512}))


def downgrade():
    op.drop_column('Slices', 'width')
    op.drop_column('Slices', 'height')
