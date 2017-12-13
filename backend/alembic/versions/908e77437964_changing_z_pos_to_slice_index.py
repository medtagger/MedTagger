"""Changing z pos to slice_index

Revision ID: 908e77437964
Revises: 89c86722cd62
Create Date: 2017-10-30 18:46:44.390951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '908e77437964'
down_revision = '7672053dd637'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('LabelSelections', 'position_z', new_column_name='slice_index')


def downgrade():
    op.alter_column('LabelSelections', 'slice_index', new_column_name='position_z')
