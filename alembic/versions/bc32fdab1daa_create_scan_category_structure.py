"""Create Scan Category structure

Revision ID: bc32fdab1daa
Revises: fcf5d0ba4bca
Create Date: 2017-10-30 20:50:17.232076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc32fdab1daa'
down_revision = 'fcf5d0ba4bca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('ScanCategories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('image_path', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )
    op.add_column('Scans', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Scans', 'ScanCategories', ['category_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'Scans', type_='foreignkey')
    op.drop_column('Scans', 'category_id')
    op.drop_table('ScanCategories')
