"""Add tools array to Label Tag

Revision ID: 3f2c98c1710b
Revises: 617bf951f6a2
Create Date: 2018-07-20 19:40:44.050854

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '3f2c98c1710b'
down_revision = '617bf951f6a2'
branch_labels = None
depends_on = None

# Using existing enum with Label Tools
label_tool_enum = ENUM('RECTANGLE', 'BRUSH', 'POINT', 'CHAIN', name='label_tool', create_type=False)


def upgrade():
    op.add_column('LabelTags', sa.Column('tools', postgresql.ARRAY(label_tool_enum), nullable=True))


def downgrade():
    op.drop_column('LabelTags', 'tools')
