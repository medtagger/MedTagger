"""Remove all binary mask related things from SQL

Revision ID: 89c593744804
Revises: ddd21c46f46d
Create Date: 2018-05-05 12:39:22.625929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c593744804'
down_revision = 'ddd21c46f46d'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('LabelSelections', 'has_binary_mask')


def downgrade():
    op.add_column('LabelSelections', sa.Column('has_binary_mask', sa.BOOLEAN(), autoincrement=False,
                                               nullable=False, server_default=sa.literal(False)))
