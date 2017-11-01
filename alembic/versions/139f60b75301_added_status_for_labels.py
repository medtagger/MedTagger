"""Added status for labels

Revision ID: 139f60b75301
Revises: 908e77437964
Create Date: 2017-11-01 19:03:55.009544

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '139f60b75301'
down_revision = '908e77437964'
branch_labels = None
depends_on = None

label_status_enum = ENUM('VALID', 'INVALID', 'NOT_VERIFIED', name='label_status_enum', create_type=False)


def upgrade():
    label_status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('Labels', sa.Column('status', label_status_enum, server_default='NOT_VERIFIED', nullable=False))


def downgrade():
    op.drop_column('Labels', 'status')
    label_status_enum.drop(op.get_bind(), checkfirst=True)
