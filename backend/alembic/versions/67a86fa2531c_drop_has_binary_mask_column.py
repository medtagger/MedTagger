"""Drop has_binary_mask column

Revision ID: 67a86fa2531c
Revises: 7995a5e4f811
Create Date: 2018-05-05 18:21:51.040723

"""
from alembic import op
import sqlalchemy as sa

revision = '67a86fa2531c'
down_revision = '7995a5e4f811'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('LabelElements', 'has_binary_mask')


def downgrade():
    op.add_column('LabelElements', sa.Column('has_binary_mask', sa.Boolean(), nullable=True))
