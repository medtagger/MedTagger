"""Initial commit

Revision ID: 029e431a31ea
Revises: 
Create Date: 2017-10-28 21:39:11.947677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '029e431a31ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password', sa.String(length=255), server_default='', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('Users')
