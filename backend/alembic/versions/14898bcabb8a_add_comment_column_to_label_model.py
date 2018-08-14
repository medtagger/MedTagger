"""Add comment column to Label model

Revision ID: 14898bcabb8a
Revises: 9c615d167588
Create Date: 2018-07-11 08:38:47.487875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14898bcabb8a'
down_revision = '9c615d167588'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Labels', sa.Column('comment', sa.String(), nullable=True))


def downgrade():
    op.drop_column('Labels', 'comment')
