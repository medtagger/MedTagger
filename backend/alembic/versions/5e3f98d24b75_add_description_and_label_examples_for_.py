"""Add description and label examples for Task

Revision ID: 5e3f98d24b75
Revises: c075df75ca43
Create Date: 2019-05-24 21:58:51.753199

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5e3f98d24b75'
down_revision = 'c075df75ca43'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Tasks', sa.Column('description', sa.Text(), server_default='', nullable=True))
    op.add_column('Tasks', sa.Column('label_examples', postgresql.ARRAY(sa.String(length=256)),
                                     server_default='{}', nullable=True))


def downgrade():
    op.drop_column('Tasks', 'label_examples')
    op.drop_column('Tasks', 'description')
