"""Add more user information

Revision ID: 7672053dd637
Revises: fcf5d0ba4bca
Create Date: 2017-10-31 21:12:55.609291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7672053dd637'
down_revision = 'bc32fdab1daa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Users', sa.Column('email', sa.String(length=50), nullable=False))
    op.add_column('Users', sa.Column('first_name', sa.String(length=50), nullable=False))
    op.add_column('Users', sa.Column('last_name', sa.String(length=50), nullable=False))
    op.drop_constraint('Users_username_key', 'Users', type_='unique')
    op.create_unique_constraint(None, 'Users', ['email'])
    op.drop_column('Users', 'username')


def downgrade():
    op.add_column('Users', sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'Users', type_='unique')
    op.create_unique_constraint('Users_username_key', 'Users', ['username'])
    op.drop_column('Users', 'last_name')
    op.drop_column('Users', 'first_name')
    op.drop_column('Users', 'email')
