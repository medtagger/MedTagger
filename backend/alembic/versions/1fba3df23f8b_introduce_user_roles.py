"""Introduce user roles

Revision ID: 1fba3df23f8b
Revises: 139f60b75301
Create Date: 2017-11-28 19:41:53.124884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fba3df23f8b'
down_revision = '139f60b75301'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Users_Roles',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['Roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], )
    )
    op.add_column('Users', sa.Column('active', sa.Boolean(), nullable=False))


def downgrade():
    op.drop_column('Users', 'active')
    op.drop_table('Users_Roles')
    op.drop_table('Roles')
