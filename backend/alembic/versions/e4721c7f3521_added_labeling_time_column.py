"""Added labeling time column

Revision ID: e4721c7f3521
Revises: 4e93b463a357
Create Date: 2018-03-10 02:09:46.573999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4721c7f3521'
down_revision = '4e93b463a357'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Labels', sa.Column('labeling_time', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('Labels', 'labeling_time')
