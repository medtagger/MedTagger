"""Add description and label examples for Task

Revision ID: e7b5c96cdde6
Revises: c075df75ca43
Create Date: 2019-05-22 22:05:26.235486

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e7b5c96cdde6'
down_revision = 'c075df75ca43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Tasks', sa.Column('description', sa.String(length=500), server_default='', nullable=True))
    op.add_column('Tasks', sa.Column('label_examples', postgresql.ARRAY(sa.String(length=50)), server_default='{}',
                                     nullable=True))


def downgrade():
    op.drop_column('Tasks', 'label_examples')
    op.drop_column('Tasks', 'description')
